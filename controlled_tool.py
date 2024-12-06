from __future__ import annotations

from global_states import *
from collections.abc import Awaitable
from inspect import signature
from typing import (
    Any,
    Callable,
    Optional,
    Union,
)

from pydantic import BaseModel

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.messages import ToolCall
from langchain_core.runnables import RunnableConfig, run_in_executor
from langchain_core.tools.base import (
    BaseTool,
    ToolException,
    _get_runnable_config_param,
)

class ControlledTool(BaseTool):
    """Tool that takes in function or coroutine directly."""

    description: str = ""
    func: Optional[Callable[..., str]]
    """The function to run when the tool is called."""
    coroutine: Optional[Callable[..., Awaitable[str]]] = None
    """The asynchronous version of the function."""

    # --- Runnable ---

    async def ainvoke(
        self,
        input: Union[str, dict, ToolCall],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Any:
        if not self.coroutine:
            # If the tool does not implement async, fall back to default implementation
            return await run_in_executor(config, self.invoke, input, config, **kwargs)

        return await super().ainvoke(input, config, **kwargs)

    # --- Tool ---

    @property
    def args(self) -> dict:
        """The tool's input arguments.

        Returns:
            The input arguments for the tool.
        """
        if self.args_schema is not None:
            return self.args_schema.model_json_schema()["properties"]
        # For backwards compatibility, if the function signature is ambiguous,
        # assume it takes a single string input.
        return {"tool_input": {"type": "string"}}

    def _to_args_and_kwargs(self, tool_input: Union[str, dict]) -> tuple[tuple, dict]:
        """Convert tool input to pydantic model."""
        args, kwargs = super()._to_args_and_kwargs(tool_input)
        # For backwards compatibility. The tool must be run with a single input
        all_args = list(args) + list(kwargs.values())
        if len(all_args) != 1:
            msg = (
                f"""Too many arguments to single-input tool {self.name}.
                Consider using StructuredTool instead."""
                f" Args: {all_args}"
            )
            raise ToolException(msg)
        return tuple(all_args), {}



    def _run(
        self,
        *args: Any,
        config: RunnableConfig,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> Any:
        """Use the tool."""
        if self.func:
            if run_manager and signature(self.func).parameters.get("callbacks"):
                kwargs["callbacks"] = run_manager.get_child()
            if config_param := _get_runnable_config_param(self.func):
                kwargs[config_param] = config
            # before execute the cmd, verify.
            for rule in self.rules:
                # TODO:
                #1. check if the rule is triggered.
                if rule.trigger != self.name or rule.trigger != "any":
                    continue

                #2. interpret the following prepare/condition/enforce of the rule.
                

                #3. check the enforcement of the rule:
                #   for USER_INSPECT, we either 1)continue if user authorized or 2) return an empty dict if not
                #   for SELF_REFLECT, we exit the execution to let the agent execute an new option.
                
            return self.func(*args, **kwargs)
        msg = "Tool does not support sync invocation."
        raise NotImplementedError(msg)

    async def _arun(
        self,
        *args: Any,
        config: RunnableConfig,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        **kwargs: Any,
    ) -> Any:
        """Use the tool asynchronously."""
        if self.coroutine:
            if run_manager and signature(self.coroutine).parameters.get("callbacks"):
                kwargs["callbacks"] = run_manager.get_child()
            if config_param := _get_runnable_config_param(self.coroutine):
                kwargs[config_param] = config
            return await self.coroutine(*args, **kwargs)

        # NOTE: this code is unreachable since _arun is only called if coroutine is not
        # None.
        return await super()._arun(
            *args, config=config, run_manager=run_manager, **kwargs
        )

    # TODO: this is for backwards compatibility, remove in future
    def __init__(
        self, name: str, func: Optional[Callable], description: str, rules = [], **kwargs: Any
    ) -> None:
        """Initialize tool."""
        super().__init__(  # type: ignore[call-arg]
            name=name, func=func, description=description, **kwargs
        )
        self.rules = rules
        registered_tools.add(name)

    @classmethod
    def from_function(
        cls,
        func: Optional[Callable],
        name: str,  # We keep these required to support backwards compatibility
        description: str,
        return_direct: bool = False,
        args_schema: Optional[type[BaseModel]] = None,
        coroutine: Optional[
            Callable[..., Awaitable[Any]]
        ] = None,  # This is last for compatibility, but should be after func
        **kwargs: Any,
    ) -> ControlledTool:
        """Initialize tool from a function.

        Args:
            func: The function to create the tool from.
            name: The name of the tool.
            description: The description of the tool.
            return_direct: Whether to return the output directly. Defaults to False.
            args_schema: The schema of the tool's input arguments. Defaults to None.
            coroutine: The asynchronous version of the function. Defaults to None.
            kwargs: Additional arguments to pass to the tool.

        Returns:
            The tool.

        Raises:
            ValueError: If the function is not provided.
        """
        if not coroutine is None:
            raise ValueError("unsupported coroutine")

        if func is None and coroutine is None:
            msg = "Function and/or coroutine must be provided"
            raise ValueError(msg)
        registered_tools.add(name)
        return cls(
            name=name,
            func=func,
            coroutine=coroutine,
            description=description,
            return_direct=return_direct,
            args_schema=args_schema,
            **kwargs,
        )

ControlledTool.model_rebuild()

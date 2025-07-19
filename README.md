# Pro<sup>2</sup>Guard

This is the implementation for paper:
Pro<sup>2</sup>Guard: Proactive Runtime Enforcement of LLM Agent Safety via Probabilistic Model Checking 


## 🚀 Get Started

* install PRISM 
```
cd prism
./install.sh
```
You can use prism at ./prism/bin/prism

* install pip dependencies:
```
pip install -r requirement.txt
```

### Learning DTMCs
To learn dtmcs for embodied agent and autonomous vehicles, run:
```
cd src/
python3 -m safereach.embodied_build
# or
python3 -m safereach.av_build
```

Example output DTMC in PRISM:
```
dtmc

module dtmc_model

    s : [0..4] init 0;

    [] s=0 -> 17/50 : (s'=0) + 1/50 : (s'=1) + 31/50 : (s'=2) + 1/50 : (s'=4);
    [] s=1 -> 1/4 : (s'=0) + 1/4 : (s'=1) + 1/4 : (s'=3) + 1/4 : (s'=4);
    [] s=2 -> 1/168 : (s'=0) + 45/56 : (s'=2) + 1/168 : (s'=3) + 31/168 : (s'=4);
    [] s=3 -> 1/4 : (s'=1) + 1/4 : (s'=2) + 1/4 : (s'=3) + 1/4 : (s'=4);
    [] s=4 -> 1 : (s'=4);

endmodule
```

### leverage DTMCs for monitoring (offline test)

To use DTMCs for runtime monitoring, run:
```
cd src/
python3 -m safereach.embodied_monitor
# or
python3 -m safereach.av_monitor
```

## run embodied agent with runtime enforcement:
Using Langchain + [AgentSpec](https://arxiv.org/abs/2503.18666) as llm agent with runtime enforcement, equipped with low level controller (provided by [SafeAgentBench](https://github.com/shengyin1224/SafeAgentBench)).
Example: src/embodied_agent.py
```python
from agentspec.controlled_agent_excector import initialize_controlled_agent

# ...

tool = Tool(
    name="robotic controller",
    description="High-level controller for the robot.",
    func=planner.llm_skill_interact
)
tools = [tool]  # Equip LLM with low-level controller

# Initialize controlled agent with DTMC-based proactive runtime verification
agent = initialize_controlled_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    rules=[],
    abs=kwargs["abs"],
    dtmc_path=kwargs["dtmc_path"],  # Path to DTMC (output from embodied_build)
    unsafe_states=kwargs["unsafe_states"],  # Set of unsafe states (must match DTMC states)
    cache=kwargs["cache"],  # Cache to amortize DTMC inference costs
    task_obj=kwargs["task_obj"],
    threshold=kwargs["threshold"]  # Threshold for model checking (e.g., P < threshold [F unsafe_states])
)

agent.invoke(task_description)
# ...

```

## integrating Pro<sup>2</sup>Guard on autonomous vehicle:

This can be achieved by generating [muDrive](https://arxiv.org/pdf/2407.13201) scripts that dynamically adjust planning settings.

## Extending Pro<sup>2</sup>Guard to new Domains:

The core requirement is implementing an  `Abstraction.py` class:

```python
class Abstraction(ABC):

    # Map 01-bit strings to integer indices (as PRISM stores states)
    @abstractmethod
    def get_state_idx(self) -> Dict[str, int]:
        pass

    # Encode observations into 01-bit strings representing the state
    @abstractmethod
    def encode(self, observations: List[Any]) -> str:
        pass

    # Decode 01-bit state strings back to observation list
    @abstractmethod
    def decode(self, state: str) -> List[Any]:
        pass

    # Define valid state transitions
    @abstractmethod
    def can_reach(self, state1: str, state2: str) -> bool:
        pass

    # Return possible state bitstrings satisfying a spec (condition on observation)
    @abstractmethod
    def filter(self, spec: Any) -> Set[str]:
        pass

    # Enumerate all valid states
    @abstractmethod
    def enumerate_possible_states(self) -> Set[str]:
        pass

    
```

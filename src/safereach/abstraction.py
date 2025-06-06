from abc import ABC, abstractmethod
from typing import Any, Set

class Abstraction(ABC):

    @abstractmethod
    def encode(self, observation: Any) -> str:
        pass

    @abstractmethod
    def decode(self, state: str) -> Any:
        pass

    @abstractmethod
    def can_reach(self, state1: str, state2: str) -> bool:
        pass

    @abstractmethod
    def enumerate_possible_states(self) -> Set[str]:
        pass


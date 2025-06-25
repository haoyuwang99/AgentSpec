from abc import ABC, abstractmethod
from typing import Any, Set, List, Dict

FINISH = "finish"

class Abstraction(ABC):

    @abstractmethod
    def get_state_idx(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_state_interpretation(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def encode(self, observations: List[Any]) -> str:
        pass

    @abstractmethod
    def decode(self, state: str) -> List[Any]:
        pass

    @abstractmethod
    def can_reach(self, state1: str, state2: str) -> bool:
        pass
    
    @abstractmethod
    def filter(self, spec: Any) -> Set[str]:
        pass

    @abstractmethod
    def enumerate_possible_states(self) -> Set[str]:
        pass

    
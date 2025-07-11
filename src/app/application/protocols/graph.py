from abc import ABC, abstractmethod
from typing import Dict


class CompiledGraph(ABC):
    @abstractmethod
    def invoke(self, input: Dict[str, str]) -> Dict[str, str]:
        pass
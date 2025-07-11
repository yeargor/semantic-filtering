from abc import ABC, abstractmethod
from typing import List, Any


class DatabaseGateway(ABC):
    @abstractmethod
    def similarity_search(self, query: str) -> List[Any]:
        raise NotImplementedError
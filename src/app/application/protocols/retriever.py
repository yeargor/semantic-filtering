from abc import abstractmethod, ABC


class AbstractRecipeRetriever(ABC):
    @abstractmethod
    def invoke(self, input: str):
        raise NotImplementedError
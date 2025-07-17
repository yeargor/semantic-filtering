from abc import abstractmethod, ABC


class AbstractRecipeRetriever(ABC):
    @abstractmethod
    async def ainvoke(self, input: str):
        raise NotImplementedError
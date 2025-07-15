from abc import abstractmethod, ABC


class AbstractConsumer(ABC):
    @abstractmethod
    def start(self):
        raise NotImplementedError

    @abstractmethod
    def consume(self):
        raise NotImplementedError

    @abstractmethod
    def stop(self):
        raise NotImplementedError
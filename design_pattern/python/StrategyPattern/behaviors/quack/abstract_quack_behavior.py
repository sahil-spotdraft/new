import abc


class QuackBehavior(abc.ABC):
    @abc.abstractmethod
    def quack(self):
        pass
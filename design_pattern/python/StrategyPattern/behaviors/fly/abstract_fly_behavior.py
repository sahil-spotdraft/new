import abc


class FlyBehavior(abc.ABC):
    @abc.abstractmethod
    def fly(self):
        pass
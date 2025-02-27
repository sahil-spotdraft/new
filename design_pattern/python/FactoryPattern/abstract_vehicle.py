import abc


class AbstractVehicle(abc.ABC):
    @abc.abstractmethod
    def desc(self):
        pass

    @abc.abstractmethod
    def cost(self):
        pass
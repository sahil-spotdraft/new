import abc

from FactoryPattern.AbstractFactory.vehicles import Bus, Car, LandVehicle, SeaVehicle, Ship, Yacht
from FactoryPattern.abstract_vehicle import AbstractVehicle


class AbstractFactory(abc.ABC):
    @abc.abstractmethod
    def create_cheap_transport(self) -> AbstractVehicle:
        pass
    
    @abc.abstractmethod
    def create_expensive_transport(self) -> AbstractVehicle:
        pass

    def create_obj(self, option) -> AbstractVehicle:
        if option == "cheap":
            return self.create_cheap_transport()
        else:
            return self.create_expensive_transport()


class SeaTransportFactory(AbstractFactory):
    def create_cheap_transport(self) -> SeaVehicle:
        return Ship()
    
    def create_expensive_transport(self) -> SeaVehicle:
        return Yacht()


class LandTransportFactory(AbstractFactory):
    def create_cheap_transport(self) -> LandVehicle:
        return Bus()
    
    def create_expensive_transport(self) -> LandVehicle:
        return Car()
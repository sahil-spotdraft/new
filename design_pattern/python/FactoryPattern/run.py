from FactoryPattern.AbstractFactory.factories import LandTransportFactory, SeaTransportFactory
from FactoryPattern.FactoryMethod.factories import BusFactory, CarFactory, TransportFactory
from FactoryPattern.FactoryMethod.vehicles import AbstractVehicle


class TransportationFactotryMethodExample:
    def __init__(self, option: str):
        if option == "car":
            self.factory = CarFactory()
        else:
            self.factory = BusFactory()

    def get_vehicle_obj(self) -> AbstractVehicle:
        return self.factory.createObj()
    

class TransportationAbstractFactoryExample:
    def __init__(self, transport_option: str) -> None:
        if transport_option == "sea":
            self.factory = SeaTransportFactory()
        else:
            self.factory = LandTransportFactory()
        
    def get_vehicle_obj(self, cost_option: str) -> AbstractVehicle:
        return self.factory.create_obj(cost_option)


class FactoryPatternExample:
    @staticmethod
    def run():
        # client code
        print("\n=====Execution of FactoryPattern example=====")
        # factory method
        tr = TransportationFactotryMethodExample("bus")
        obj = tr.get_vehicle_obj()
        print(obj.desc())
        print(f"I will cost you ${obj.cost()}")

        # abstract factory
        tr = TransportationAbstractFactoryExample("land")
        obj = tr.get_vehicle_obj("cheap")
        print(obj.desc())
        print(f"I will cost you ${obj.cost()}")

        
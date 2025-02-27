import abc

from FactoryPattern.abstract_vehicle import AbstractVehicle


class SeaVehicle(AbstractVehicle):
    ...


class LandVehicle(AbstractVehicle):
    ...


class Ship(SeaVehicle):
    def desc(self):
        return "I am ship and cheap"

    def cost(self):
        return 1000
    

class Yacht(SeaVehicle):
    def desc(self):
        return "I am yacht and expensive"
    
    def cost(self):
        return 2000
    

class Bus(LandVehicle):
    def desc(self):
        return "I am bus and cheap"

    def cost(self):
        return 1000
    

class Car(LandVehicle):
    def desc(self):
        return "I am car and expensive"
    
    def cost(self):
        return 2000
    
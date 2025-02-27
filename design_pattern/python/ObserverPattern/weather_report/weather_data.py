import abc
from typing import List, Optional
from ObserverPattern.abstract_observable import AbstractObservable
from ObserverPattern.abstract_observer import AbstractObserver


class WeatherData(AbstractObservable):
    def __init__(self):
        self.temperature = None
        self.humidity = None
        self.pressure = None
        super().__init__()
    
    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.measurements_changed()

    def measurements_changed(self):
        self.notifyObservers()

    def notifyObservers(self):
        for observer in self.observers:
            observer.update(self)
        
    def addObservers(self, observers: List[AbstractObserver]):
        for observer in observers:
            self.observers.append(observer)
    
    def removeObservers(self, observers: List[AbstractObserver]):
        for obeserver in observers:
            self.observers.remove(obeserver)

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_pressure(self):
        return self.pressure  

    
class AbstractDisplayElement(abc.ABC):
    @abc.abstractmethod
    def display(self):
        pass


class CurrentConditionDisplay(AbstractObserver, AbstractDisplayElement):
    def __init__(self, weather_data: AbstractObservable):
        self.temperature = None
        self.humidity = None
        self.weater_data = weather_data
        self.weater_data.addObservers([self])

    def update(self, obs: AbstractObservable):
        if not isinstance(obs, WeatherData): return
        self.temperature = obs.get_temperature()
        self.humidity = obs.get_humidity()
        self.display()

    def display(self):
        print(f"CurrentConditionDisplay - {self.temperature} / {self.humidity}")


class StatisticDisplay(AbstractObserver, AbstractDisplayElement):
    def __init__(self, weather_data: AbstractObservable):
        self.temperature = None
        self.humidity = None
        self.pressure = None
        self.weater_data = weather_data
        self.weater_data.addObservers([self])

    def update(self, obs: AbstractObservable):
        if not isinstance(obs, WeatherData): return
        self.temperature = obs.get_temperature()
        self.humidity = obs.get_humidity()
        self.pressure = obs.get_pressure()
        self.display()

    def display(self):
        print(f"StatisticDisplay - {self.temperature} / {self.humidity} / {self.pressure}")

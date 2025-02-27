from typing import List


class Observer:
    def update(self, data):
        pass

class Observable:
    def __init__(self):
        self._observers: List[Observer] = []

    def add_observers(self, observers: List[Observer]):
        self._observers.extend(
            observers
        )
    
    def remove_observers(self, observers: List[Observer]):
        for obs in observers:
            self._observers.remove(
                obs
            )
    
    def notify_observers(self):
        pass


class WeatherSensor(Observable):
    def __init__(self, temperature, moisture):
        super().__init__()
        self.temperature = temperature
        self.moisture = moisture

    def set_weather_report(self, temperature, moisture):
        self.temperature = temperature
        self.moisture = moisture
        self.notify_observers()

    def notify_observers(self):
        for obs in self._observers:
            obs.update(self)


class TemperatureReport(Observer):
    def update(self, data: WeatherSensor):
        print(f"Temperature - {data.temperature}")

class MoistureReport(Observer):
    def update(self, data: WeatherSensor):
        print(f"Moisture - {data.moisture}")

obj = WeatherSensor(30, 240)
obs1 = TemperatureReport()
obs2 = MoistureReport()
obj.add_observers([obs1, obs2])

obj.set_weather_report(45, 230)
obj.remove_observers([obs1])
obj.set_weather_report(34, 210)

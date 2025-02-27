from ObserverPattern.weather_report.weather_data import CurrentConditionDisplay, StatisticDisplay, WeatherData


class ObserverPatterExample:
    @staticmethod
    def run():
        print("\n=====Execution of ObserverPatter example=====")
        weather_data = WeatherData()
        current_condition_display = CurrentConditionDisplay(weather_data)
        statistic_display = StatisticDisplay(weather_data)

        weather_data.set_measurements(27, 65, 30.2)
        weather_data.removeObservers([current_condition_display])
        weather_data.set_measurements(32, 85, 27.4)
        current_condition_display.display()

from StrategyPattern.behaviors.fly.fly_behaviors import FlyNoWay
from StrategyPattern.duck_simulator.duck import MallardDuck, WoodenDuck


class StartegyPatternExample:
    @staticmethod
    def run():
        print("\n=====Execution of StartegyPattern example=====")
        # mallard_duck = MallardDuck()
        # mallard_duck.display()
        # mallard_duck.quack()
        # mallard_duck.fly()
        # mallard_duck.setFlyBehavior(FlyNoWay())
        # mallard_duck.fly()

        wooden_duck = WoodenDuck()
        wooden_duck.display()
        wooden_duck.quack()
        wooden_duck.fly()

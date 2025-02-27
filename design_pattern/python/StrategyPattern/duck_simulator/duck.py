from StrategyPattern.behaviors.fly.fly_behaviors import FlyNoWay, FlyWithWings
from StrategyPattern.behaviors.quack.abstract_quack_behavior import QuackBehavior
from StrategyPattern.behaviors.fly.abstract_fly_behavior import FlyBehavior
from StrategyPattern.behaviors.quack.quack_behaviors import Mute, Quack


class Duck:
    def __init__(self):
        self.quackBehavior = QuackBehavior()
        self.flyBehavior = FlyBehavior()

    def quack(self):
        self.quackBehavior.quack()

    def fly(self):
        self.flyBehavior.fly()

    def swim(self):
        print("Duck swim")
    
    def display(self):
        print("I am a Duck")

    def setQuackBehavior(self, quackBehavior: QuackBehavior):
        self.quackBehavior = quackBehavior

    def setFlyBehavior(self, flyBehavior: FlyBehavior):
        self.flyBehavior = flyBehavior


class MallardDuck(Duck):
    def __init__(self):
        self.quackBehavior = Quack()
        self.flyBehavior = FlyWithWings()

    def display(self):
        print("I am a mallard duck")


class WoodenDuck(Duck):
    def __init__(self):
        self.quackBehavior = Mute()
        self.flyBehavior = FlyNoWay()

    def display(self):
        print("I am a wooden duck")

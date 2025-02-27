from StrategyPattern.behaviors.quack.abstract_quack_behavior import QuackBehavior


class Quack(QuackBehavior):
    def quack(self):
        print("Quack")

class Squeak(QuackBehavior):
    def quack(self):
        print("Squeak")

class Mute(QuackBehavior):
    def quack(self):
        print("Mute")
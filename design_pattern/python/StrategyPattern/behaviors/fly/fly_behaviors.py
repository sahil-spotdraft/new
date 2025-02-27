from StrategyPattern.behaviors.fly.abstract_fly_behavior import FlyBehavior


class FlyWithWings(FlyBehavior):
    def fly(self):
        print("Fly with wings")


class FlyNoWay(FlyBehavior):
    def fly(self):
        print("Fly no way")

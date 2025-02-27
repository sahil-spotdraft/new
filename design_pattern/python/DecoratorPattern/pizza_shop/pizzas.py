import abc


class AbstractItem(abc.ABC):
    def __init__(self):
        self.desc = "Plain pizza"

    def description(self):
        return self.desc

    @abc.abstractmethod
    def cost(self):
        pass


class DoubleCheesePizza(AbstractItem):
    def __init__(self):
        self.desc = "DoubleCheesePizza"
    
    def cost(self):
        return .89
    

class ThinCrustPizza(AbstractItem):
    def __init__(self):
        self.desc = "ThinCrustPizza"

    def cost(self):
        return 1.22  

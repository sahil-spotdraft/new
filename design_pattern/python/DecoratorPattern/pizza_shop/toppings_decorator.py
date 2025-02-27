from DecoratorPattern.pizza_shop.pizzas import AbstractItem


class ToppingDecorator(AbstractItem):
    def __init__(self, pizza: AbstractItem):
        self.pizza = pizza

    def description(self):
        return self.pizza.description()

    def cost(self):
        return self.pizza.cost()
    

class TomatoSauce(ToppingDecorator):
    def __init__(self, pizza: AbstractItem):
        super().__init__(pizza)

    def description(self):
        return self.pizza.description() + "+" + "TomatoSauce"
    
    def cost(self):
        return self.pizza.cost() + 0.12
    

class Mozzarella(ToppingDecorator):
    def __init__(self, pizza: AbstractItem):
        super().__init__(pizza)
    
    def description(self):
        return self.pizza.description() + "+" + "Mozzarella"
    
    def cost(self):
        return self.pizza.cost() + 0.32

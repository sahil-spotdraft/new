from DecoratorPattern.pizza_shop.pizzas import DoubleCheesePizza
from DecoratorPattern.pizza_shop.toppings_decorator import Mozzarella, TomatoSauce


class DecoratorPatternExample:
    @staticmethod
    def run():
        print("\n=====Execution of DecoratorPatternExample example=====")
        # pizza_1 = DoubleCheesePizza()
        # pizza_1 = Mozzarella(pizza_1)
        # print(pizza_1.description(), ": $", pizza_1.cost())

        
        
        pizza_2 = DoubleCheesePizza()
        pizza_2 = TomatoSauce(pizza_2)
        pizza_2 = TomatoSauce(pizza_2)
        pizza_2 = Mozzarella(pizza_2)
        print(pizza_2.description(), ": $", pizza_2.cost())

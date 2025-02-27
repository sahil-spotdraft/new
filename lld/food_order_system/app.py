from collections import defaultdict
import heapq
from typing import Dict, List


class Order:
    def __init__(self, id, restaurant_id, food_item_id):
        self.id = id
        self.restaurant_id = restaurant_id
        self.food_item_id = food_item_id
        self.rating = 0

class OrderManager:
    def __init__(self):
        self.orders: Dict[str, "Order"] = {}
        self._observers: List["ListRestaurants"] = []

    def add_observers(self, observers):
        self._observers.extend(observers)

    def _notify_observers(self, order):
        for observer in self._observers:
            observer.update(order)

    def order_food(self, order_id, restaurant_id, food_item_id):
        order = Order(
            id=order_id, restaurant_id=restaurant_id, food_item_id=food_item_id
        )
        self.orders[order_id] = order
    
    def rate_food(self, order_id, rating):
        order = self.orders[order_id]
        order.rating = rating
        self._notify_observers(order)

class ListRestaurants:
    def update(self, order: Order):
        pass

    def list_restaurants(self, *args, **kwargs):
        pass
    
class Rating:
    def __init__(self):
        self.sum = 0
        self.count = 0

    def update(self, val):
        self.sum += val
        self.count += 1

    def get_avg(self):
        if self.count <= 0:
            return 0
        rating = self.sum /self.count
        return round(rating, 1)
    
    def __repr__(self):
        return f"sum {self.sum}, cnt {self.count}, avg {self.get_avg()}"

class MostRatedRestaurants(ListRestaurants):
    def __init__(self):
        self.restaurant_id_to_rating_map = defaultdict(lambda: Rating())

    def update(self, order):
        self.restaurant_id_to_rating_map[order.restaurant_id].update(order.rating)

    def list_restaurants(self):
        return [
            (restuarant_id, self.restaurant_id_to_rating_map[restuarant_id].get_avg())
            for restuarant_id in sorted(
                self.restaurant_id_to_rating_map, key=lambda x: (-self.restaurant_id_to_rating_map[x].get_avg(), x[0])
            )
        ]

class MostRatedRestaurantsByFood(ListRestaurants):
    def __init__(self):
        self.food_id_to_rating_map = defaultdict(lambda: defaultdict(lambda: Rating()))

    def update(self, order):
        self.food_id_to_rating_map[order.food_item_id][order.restaurant_id].update(order.rating)

    def list_restaurants(self, food_id):
        restaurant_ids = list(self.food_id_to_rating_map[food_id].keys())
        restaurant_ids.sort()
        return heapq.nlargest(
            20,
            restaurant_ids, 
            key=lambda restaurant_id: self.food_id_to_rating_map[food_id][restaurant_id].get_avg()
        )

class FoodOrderingSystem:
    def __init__(self):
        self.order_manager = OrderManager()
        self.most_rated_restaurants = MostRatedRestaurants()
        self.most_rated_restaurants_by_food = MostRatedRestaurantsByFood()
        self.order_manager.add_observers(
            [self.most_rated_restaurants, self.most_rated_restaurants_by_food]
        )

    def order_food(self, order_id, restaurant_id, food_item_id):
        self.order_manager.order_food(order_id, restaurant_id, food_item_id)

    def rate_order(self, order_id, rating):
        self.order_manager.rate_food(order_id, rating)

    def get_top_restaurants_by_food(self, food_item_id):
        return self.most_rated_restaurants_by_food.list_restaurants(food_item_id)
    
    def get_top_rated_restaurants(self):
        return self.most_rated_restaurants.list_restaurants()
    

# client
obj = FoodOrderingSystem()

obj.order_food(order_id = 'order-0', food_item_id = 'food-1', restaurant_id = 'restaurant-0')
obj.rate_order(order_id = 'order-0', rating = 3)
obj.order_food(order_id = 'order-1', food_item_id = 'food-0', restaurant_id = 'restaurant-2')
obj.rate_order(order_id = 'order-1', rating = 1)
obj.order_food(order_id = 'order-2', food_item_id = 'food-0', restaurant_id = 'restaurant-1')
obj.rate_order(order_id = 'order-2', rating = 3)
obj.order_food(order_id = 'order-3', food_item_id = 'food-0', restaurant_id = 'restaurant-2')
obj.rate_order(order_id = 'order-3', rating = 5)
obj.order_food(order_id = 'order-4', food_item_id = 'food-0', restaurant_id = 'restaurant-0')
obj.rate_order(order_id = 'order-4', rating = 3)
obj.order_food(order_id = 'order-5', food_item_id = 'food-0', restaurant_id = 'restaurant-1')
obj.rate_order(order_id = 'order-5', rating = 4)
obj.order_food(order_id = 'order-6', food_item_id = 'food-1', restaurant_id = 'restaurant-0')
obj.rate_order(order_id = 'order-6', rating = 2)
obj.order_food(order_id = 'order-7', food_item_id = 'food-1', restaurant_id = 'restaurant-0')
obj.rate_order(order_id = 'order-7', rating = 2)
obj.order_food(order_id = 'order-8', food_item_id = 'food-0', restaurant_id = 'restaurant-1')
obj.rate_order(order_id = 'order-8', rating = 2)
obj.order_food(order_id = 'order-9', food_item_id = 'food-0', restaurant_id = 'restaurant-1')
obj.rate_order(order_id = 'order-9', rating = 4)
print(obj.get_top_restaurants_by_food('food-0'))
print(obj.get_top_restaurants_by_food('food-1'))
print(obj.get_top_rated_restaurants())

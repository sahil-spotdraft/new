from collections import defaultdict
from typing import List

class RateOrderObserver:
    def update(self, order):
        pass

class Solution:
    def __init__(self):
        self.ordersManager = OrdersManager()
        self.mostRatedRestaurants = MostRatedRestaurants()
        self.mostRatedRestaurantsByFood = MostRatedRestaurantsByFood()
        self.ordersManager.addObserver(self.mostRatedRestaurants)
        self.ordersManager.addObserver(self.mostRatedRestaurantsByFood)

    def order_food(self, order_id, restaurant_id, food_item_id):
        self.ordersManager.orderFood(order_id, restaurant_id, food_item_id)

    def rate_order(self, order_id, rating):
        self.ordersManager.rateOrder(order_id, rating)

    def get_top_restaurants_by_food(self, food_item_id) -> List[str]:
        return self.mostRatedRestaurantsByFood.getRestaurants(food_item_id, 20)

    def get_top_rated_restaurants(self) -> List[str]:
        return self.mostRatedRestaurants.getRestaurants(20)

class OrdersManager:
    def __init__(self):
        self.map = {}
        self.observers = []

    def orderFood(self, orderId, restaurantId, foodItemId):
        order = Order(orderId, restaurantId, foodItemId, 0)
        self.map[orderId] = order

    def rateOrder(self, orderId, rating):
        order = self.map[orderId]
        order.setRating(rating)
        self.notifyAll(order)

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyAll(self, order):
        for observer in self.observers:
            observer.update(order)

class MostRatedRestaurants(RateOrderObserver):
    def __init__(self):
        self.ratings = defaultdict(lambda: Rating(0, 0))

    def update(self, order):
        if order.getRestaurantId() not in self.ratings:
            self.ratings[order.getRestaurantId()] = Rating(0, 0)
        rating = self.ratings[order.getRestaurantId()]
        rating.add(order.getRating())

    def getRestaurants(self, n) -> List[str]:
        sorted_restaurants = sorted(self.ratings.keys(),
           key=lambda x: (-self.ratings[x].getAverageRating(), x))
        return [(x, self.ratings[x].getAverageRating()) for x in sorted_restaurants[:n]]

class MostRatedRestaurantsByFood(RateOrderObserver):
    def __init__(self):
        self.ratings = defaultdict(lambda: defaultdict(lambda: Rating(0, 0)))

    def update(self, order):
        if order.getFoodItemId() not in self.ratings:
            self.ratings[order.getFoodItemId()] = defaultdict(lambda: Rating(0, 0))
        restaurants_map = self.ratings[order.getFoodItemId()]
        if order.getRestaurantId() not in restaurants_map:
            restaurants_map[order.getRestaurantId()] = Rating(0, 0)
        rating = restaurants_map[order.getRestaurantId()]
        rating.add(order.getRating())

    def getRestaurants(self, foodItemId, n) -> List[str]:
        if foodItemId not in self.ratings:
            return []
        restaurants_map = self.ratings[foodItemId]
        sorted_restaurants = sorted(
            restaurants_map.keys(),
            key=lambda x: (-restaurants_map[x].getAverageRating(), x)
        )
        return sorted_restaurants[:n]

class Rating:
    def __init__(self, sum, count):
        self.sum = sum
        self.count = count

    def __str__(self):
        return f"sum {self.sum}, count {self.count}, avg {self.getAverageRating()}"

    def getAverageRating(self):
        if self.count <= 0:
            return 0
        rating = self.sum / self.count
        rating = round(rating, 1)#int((rating + 0.05) * 10) / 10.0
        return rating

    def add(self, num):
        self.sum += num
        self.count += 1

class Order:
    def __init__(self, orderId, restaurantId, foodItemId, rating):
        self.orderId = orderId
        self.restaurantId = restaurantId
        self.foodItemId = foodItemId
        self.rating = rating

    def setRating(self, rating):
        self.rating = rating

    def getRestaurantId(self):
        return self.restaurantId

    def getFoodItemId(self):
        return self.foodItemId

    def getRating(self):
        return self.rating

# client
obj = Solution()

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

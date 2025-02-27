from collections import defaultdict
import enum


SPOT_TYPE = str

class ParkingType(enum.Enum):
    INACTIVE = (0, None)
    WHEELER_2 = (2, "2-Wheeler")
    WHEELER_4 = (4, "4-Wheeler")

    def __init__(self, type: int,  category):
        self.type = type
        self.category = category
        super().__init__()

    @classmethod
    def get_values(cls):
        return [
            item.type
            for item in cls
        ]


class Helper:
    def print(self, msg: str):
        print(msg, end=" ")

    def println(self, msg: str):
        print(msg)


class ParkingFloor:
    def __init__(self, floor: int, grid: list, helper: Helper):
        self.helper = helper
        self.floor_parking_type_count = {
            i: 0 for i in ParkingType.get_values()
        }
        self.parking_spots = [[None for _ in range(len(grid))] for _ in range(len(grid))]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                try:
                    self.floor_parking_type_count[grid[i][j]] += 1
                except KeyError:
                    helper.println("Not a valid parking type")
                    return
                if grid[i][j] != 0:
                    self.parking_spots[i][j] = ParkingSpot(
                        f"{floor}-{i}-{j}", grid[i][j], helper
                    )
        

    def get_free_spots_count(self, vehicle_type):
        return self.floor_parking_type_count.get(vehicle_type, 0)
    
    def park(self, vehicle_type, vehicle_number, ticket_id):
        for i in range(len(self.parking_spots)):
            for j in range(len(self.parking_spots[i])):
                spot = self.parking_spots[i][j]
                assert isinstance(spot, ParkingSpot)
                if not spot.vehicle_type == vehicle_type:
                    continue
                if spot.vacant:
                    spot.occupy()
                    self.floor_parking_type_count[vehicle_type] -= 1
                    return spot.spot_id
            
    def remove_vehicle(self, row, col):
        if row < 0 or row >= len(self.parking_spots) or col < 0 or col >= len(self.parking_spots[0]) or self.parking_spots[row][col].vacant:
            return False
        vehicle_type = self.parking_spots[row][col].vehicle_type
        self.floor_parking_type_count[vehicle_type] += 1
        self.parking_spots[row][col].release()
        return True

class ParkingSpot:
    def __init__(self, spot_id: str, vehicle_type: int, helper: Helper):
        self.spot_id = spot_id
        self.vacant = True
        self.vehicle_type = vehicle_type
        self.helper = helper

    def occupy(self):
        self.vacant = False
    
    def release(self):
        self.vacant = True


class NearestParkingStrategy:
    def park(self, floors: list, vehicle_type, vehicle_number, ticket_id):
        for floor in floors:
            spot_id = floor.park(vehicle_type, vehicle_number, ticket_id)
            if spot_id: return spot_id
        return ""
    

class MostFreeSpaceParkingStrategy:
    def park(self, floors: list, vehicle_type, vehicle_number, ticket_id):
        mp = defaultdict(list)
        for floor in floors:
            vacancy = floor.vacancy_for_vehicle_type(vehicle_type)
            mp[vacancy].append(floor)

        max_vacancy = max(mp)
        for floor in mp[max_vacancy]:
            spot_id = floor.park(vehicle_type, vehicle_number, ticket_id)
            if spot_id: return spot_id
        return ""


class ParkingService:
    def __init__(self):
        self.parking_strategies = {
            0: NearestParkingStrategy(),
            1: MostFreeSpaceParkingStrategy()
        }

    def park(self, floors, vehicle_type, vehicle_number, ticket_id, parking_strategy):
        if parking_strategy in self.parking_strategies:
            return self.parking_strategies[parking_strategy].park(
                floors, vehicle_type, vehicle_number, ticket_id
            )
        return ""
    

class SearchService:
    def __init__(self):
        self.cache = {}

    def index(self, vehicle_number, ticket_id, spot_id):
        self.cache[vehicle_number] = spot_id
        self.cache[ticket_id] = spot_id

    def remove(self, vehicle_number, ticket_id):
        del self.cache[vehicle_number]
        del self.cache[ticket_id]

    def search(self, query):
        return self.cache.get(query, "")


class ParkingLotSystem:
    def __init__(self, helper: Helper, parking: list):
        self.helper = helper
        print("Added new parking data in memory")
        self.floors = [
            ParkingFloor(i, parking[i], helper)
            for i in range(len(parking))
        ]
        self.parking_service = ParkingService()
        self.search_service = SearchService()

    def park(self, vehicle_type: int, vehicle_number: str, ticket_id: str, parking_strategy: int) -> SPOT_TYPE:
        spot_id = self.parking_service.park(self.floors, vehicle_type, vehicle_number, ticket_id, parking_strategy)
        if spot_id:
            self.search_service.index(vehicle_number, ticket_id, spot_id)
        return spot_id
        
    def remove_vehicle(self, spot_id: str) -> bool:
        floor_index, row, col = map(int, spot_id.split('-'))
        return self.floors[floor_index].remove_vehicle(row, col)

    def get_free_spots_count(self, floor: int, vehicle_type: int) -> int:
        return self.floors[floor].get_free_spots_count(vehicle_type)

    def search(self, query: str) -> str:
        return self.search_service.search(query)


parking = [[
[4, 4, 2, 2],
[2, 4, 2, 0],
[0, 2, 2, 2],
[4, 4, 4, 0]]]
helper = Helper()
app = ParkingLotSystem(
    helper=helper, parking=parking
)

print(app.park(2, "bh234", "tkt4534", 0))
print(app.search("tkt4534"))
print(app.get_free_spots_count(0, 2))
print(app.remove_vehicle("0-0-2"))
print(app.get_free_spots_count(0, 2))
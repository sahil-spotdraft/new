UPWARD = "U"
DOWNWARD = "D"
IDLE = "I"

class AbstractElevatorState:
    def get_time_to_reach_floor(self, floor, current_floor):
        """Method to get dist b/w current floor to given floor"""
        pass 

    def sync_lift_data(self, lift: "Lift"):
        pass

class IdleState(AbstractElevatorState):
    def __init__(self):
        self.type = IDLE

    def get_time_to_reach_floor(self, floor, current_floor):
        return abs(current_floor -floor)
    
    def sync_lift_data(self, lift: "Lift"):
        return

class MovingUpwardState(AbstractElevatorState):
    def __init__(self):
        self.type = UPWARD

    def get_time_to_reach_floor(self, floor, current_floor):
        if floor < current_floor:
            return -1
        return floor -current_floor
    
    def sync_lift_data(self, lift: "Lift"):
        if lift.current_floor in lift.destination_floors:
            lift.destination_floors.discard(
                lift.current_floor
            )
            lift.floors_to_visit.discard(
                lift.current_floor
            )
            lift.head_count -= 1
        if len(lift.destination_floors) == 0:
            assert lift.head_count == 0
            lift.state = IdleState()
        else:
            lift.current_floor += 1
       
class MovingDownwardState(AbstractElevatorState):
    def __init__(self):
        self.type = DOWNWARD

    def get_time_to_reach_floor(self, floor, current_floor):
        if floor > current_floor:
            return -1
        return current_floor -floor
    
    def sync_lift_data(self, lift: "Lift"):
        if lift.current_floor in lift.destination_floors:
            lift.destination_floors.discard(
                lift.current_floor
            )
            lift.floors_to_visit.discard(
                lift.current_floor
            )
            lift.head_count -= 1
        if len(lift.destination_floors) == 0:
            assert lift.head_count == 0
            lift.state = IdleState()
        else:
            lift.current_floor -= 1

class Lift:
    def __init__(self, id, capacity):
        self.id = id
        self.state = IdleState()
        self.capacity = capacity
        self.head_count = 0
        self.floors_to_visit = set()
        self.destination_floors = set()
        self.current_floor = 0

    def __str__(self):
        return f"{self.current_floor}-{self.state.type}"
    
    def __repr__(self):
        return f"{self.id}: {self.current_floor} moving {self.state.type}; {self.floors_to_visit}"

    def get_time_to_reach_floor(self, floor):
        if self.head_count == self.capacity: return -1
        # print(f"get time {self.id} {self.current_floor}")
        return self.state.get_time_to_reach_floor(floor, self.current_floor)
    
    def accept_request(self, src_floor, dest_floor, direction):
        self.head_count += 1
        self.state = MovingUpwardState() if direction == UPWARD else MovingDownwardState()
        self.floors_to_visit.add(src_floor)
        self.floors_to_visit.add(dest_floor)
        self.destination_floors.add(dest_floor)

    def get_number_of_people_on_lift(self): 
        return self.head_count
    
    def sync_lift_data(self):
        self.state.sync_lift_data(self)

class ElevatorManagement:
    def __init__(self, total_floors, lifts):
        self.lifts = [
            Lift(i, 10) for i in range(lifts)
        ]
        self.total_floors = total_floors

    def _filter_lifts(self, states):
        return list(
            filter(
                lambda x: x.state.type in states, self.lifts
            )
        )
    
    def _is_valid_floor(self, floors):
        return all(0 <= floor < self.total_floors for floor in floors)
    
    def request_lift(self, src_floor, dest_floor):
        # if not self._is_valid_floor([src_floor, dest_floor]): return -1
        direction = UPWARD if dest_floor > src_floor else DOWNWARD
        lifts = self._filter_lifts([IDLE, direction])
        time_to_index_map = {}
        for i in range(len(lifts)):
            lift = self.lifts[i]
            assert isinstance(lift, Lift)
            time = self.lifts[i].get_time_to_reach_floor(src_floor)
            if time not in time_to_index_map and time != -1:
                time_to_index_map[time] = lift.id
        # print(time_to_index_map)
        lift_id = time_to_index_map[min(time_to_index_map)] if time_to_index_map else -1
        if lift_id != -1:
            self.lifts[lift_id].accept_request(
                src_floor, dest_floor, direction
            )
        return lift_id
    
    def get_lift_states(self):
        result = []
        for i in range(len(self.lifts)):
            result.append(str(self.lifts[i]))
        return result
    
    def get_number_of_people_on_lift(self, lift_id):
        return self.lifts[lift_id].get_number_of_people_on_lift()
    
    def tick(self):
        # breakpoint()
        for i in range(len(self._filter_lifts([UPWARD, DOWNWARD]))):
            lift = self.lifts[i]
            assert isinstance(lift, Lift)
            lift.sync_lift_data()
            print(f"{i} - floor: {lift.current_floor}, {lift.state.type}, {list(lift.floors_to_visit)}")

    def get_lifts_stopping_on_floor(self, floor, move_direction):
        result = []
        for i in range(len(self._filter_lifts([move_direction]))):
            lift = self.lifts[i]
            assert isinstance(lift, Lift)
            if floor in lift.floors_to_visit:
                result.append(lift.id)
        return result
    

obj = ElevatorManagement(6, 2)
print(f"Request - {obj.request_lift(0, 3)}")
obj.tick()
print(f"Request - {obj.request_lift(0, 2)}")
obj.tick()
print(f"Request - {obj.request_lift(0, 5)}")
print(f"Request - {obj.request_lift(1, 0)}")
obj.tick()
obj.tick()
obj.tick()  
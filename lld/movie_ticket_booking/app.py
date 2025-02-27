from collections import defaultdict

class Show:
    def __init__(self, cinema_id, show_id, start_time, end_time):
        self.cinema_id = cinema_id
        self.show_id = show_id
        self.start_time = start_time
        self.end_time = end_time

class Screen:
    def __init__(self, screen_row, screen_column):
        self.movie_id_to_show_id_mapping = defaultdict(list)
        self.seats = [[True for _ in range(screen_column)] for _ in range(screen_row)]
        self.free_seats_count = screen_column *screen_row

class Cinema:
    def __init__(self, city_id, cinema_id, screen_count, screen_row, screen_column):
        self.city_id = city_id
        self.cinema_id = cinema_id
        self.screens = [
            Screen(screen_row, screen_column) for _ in range(screen_count)
        ]
        self.show_id_to_screen_mapping = {}

    def add_show(self, show_id, screen_index):
        if 0 > screen_index -1 >= len(self.screens):
            print(f"Screen not found")
            return
        self.show_id_to_screen_mapping[show_id] = self.screens[screen_index]

    def get_screen(self, show_id):
        return self.show_id_to_screen_mapping[show_id]

    def get_free_seats_count(self, show_id):
        screen = self.show_id_to_screen_mapping[show_id]
        assert isinstance(screen, Screen)
        return screen.free_seats_count

class SearchManager:
    def __init__(self):
        self.cinema_id_to_city_id_mapping = {}
        self.movie_id_and_city_id_to_cinema_id_mapping = defaultdict(list)
        self.moview_id_and_cinema_id_to_show_id_mapping = defaultdict(list)
    
    def add_cinema(self, cinema_id, city_id):
        self.cinema_id_to_city_id_mapping[cinema_id] = city_id
    
    def add_show(self, show_id, movie_id, cinema_id):
        city_id = self.cinema_id_to_city_id_mapping.get(cinema_id, None)
        if not city_id:
            print(f"Cinema - {cinema_id} not found")
            return
        self.movie_id_and_city_id_to_cinema_id_mapping[movie_id, city_id].append(cinema_id)
        self.moview_id_and_cinema_id_to_show_id_mapping[movie_id, cinema_id].append(show_id)

class BookingManager:
    def __init__(self):
        self.bookings = {}
        self.ticket_id_to_screen_mapping = {}

    def _allocate_seats(self, screen, tickets_count):
        assert isinstance(screen, Screen)
        if screen.free_seats_count <tickets_count: return []
        seats = screen.seats
        random_res = []
        for i in range(len(seats)):
            continuous_res = []
            for j in range(len(seats[i])):
                if seats[i][j]:
                    continuous_res.append(
                        f"{i}-{j}"
                    )
                    if len(random_res) <tickets_count:
                        random_res.append(
                            f"{i}-{j}"
                        )
                else:
                    continuous_res = []
                if len(continuous_res) == tickets_count:
                    return continuous_res
                
        if len(random_res) == tickets_count: return random_res
        return []
    
    def book_seats(self, ticket_id, screen, tickets_count):
        assert isinstance(screen, Screen)
        allocated_seats = self._allocate_seats(
            screen, tickets_count
        )
        seats = screen.seats
        for seat in allocated_seats:
            i, j = list(seat.split("-"))
            seats[int(i)][int(j)] = False
        screen.free_seats_count -= len(allocated_seats)
        if allocated_seats:
            self.bookings[ticket_id] = allocated_seats
            self.ticket_id_to_screen_mapping[ticket_id] = screen
        return allocated_seats
    
    def unbook_seats(self, ticket_id):
        if ticket_id not in self.bookings:
            return False
        screen = self.ticket_id_to_screen_mapping[ticket_id]
        assert isinstance(screen, Screen)
        seats = self.bookings[ticket_id]
        for seat in seats:
            i, j = list(seat.split("-"))
            screen.seats[int(i)][int(j)] = True
        screen.free_seats_count += len(seats)
        self.bookings.pop(ticket_id)
        self.ticket_id_to_screen_mapping.pop(ticket_id)
        return True

class MovieBookingSystem:
    def __init__(self):
        self.cinemas = {}
        self.shows = {}
        self.search_manager = SearchManager()
        self.booking_manager = BookingManager()

    def add_cinema(
        self, cinema_id, city_id, screen_count, screen_row, screen_column
    ):
        self.search_manager.add_cinema(cinema_id, city_id)
        self.cinemas[cinema_id] = Cinema(city_id, cinema_id, screen_count, screen_row, screen_column)

    def add_show(self, show_id, movie_id, cinema_id, screen_index, start_time, end_time):
        cinema = self.cinemas.get(cinema_id, None)
        if not cinema:
            print(f"Cinema - {cinema_id} not found")
            return
        assert isinstance(cinema, Cinema)
        self.search_manager.add_show(show_id, movie_id, cinema_id)
        cinema.add_show(
            show_id, screen_index
        )
        self.shows[show_id] = Show(cinema_id, show_id, start_time, end_time)
    
    def get_free_seats_count(self, show_id):
        if show_id not in self.shows: return 0
        show = self.shows[show_id]
        assert isinstance(show, Show)
        cinema = self.cinemas[show.cinema_id]
        return cinema.get_free_seats_count(show_id)
    
    def book_ticket(self, ticket_id, show_id, tickets_count):
        show = self.shows[show_id]
        assert isinstance(show, Show)
        cinema = self.cinemas[show.cinema_id]
        screen = cinema.get_screen(show_id)
        seats = self.booking_manager.book_seats(
            ticket_id, screen, tickets_count
        )   
        if seats:
            return seats
        return []  
    
    def cancel_ticket(self, ticket_id):
        return self.booking_manager.unbook_seats(
            ticket_id
        )
    
    def list_cinemas(self, movie_id, city_id):
        return sorted(
            self.search_manager.movie_id_and_city_id_to_cinema_id_mapping.get(
                (movie_id, city_id), []
            )
        )
    
    def list_shows(self, movie_id, cinema_id):
        show_ids = self.search_manager.moview_id_and_cinema_id_to_show_id_mapping.get(
            (movie_id, cinema_id), []
        )
        return sorted(
            show_ids, key=lambda show_id: (self.shows[show_id].start_time, self.shows[show_id].end_time)
        )
    

app = MovieBookingSystem()
app.add_cinema(
    0, 1, 4, 5, 10
)
app.add_show(
    1, 4, 0, 1, 1710516108725, 1710523308725
)
app.add_show(
    2, 11, 0, 3, 17105161085, 1710523308725
)
app.add_show(
    3, 11, 0, 3, 171051619090, 171052330890
)

print(app.list_cinemas(
    0, 1
))
print(app.list_shows(
    4, 0
))
print(app.list_shows(
    11, 0
))
print(app.get_free_seats_count(
    1
))
print(app.book_ticket(
    'tkt-1', 1, 4
))
print(app.get_free_seats_count(
    1
))
print(app.book_ticket(
    'tkt-2', 1, 8
))
print(app.get_free_seats_count(
    1
))
print(
    app.cancel_ticket(
        'tkt-1'
    )
)
print(app.get_free_seats_count(
    1
))
print(
    app.cancel_ticket(
        'tkt-1'
    )
)
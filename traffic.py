import random

from collections import defaultdict
from termcolor import cprint, colored

# directions
N = (0,1)
E = (1,0)
S = (0,-1)
W = (-1,0)
NW = (-1,1)
NE = (1,1)
SE = (1,-1)
SW = (-1,-1)

# grid size
GRID_MIN = 0
GRID_MAX = 17

# middle of grid. used for relative coordinates of lanes, lights, etc.
GRID_MID = GRID_MAX // 2

# coordinates of the various lanes
GRID_RANGE = range(GRID_MIN, GRID_MAX)
NORTHBOUND1 = [(GRID_MID+1,y) for y in GRID_RANGE]
NORTHBOUND2 = [(GRID_MID+2,y) for y in GRID_RANGE]
SOUTHBOUND1 = [(GRID_MID-1,y) for y in GRID_RANGE]
SOUTHBOUND2 = [(GRID_MID-2,y) for y in GRID_RANGE]
WESTBOUND1 = [(x,GRID_MID+1) for x in GRID_RANGE]
WESTBOUND2 = [(x,GRID_MID+2) for x in GRID_RANGE]
EASTBOUND1 = [(x,GRID_MID-2) for x in GRID_RANGE]
EASTBOUND2 = [(x,GRID_MID-1) for x in GRID_RANGE]
NORTHRIGHT = [(GRID_MID+3,y) for y in range(GRID_MIN,GRID_MID-2)]
SOUTHRIGHT = [(GRID_MID-3,y) for y in range(GRID_MID+3,GRID_MAX)]
EASTRIGHT = [(x,GRID_MID-3) for x in range(GRID_MIN,GRID_MID-2)]
WESTRIGHT = [(x,GRID_MID+3) for x in range(GRID_MID+3,GRID_MAX)]
NORTHLEFT = [(GRID_MID,y) for y in range(GRID_MIN,GRID_MID)]
SOUTHLEFT = [(GRID_MID,y) for y in range(GRID_MID+1,GRID_MAX)]
EASTLEFT = [(x,GRID_MID) for x in range(GRID_MIN,GRID_MID)]
WESTLEFT = [(x,GRID_MID) for x in range(GRID_MID+1,GRID_MAX)]
MIDDLE = [(GRID_MID,GRID_MID)]

LANES = NORTHBOUND1 + NORTHBOUND2 + SOUTHBOUND1 + SOUTHBOUND2 + \
        EASTBOUND1 + EASTBOUND2 + WESTBOUND1 + WESTBOUND2 + \
        NORTHRIGHT + SOUTHRIGHT + EASTRIGHT + WESTRIGHT + \
        NORTHLEFT + SOUTHLEFT + EASTLEFT + WESTLEFT + \
        MIDDLE

# coordinates of the lights.
# basically the entry points into the intersection, for each lane
# a car may not move into a coordinate that is a red light
NORTH_LEFT_LIGHT = (GRID_MID,GRID_MID-3)
NORTH1_LIGHT = (GRID_MID+1,GRID_MID-3)
NORTH2_LIGHT = (GRID_MID+2,GRID_MID-3)
NORTHRIGHT_LIGHT = (GRID_MID+3,GRID_MID-3)
SOUTH_LEFT_LIGHT = (GRID_MID,GRID_MID+3)
SOUTH1_LIGHT = (GRID_MID-1,GRID_MID+3)
SOUTH2_LIGHT = (GRID_MID-2,GRID_MID+3)
SOUTHRIGHT_LIGHT = (GRID_MID-3,GRID_MID+3)
EAST_LEFT_LIGHT = (GRID_MID-3,GRID_MID)
EAST1_LIGHT = (GRID_MID-3,GRID_MID-1)
EAST2_LIGHT = (GRID_MID-3,GRID_MID-2)
EASTRIGHT_LIGHT = (GRID_MID-3,GRID_MID-3)
WEST_LEFT_LIGHT = (GRID_MID+3,GRID_MID)
WEST1_LIGHT = (GRID_MID+3,GRID_MID+1)
WEST2_LIGHT = (GRID_MID+3,GRID_MID+2)
WESTRIGHT_LIGHT = (GRID_MID+3,GRID_MID+3)

# groups of lights that turn together
NORTH_LIGHTS = [NORTH1_LIGHT, NORTH2_LIGHT, NORTHRIGHT_LIGHT]
NORTH_LEFT_LIGHTS = [NORTH_LEFT_LIGHT]
SOUTH_LIGHTS = [SOUTH1_LIGHT, SOUTH2_LIGHT, SOUTHRIGHT_LIGHT]
SOUTH_LEFT_LIGHTS = [SOUTH_LEFT_LIGHT]
EAST_LIGHTS = [EAST1_LIGHT, EAST2_LIGHT, EASTRIGHT_LIGHT]
EAST_LEFT_LIGHTS = [EAST_LEFT_LIGHT]
WEST_LIGHTS = [WEST1_LIGHT, WEST2_LIGHT, WESTRIGHT_LIGHT]
WEST_LEFT_LIGHTS = [WEST_LEFT_LIGHT]

LIGHTS = NORTH_LIGHTS + NORTH_LEFT_LIGHTS + \
        SOUTH_LIGHTS + SOUTH_LEFT_LIGHTS + \
        EAST_LIGHTS + EAST_LEFT_LIGHTS + \
        WEST_LIGHTS + WEST_LEFT_LIGHTS

# these are in order:
LIGHT_STATES = [
        'NS_GREEN',
        'NS_YELLOW',
        'NS_ALL_RED', # waiting for intersection to clear
        'NS_LEFT_GREEN',
        'NS_LEFT_YELLOW',
        'EW_GREEN',
        'EW_YELLOW',
        'EW_ALL_RED', # waiting for intersection to clear
        'EW_LEFT_GREEN',
        'EW_LEFT_YELLOW',
        ]
# how long to remain in each state
LIGHT_STATE_DURATIONS = {
        'NS_GREEN': 8,
        'NS_YELLOW': 1,
        'NS_ALL_RED': 3,
        'NS_LEFT_GREEN': 4,
        'NS_LEFT_YELLOW': 1,
        'EW_GREEN': 8,
        'EW_YELLOW': 1,
        'EW_ALL_RED': 3,
        'EW_LEFT_GREEN': 4,
        'EW_LEFT_YELLOW': 1,
        }

# light color constants
RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'


# coordinate, direction pairs for where cars may enter the grid
NORTH_INITIALIZERS = [((GRID_MID+1,GRID_MIN-1), N),((GRID_MID+2,GRID_MIN-1), N), ((GRID_MID+3,GRID_MIN-1), N), ((GRID_MID,GRID_MIN-1), N)]
SOUTH_INITIALIZERS = [((GRID_MID-2,GRID_MAX), S),((GRID_MID-1,GRID_MAX), S), ((GRID_MID-3,GRID_MAX), S), ((GRID_MID,GRID_MAX), S)]
EAST_INITIALIZERS = [((GRID_MIN-1,GRID_MID-2), E), ((GRID_MIN-1,GRID_MID-1), E), ((GRID_MIN-1,GRID_MID-3), E), ((GRID_MIN-1,GRID_MID), E)]
WEST_INITIALIZERS = [((GRID_MAX,GRID_MID+1), W), ((GRID_MAX,GRID_MID+2), W), ((GRID_MAX,GRID_MID+3), W), ((GRID_MAX,GRID_MID), W)]

INITIALIZERS = NORTH_INITIALIZERS + SOUTH_INITIALIZERS + EAST_INITIALIZERS + WEST_INITIALIZERS

# definition of how cars move through the grid
# for a given coordinate and direction, defined the next direction
# this allows us to define direction changes for turn lanes
# most transitions will continue in the same direction, because the cars will
# typically continue in their lane
TRANSITIONS = defaultdict(dict)

# straight lane transitions
for coord in NORTHBOUND1 + NORTHBOUND2:
    TRANSITIONS[coord][N] = N # northbound continues northbound
for coord in SOUTHBOUND1 + SOUTHBOUND2:
    TRANSITIONS[coord][S] = S # southbound continues southbound
for coord in EASTBOUND1 + EASTBOUND2:
    TRANSITIONS[coord][E] = E # eastbount continues eastbount
for coord in WESTBOUND1 + WESTBOUND2:
    TRANSITIONS[coord][W] = W # westbount continues westbount
# right turn lane transitions
for coord in NORTHRIGHT:
    TRANSITIONS[coord][N] = N
TRANSITIONS[(GRID_MID+3,GRID_MID-2)][N] = E
for coord in SOUTHRIGHT:
    TRANSITIONS[coord][S] = S
TRANSITIONS[(GRID_MID-3,GRID_MID+2)][S] = W
for coord in EASTRIGHT:
    TRANSITIONS[coord][E] = E
TRANSITIONS[(GRID_MID-2,GRID_MID-3)][E] = S
for coord in WESTRIGHT:
    TRANSITIONS[coord][W] = W
TRANSITIONS[(GRID_MID+2,GRID_MID+3)][W] = N
# left turn lane transitions
# left turns go on the diagonal briefly to round the corner
# otherwise the left turns from opposite directions would collide
for coord in NORTHLEFT:
    TRANSITIONS[coord][N] = N
TRANSITIONS[(GRID_MID,GRID_MID-1)][N] = NW
TRANSITIONS[(GRID_MID-1,GRID_MID)][NW] = NW
TRANSITIONS[(GRID_MID-2,GRID_MID+1)][NW] = W
for coord in SOUTHLEFT:
    TRANSITIONS[coord][S] = S
TRANSITIONS[(GRID_MID,GRID_MID+1)][S] = SE
TRANSITIONS[(GRID_MID+1,GRID_MID)][SE] = SE
TRANSITIONS[(GRID_MID+2,GRID_MID-1)][SE] = E
for coord in EASTLEFT:
    TRANSITIONS[coord][E] = E
TRANSITIONS[(GRID_MID-1,GRID_MID)][E] = NE
TRANSITIONS[(GRID_MID,GRID_MID+1)][NE] = NE
TRANSITIONS[(GRID_MID+1,GRID_MID+2)][NE] = N
for coord in WESTLEFT:
    TRANSITIONS[coord][W] = W
TRANSITIONS[(GRID_MID+1,GRID_MID)][W] = SW
TRANSITIONS[(GRID_MID,GRID_MID-1)][SW] = SW
TRANSITIONS[(GRID_MID-1,GRID_MID-2)][SW] = S

# lights advance on a set pattern
class Lights:
    def __init__(self, light_state='NS_GREEN'):
        self.light_state = light_state
        self.light_state_counter = 0

    def is_light(self, coord):
        return coord in LIGHTS

    def get_light_value(self, coord):
        if self.light_state == 'NS_GREEN':
            if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
                return GREEN
        if self.light_state == 'NS_YELLOW':
            if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
                return YELLOW
        if self.light_state == 'NS_LEFT_GREEN':
            if coord in NORTH_LEFT_LIGHTS or coord in SOUTH_LEFT_LIGHTS:
                return GREEN
        if self.light_state == 'NS_LEFT_YELLOW':
            if coord in NORTH_LEFT_LIGHTS or coord in SOUTH_LEFT_LIGHTS:
                return YELLOW
        if self.light_state == 'EW_GREEN':
            if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
                return GREEN
        if self.light_state == 'EW_YELLOW':
            if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
                return YELLOW
        if self.light_state == 'EW_LEFT_GREEN':
            if coord in EAST_LEFT_LIGHTS or coord in WEST_LEFT_LIGHTS:
                return GREEN
        if self.light_state == 'EW_LEFT_YELLOW':
            if coord in EAST_LEFT_LIGHTS or coord in WEST_LEFT_LIGHTS:
                return YELLOW
        return RED if self.is_light(coord) else None

    def advance_lights(self):
        self.light_state_counter += 1
        if self.light_state_counter >= LIGHT_STATE_DURATIONS[self.light_state]:
            self.light_state_counter = 0
            self.light_state = LIGHT_STATES[(LIGHT_STATES.index(self.light_state)+1)%len(LIGHT_STATES)]

# the main model of the traffic intersection
class Traffic:
    def __init__(self):
        self.all_cars = []
        self.all_cars_by_coord = {}
        self.lights = Lights()

    # code for advancing and validating the cars
    def advance(self):
        self.lights.advance_lights()
        self._add_new_cars()
        for car in self.all_cars:
            if self._car_can_move(car):
                self.all_cars_by_coord.pop(car.coord)
                car.move()
                self.all_cars_by_coord[car.coord] = car
        self._remove_finished_cars()
        self._validate_cars()

    def add_car_by_hand(self, car):
        assert not self._is_occupied(car.coord)
        assert self._is_lane(car.coord)
        self._add_car(car)

    def _add_new_cars(self):
        # for now add one car per call
        entering_car = Car(*INITIALIZERS[random.randint(0, len(INITIALIZERS)-1)])
        if self._is_occupied(entering_car.coord):
            print 'CONGESTION at {}'.format(entering_car.coord)
        else:
            self._add_car(entering_car)

    def _add_car(self, car):
        self.all_cars.append(car)
        self.all_cars_by_coord[car.coord] = car

    def _remove_finished_cars(self):
        finished_cars = [car for car in self.all_cars if self._is_done(car)]
        self.all_cars[:] = [car for car in self.all_cars if not self._is_done(car)]
        for car in finished_cars:
            self.all_cars_by_coord.pop(car.coord)

    def _validate_cars(self):
        assert len(self.all_cars) == len(self.all_cars_by_coord.keys())
        for car in self.all_cars:
            assert self._is_lane(car.coord) or self._is_outside_grid(car.coord)
            assert not self._is_done(car)

    def _is_done(self, car):
        return self._is_outside_grid(car.coord)

    # grid drawing code:
    def print_grid(self):
        print('\x1b[2J')
        for row in range(GRID_MAX, GRID_MIN-2, -1):
            self._print_row(row)

    def _get_grid_background(self, coord):
        v = self.lights.get_light_value(coord)
        return 'on_red' if v == RED else 'on_yellow' if v == YELLOW else 'on_green' if self.lights.is_light(coord) else 'on_blue' if self._is_lane(coord) else None

    def _get_grid_char(self, coord):
        if self._is_outside_grid(coord):
            return colored('   ', 'white', 'on_white')
        car = self.all_cars_by_coord.get(coord, None)
        return colored(car.display_val if car else '   ', car.color if car else 'white', self._get_grid_background(coord))

    def _print_row(self, row_index):
        print ''.join([self._get_grid_char((col_index, row_index)) for col_index in range(GRID_MIN-1,GRID_MAX+1)])

    # helpers
    def _is_occupied(self, coord):
        return coord in self.all_cars_by_coord

    def _is_lane(self, coord):
        return coord in LANES

    def _is_outside_grid(self, coord):
        return coord[0] < GRID_MIN or coord[0] >= GRID_MAX or coord[1] < GRID_MIN or coord[1] >= GRID_MAX

    def _car_can_move(self, car):
        next_coord = car.next_coord()
        if self.lights.get_light_value(next_coord) == RED:
            return False
        if self._is_occupied(next_coord):
            return False
        return True


# a car is basically a coordinate and the current direction it is headed
class Car:
    def __init__(self, coord, direction):
        self.coord = coord
        self.direction = direction
        self.color = ['magenta', 'cyan', 'white'][random.randint(0,2)]
        self.display_val = ' {} '.format(['#', '*', 'O', '%', '$'][random.randint(0,4)])

    def next_coord(self):
        return (self.coord[0] + self.direction[0], self.coord[1] + self.direction[1])

    def move(self):
        self.coord = self.next_coord()
        self.direction = TRANSITIONS.get(self.coord, {}).get(self.direction, (0,0))


def main():
    print 'Traffic Model'
    traffic = Traffic()
    traffic.print_grid()
    key = ''
    while key != 'q':
        traffic.advance()
        traffic.print_grid()
        key = raw_input('Anything but q to advance:')
    print 'bubye'

if __name__ == "__main__":
    main()

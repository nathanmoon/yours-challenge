import random

from collections import defaultdict
from termcolor import cprint, colored

# directions
N = (0,1)
E = (1,0)
S = (0,-1)
W = (-1,0)
NW = (-1,1)
SE = (1,-1)

# grid size
GRID_MIN = 0
GRID_MAX = 13

GRID_RANGE = range(GRID_MIN, GRID_MAX)

# coordinates of the various lanes
NORTHBOUND1 = [(7,y) for y in GRID_RANGE]
NORTHBOUND2 = [(8,y) for y in GRID_RANGE]
SOUTHBOUND1 = [(5,y) for y in GRID_RANGE]
SOUTHBOUND2 = [(4,y) for y in GRID_RANGE]
WESTBOUND1 = [(x,7) for x in GRID_RANGE]
WESTBOUND2 = [(x,8) for x in GRID_RANGE]
EASTBOUND1 = [(x,4) for x in GRID_RANGE]
EASTBOUND2 = [(x,5) for x in GRID_RANGE]
NORTHRIGHT = [(9,y) for y in range(GRID_MIN,4)]
SOUTHRIGHT = [(3,y) for y in range(9,GRID_MAX)]
EASTRIGHT = [(x,3) for x in range(GRID_MIN,4)]
WESTRIGHT = [(x,9) for x in range(9,GRID_MAX)]
NORTHLEFT = [(6,y) for y in range(GRID_MIN,4)]
SOUTHLEFT = [(6,y) for y in range(9,GRID_MAX)]
EASTLEFT = [(x,6) for x in range(GRID_MIN,4)]
WESTLEFT = [(x,6) for x in range(9,GRID_MAX)]
MIDDLE = [(6,6)]

LANES = NORTHBOUND1 + NORTHBOUND2 + SOUTHBOUND1 + SOUTHBOUND2 + \
        EASTBOUND1 + EASTBOUND2 + WESTBOUND1 + WESTBOUND2 + \
        NORTHRIGHT + SOUTHRIGHT + EASTRIGHT + WESTRIGHT + \
        NORTHLEFT + SOUTHLEFT + EASTLEFT + WESTLEFT + \
        MIDDLE

# coordinates of the lights.
# basically the entry points into the intersection, for each lane
# a car may not move into a coordinate that is a red light
NORTH_LEFT_LIGHT = (6,3)
NORTH1_LIGHT = (7,3)
NORTH2_LIGHT = (8,3)
NORTHRIGHT_LIGHT = (9,3)
SOUTH_LEFT_LIGHT = (6,9)
SOUTH1_LIGHT = (5,9)
SOUTH2_LIGHT = (4,9)
SOUTHRIGHT_LIGHT = (3,9)
EAST_LEFT_LIGHT = (3,6)
EAST1_LIGHT = (3,5)
EAST2_LIGHT = (3,4)
EASTRIGHT_LIGHT = (3,3)
WEST_LEFT_LIGHT = (9,6)
WEST1_LIGHT = (9,7)
WEST2_LIGHT = (9,8)
WESTRIGHT_LIGHT = (9,9)

NORTH_LIGHTS = [NORTH_LEFT_LIGHT, NORTH1_LIGHT, NORTH2_LIGHT, NORTHRIGHT_LIGHT]
SOUTH_LIGHTS = [SOUTH_LEFT_LIGHT, SOUTH1_LIGHT, SOUTH2_LIGHT, SOUTHRIGHT_LIGHT]
EAST_LIGHTS = [EAST_LEFT_LIGHT, EAST1_LIGHT, EAST2_LIGHT, EASTRIGHT_LIGHT]
WEST_LIGHTS = [WEST_LEFT_LIGHT, WEST1_LIGHT, WEST2_LIGHT, WESTRIGHT_LIGHT]

LIGHTS = NORTH_LIGHTS + SOUTH_LIGHTS + EAST_LIGHTS + WEST_LIGHTS

NS_LIGHTS = NORTH_LIGHTS + SOUTH_LIGHTS
EW_LIGHTS = EAST_LIGHTS + WEST_LIGHTS

# these are in order:
LIGHT_STATES = [
        'NS_GREEN',
        'NS_YELLOW',
        'NS_ALL_RED', # waiting for intersection to clear
        'EW_GREEN',
        'EW_YELLOW',
        'EW_ALL_RED', # waiting for intersection to clear
        ]
# how long to remain in each state
LIGHT_STATE_DURATIONS = {
        'NS_GREEN': 8,
        'NS_YELLOW': 1,
        'NS_ALL_RED': 5,
        'EW_GREEN': 8,
        'EW_YELLOW': 1,
        'EW_ALL_RED': 5,
        }
light_state = 'NS_GREEN'
light_state_counter = 0

RED = 'red'
YELLOW = 'yellow'
GREEN = 'green'

def get_light_value(coord):
    global light_state
    if light_state == 'NS_GREEN':
        if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
            return GREEN
    if light_state == 'NS_YELLOW':
        if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
            return YELLOW
    if light_state == 'EW_GREEN':
        if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
            return GREEN
    if light_state == 'EW_YELLOW':
        if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
            return YELLOW
    return RED if is_light(coord) else None


# coordinate, direction pairs for where cars may enter the grid
NORTH_INITIALIZERS = [((7,-1), N),((8,-1), N)]
SOUTH_INITIALIZERS = [((4,13), S),((5,13), S)]
EAST_INITIALIZERS = [((-1,4), E), ((-1,5), E)]
WEST_INITIALIZERS = [((13,7), W), ((13,8), W)]

INITIALIZERS = NORTH_INITIALIZERS + SOUTH_INITIALIZERS + EAST_INITIALIZERS + WEST_INITIALIZERS

# definition of how cars move through the grid
# for a given coordinate and direction, defined the next direction
# this allows us to define direction changes for turn lanes
# most transitions will continue in the same direction, because the cars will
# typically continue in their lane
TRANSITIONS = defaultdict(dict)

for coord in NORTHBOUND1 + NORTHBOUND2:
    TRANSITIONS[coord][N] = N # northbound continues northbound
for coord in SOUTHBOUND1 + SOUTHBOUND2:
    TRANSITIONS[coord][S] = S # southbound continues southbound
for coord in EASTBOUND1 + EASTBOUND2:
    TRANSITIONS[coord][E] = E # eastbount continues eastbount
for coord in WESTBOUND1 + WESTBOUND2:
    TRANSITIONS[coord][W] = W # westbount continues westbount

# tracks all the cars on the grid
all_cars = []

# tracks all the cars by current coordinate
all_cars_set = set()

# a car is basically a coordinate and the current direction it is headed
class Car:
    def __init__(self, coord, direction):
        assert is_lane(coord) or is_outside_grid(coord)
        self.coord = coord
        self.direction = direction

    def next_coord(self):
        return (self.coord[0] + self.direction[0], self.coord[1] + self.direction[1])

    def can_move(self):
        next_coord = self.next_coord()
        if get_light_value(next_coord) == RED:
            return False
        if is_occupied(next_coord):
            return False
        return True

    def move(self):
        global all_cars
        if self.can_move():
            # clean this reference to all_cars_set up
            all_cars_set.remove(self.coord)
            self.coord = self.next_coord()
            self.direction = TRANSITIONS[self.coord][self.direction]
            all_cars_set.add(self.coord)

    def is_done(self):
        next_coord = self.next_coord()
        return is_outside_grid(next_coord)

# helpers
def is_occupied(coord):
    return coord in all_cars_set

def is_light(coord):
    return coord in LIGHTS

def is_lane(coord):
    return coord in LANES

def is_outside_grid(coord):
    return coord[0] < GRID_MIN or coord[0] >= GRID_MAX or coord[1] < GRID_MIN or coord[1] >= GRID_MAX


# grid drawing code:
def get_grid_background(coord):
    v = get_light_value(coord)
    return 'on_red' if v == RED else 'on_yellow' if v == YELLOW else 'on_green' if is_light(coord) else 'on_blue' if is_lane(coord) else None

def get_grid_char(coord):
    if is_outside_grid(coord):
        return colored('   ', 'white', 'on_white')
    return colored(' # ' if coord in all_cars_set else '   ', 'magenta', get_grid_background(coord))

def print_row(row_index):
    print ''.join([get_grid_char((col_index, row_index)) for col_index in range(GRID_MIN-1,GRID_MAX+1)])

def print_grid():
    print('\x1b[2J')
    for row in range(GRID_MAX, GRID_MIN-2, -1):
        print_row(row)


# code for advancing and validating the cars
def add_new_cars():
    # for now add one car per call
    global all_cars
    global all_cars_set
    entering_car = Car(*INITIALIZERS[random.randint(0, len(INITIALIZERS)-1)])
    if is_occupied(entering_car.coord):
        print 'CONGESTION at {}'.format(entering_car.coord)
    else:
        all_cars.append(entering_car)
        all_cars_set.add(entering_car.coord)

def advance_lights():
    global light_state
    global light_state_counter
    light_state_counter += 1
    if light_state_counter >= LIGHT_STATE_DURATIONS[light_state]:
        light_state_counter = 0
        light_state = LIGHT_STATES[(LIGHT_STATES.index(light_state)+1)%len(LIGHT_STATES)]

def advance():
    global all_cars
    global all_cars_set
    advance_lights()
    add_new_cars()
    for car in all_cars:
        car.move()
    finished_cars = [car for car in all_cars if car.is_done()]
    all_cars[:] = [car for car in all_cars if not car.is_done()]
    for car in finished_cars:
        all_cars_set.remove(car.coord)
    validate_cars()

def validate_cars():
    global all_cars
    global all_cars_set
    assert len(all_cars) == len(all_cars_set)
    for car in all_cars:
        assert is_lane(car.coord) or is_outside_grid(car.coord)
        assert not car.is_done()

def main():
    print 'Traffic Model'
    print_grid()
    key = ''
    while key != 'q':
        advance()
        print_grid()
        key = raw_input('Anything but q to advance:')
    print 'bubye'

if __name__ == "__main__":
    main()

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

GRID_RANGE = range(GRID_MIN, GRID_MAX)

GRID_MID = GRID_MAX // 2

# coordinates of the various lanes
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

NS_LIGHTS = NORTH_LIGHTS + SOUTH_LIGHTS
NS_LEFT_LIGHTS = NORTH_LEFT_LIGHTS + SOUTH_LEFT_LIGHTS
EW_LIGHTS = EAST_LIGHTS + WEST_LIGHTS
EW_LEFT_LIGHTS = EAST_LEFT_LIGHTS + WEST_LEFT_LIGHTS

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
        'NS_GREEN': GRID_MID+2,
        'NS_YELLOW': 1,
        'NS_ALL_RED': 3,
        'NS_LEFT_GREEN': 4,
        'NS_LEFT_YELLOW': 1,
        'EW_GREEN': GRID_MID+2,
        'EW_YELLOW': 1,
        'EW_ALL_RED': 3,
        'EW_LEFT_GREEN': 4,
        'EW_LEFT_YELLOW': 1,
        }
light_state = 'NS_GREEN'
light_state_counter = 0

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


# tracks all the cars on the grid
all_cars = []

# tracks all the cars by current coordinate
all_cars_by_coord = {}

# a car is basically a coordinate and the current direction it is headed
class Car:
    def __init__(self, coord, direction):
        assert is_lane(coord) or is_outside_grid(coord)
        self.coord = coord
        self.direction = direction
        self.color = ['magenta', 'cyan', 'white'][random.randint(0,2)]
        self.display_val = ' {} '.format(['#', '*', 'O', '%', '$'][random.randint(0,4)])

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
            # clean this reference to all_cars_by_coord up
            all_cars_by_coord.pop(self.coord)
            self.coord = self.next_coord()
            self.direction = TRANSITIONS.get(self.coord, {}).get(self.direction, (0,0))
            all_cars_by_coord[self.coord] = self

    def is_done(self):
        return is_outside_grid(self.coord)

# helpers
def is_occupied(coord):
    return coord in all_cars_by_coord

def is_light(coord):
    return coord in LIGHTS

def is_lane(coord):
    return coord in LANES

def is_outside_grid(coord):
    return coord[0] < GRID_MIN or coord[0] >= GRID_MAX or coord[1] < GRID_MIN or coord[1] >= GRID_MAX

def get_light_value(coord):
    global light_state
    if light_state == 'NS_GREEN':
        if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
            return GREEN
    if light_state == 'NS_YELLOW':
        if coord in NORTH_LIGHTS or coord in SOUTH_LIGHTS:
            return YELLOW
    if light_state == 'NS_LEFT_GREEN':
        if coord in NORTH_LEFT_LIGHTS or coord in SOUTH_LEFT_LIGHTS:
            return GREEN
    if light_state == 'NS_LEFT_YELLOW':
        if coord in NORTH_LEFT_LIGHTS or coord in SOUTH_LEFT_LIGHTS:
            return YELLOW
    if light_state == 'EW_GREEN':
        if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
            return GREEN
    if light_state == 'EW_YELLOW':
        if coord in EAST_LIGHTS or coord in WEST_LIGHTS:
            return YELLOW
    if light_state == 'EW_LEFT_GREEN':
        if coord in EAST_LEFT_LIGHTS or coord in WEST_LEFT_LIGHTS:
            return GREEN
    if light_state == 'EW_LEFT_YELLOW':
        if coord in EAST_LEFT_LIGHTS or coord in WEST_LEFT_LIGHTS:
            return YELLOW
    return RED if is_light(coord) else None


# grid drawing code:
def get_grid_background(coord):
    v = get_light_value(coord)
    return 'on_red' if v == RED else 'on_yellow' if v == YELLOW else 'on_green' if is_light(coord) else 'on_blue' if is_lane(coord) else None

def get_grid_char(coord):
    if is_outside_grid(coord):
        return colored('   ', 'white', 'on_white')
    car = all_cars_by_coord.get(coord, None)
    return colored(car.display_val if car else '   ', car.color if car else 'white', get_grid_background(coord))

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
    global all_cars_by_coord
    entering_car = Car(*INITIALIZERS[random.randint(0, len(INITIALIZERS)-1)])
    if is_occupied(entering_car.coord):
        print 'CONGESTION at {}'.format(entering_car.coord)
    else:
        all_cars.append(entering_car)
        all_cars_by_coord[entering_car.coord] = entering_car

def advance_lights():
    global light_state
    global light_state_counter
    light_state_counter += 1
    if light_state_counter >= LIGHT_STATE_DURATIONS[light_state]:
        light_state_counter = 0
        light_state = LIGHT_STATES[(LIGHT_STATES.index(light_state)+1)%len(LIGHT_STATES)]

def remove_finished_cars():
    global all_cars
    global all_cars_by_coord
    finished_cars = [car for car in all_cars if car.is_done()]
    all_cars[:] = [car for car in all_cars if not car.is_done()]
    for car in finished_cars:
        all_cars_by_coord.pop(car.coord)

def advance():
    global all_cars
    advance_lights()
    add_new_cars()
    for car in all_cars:
        car.move()
    remove_finished_cars()
    validate_cars()

def validate_cars():
    global all_cars
    global all_cars_by_coord
    assert len(all_cars) == len(all_cars_by_coord.keys())
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

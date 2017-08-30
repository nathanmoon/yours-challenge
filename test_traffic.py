from traffic import (all_cars, all_cars_set, Car, advance, is_occupied, is_light,
        is_red_light, red_lights, is_lane, is_outside_grid)

def test_is_occupied():
    all_cars_set.clear()
    all_cars_set.add((0,0))
    assert is_occupied((0,0))
    assert not is_occupied((1,1))

def test_is_light():
    assert is_light((4,9))
    assert not is_light((6,6))

def test_is_lane():
    assert is_lane((6,6))
    assert not is_lane((0,0))

def test_is_outside_grid():
    assert is_outside_grid((-1,0))
    assert not is_outside_grid((0,0))
    assert is_outside_grid((1,13))
    assert not is_outside_grid((12,12))

def test_is_red_light():
    red_lights[:] = []
    red_lights.append((0,0))
    assert is_red_light((0,0))
    assert not is_red_light((1,1))

def test_is_done():
    car = Car((8,12), (0,1))
    assert car.is_done()

def test_advance_removes_finished_cars():
    all_cars[:] = []
    all_cars_set.clear()
    car = Car((8,11), (0,1))
    all_cars.append(car)
    all_cars_set.add(car.coord)
    advance()
    assert len(all_cars) == 1
    assert len(all_cars_set) == 1


import pytest

from traffic import (all_cars, all_cars_by_coord, Car, advance, is_occupied, is_light,
        is_lane, is_outside_grid, GRID_MAX, GRID_MID, N)

def test_car_must_be_in_lane():
    with pytest.raises(Exception):
        Car((0,0), N)
    Car((GRID_MID,0), N)

def test_is_occupied():
    all_cars_by_coord.clear()
    all_cars_by_coord[(GRID_MID,0)] = Car((GRID_MID,0), N)
    assert is_occupied((GRID_MID,0))
    assert not is_occupied((GRID_MID,1))

def test_is_light():
    assert is_light((GRID_MID,GRID_MID-3))
    assert not is_light((GRID_MID,GRID_MID))

def test_is_lane():
    assert is_lane((GRID_MID,GRID_MID))
    assert not is_lane((0,0))

def test_is_outside_grid():
    assert is_outside_grid((-1,0))
    assert not is_outside_grid((0,0))
    assert is_outside_grid((1,GRID_MAX))
    assert not is_outside_grid((GRID_MAX-1,GRID_MAX-1))

def test_is_done():
    car = Car((GRID_MID+1,GRID_MAX), N)
    assert car.is_done()

def test_advance_removes_finished_cars():
    all_cars[:] = []
    all_cars_by_coord.clear()
    car = Car((GRID_MID+1,GRID_MAX-1), N)
    all_cars.append(car)
    all_cars_by_coord[car.coord] = car
    advance()
    assert len(all_cars) == 1
    assert len(all_cars_by_coord.keys()) == 1


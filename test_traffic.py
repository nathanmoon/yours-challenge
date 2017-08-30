import pytest

from traffic import (Car, Traffic, Lights, GRID_MAX, GRID_MID, N)

def test_car_must_be_in_lane():
    traffic = Traffic()
    with pytest.raises(Exception):
        traffic.add_car_by_hand(Car((0,0), N))
    traffic.add_car_by_hand(Car((GRID_MID,0), N))

def test_is_occupied():
    traffic = Traffic()
    car = Car((GRID_MID,0), N)
    traffic.add_car_by_hand(car)
    assert traffic._is_occupied((GRID_MID,0))
    assert not traffic._is_occupied((GRID_MID,1))

def test_is_light():
    lights = Lights()
    assert lights.is_light((GRID_MID,GRID_MID-3))
    assert not lights.is_light((GRID_MID,GRID_MID))

def test_is_lane():
    traffic = Traffic()
    assert traffic._is_lane((GRID_MID,GRID_MID))
    assert not traffic._is_lane((0,0))

def test_is_outside_grid():
    traffic = Traffic()
    assert traffic._is_outside_grid((-1,0))
    assert not traffic._is_outside_grid((0,0))
    assert traffic._is_outside_grid((1,GRID_MAX))
    assert not traffic._is_outside_grid((GRID_MAX-1,GRID_MAX-1))

def test_is_done():
    traffic = Traffic()
    car = Car((GRID_MID+1,GRID_MAX), N)
    assert traffic._is_done(car)

def test_advance_removes_finished_cars():
    traffic = Traffic()
    car = Car((GRID_MID+1,GRID_MAX-1), N)
    traffic.add_car_by_hand(car)
    traffic.advance()
    assert len(traffic.all_cars) == 1
    assert len(traffic.all_cars_by_coord.keys()) == 1


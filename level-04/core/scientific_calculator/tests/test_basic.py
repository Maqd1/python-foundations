import pytest
from calculator import basic


def test_add():
    assert basic.add(2, 3) == 5
    assert basic.add(-2, 2) == 0


def test_subtract():
    assert basic.subtract(5, 3) == 2


def test_multiply():
    assert basic.multiply(4, 3) == 12


def test_divide():
    assert basic.divide(10, 2) == 5


def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        basic.divide(5, 0)


def test_power():
    assert basic.power(2, 10) == 1024


def test_modulus():
    assert basic.modulus(10, 3) == 1


def test_modulus_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        basic.modulus(5, 0)


def test_floor_divide():
    assert basic.floor_divide(7, 2) == 3


def test_floor_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        basic.floor_divide(5, 0)

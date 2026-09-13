import math

import pytest
from calculator import scientific


def test_sqrt():
    assert scientific.sqrt(16) == 4


def test_sqrt_negative_raises():
    with pytest.raises(ValueError):
        scientific.sqrt(-1)


def test_log_default_base_10():
    assert scientific.log(100) == pytest.approx(2.0)


def test_ln():
    assert scientific.ln(math.e) == pytest.approx(1.0)


def test_sin_deg_matches_known_value():
    assert scientific.sin_deg(90) == pytest.approx(1.0)


def test_sin_radians_matches_known_value():
    assert scientific.sin(math.pi / 2) == pytest.approx(1.0)


def test_factorial():
    assert scientific.factorial(5) == 120


def test_factorial_negative_raises():
    with pytest.raises(ValueError):
        scientific.factorial(-3)


def test_pi_and_e_constants():
    assert scientific.pi() == pytest.approx(math.pi)
    assert scientific.e() == pytest.approx(math.e)

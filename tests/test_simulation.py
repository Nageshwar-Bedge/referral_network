# tests/test_simulation.py
import math
import pytest
from source.simulation import simulate_expected_cumulative, days_to_target, min_bonus_for_target

def test_simulate_expected_cumulative_edge():
    result = simulate_expected_cumulative(0, 10, 0.5, 5)
    assert all(x == 0 for x in result)

    result = simulate_expected_cumulative(10, 0, 0.5, 5)
    assert all(x == 0 for x in result)

def test_days_to_target_not_reached():
    d = days_to_target(100, 10, 0.0, 50)
    assert d is None

def test_min_bonus_early_return_and_rounding():
    def zero_prob(bonus):
        return 0.0

    assert min_bonus_for_target(10, 10, zero_prob) is None

    def prob(bonus):
        return min(0.99, 0.05 * bonus)

    bonus = min_bonus_for_target(30, 5, prob)
    assert bonus is not None
    assert bonus % 10 == 0

def test_min_bonus_rounding_up():
    def prob(bonus):
        if bonus < 23:
            return 0.0
        else:
            return 0.1

    bonus = min_bonus_for_target(10, 5, prob, initial_referrers=100, capacity=10, max_bonus=50)
    assert bonus is not None
    assert bonus % 10 == 0
    assert bonus >= 23

def test_simulate_and_days_existing():
    c = simulate_expected_cumulative(100, 10, 0.05, 30)
    assert c[-1] > 0
    d = days_to_target(100, 10, 0.05, 50)
    assert isinstance(d, int)

def test_min_bonus_existing():
    def adoption_prob_linear(bonus):
        return min(0.99, 0.01 * math.sqrt(bonus))
    b = min_bonus_for_target(30, 500, adoption_prob_linear)
    assert b is None or (b % 10 == 0)

def test_min_bonus_rounding_up_duplicate():
    def prob(bonus):
        if bonus < 23:
            return 0.0
        else:
            return 0.1

    bonus = min_bonus_for_target(10, 5, prob, initial_referrers=100, capacity=10, max_bonus=50)
    assert bonus is not None
    assert bonus % 10 == 0
    assert bonus >= 23
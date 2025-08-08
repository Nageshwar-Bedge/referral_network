# tests/test_analysis.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from source.analysis import analyze_results

def test_analyze_results_basic():
    data = [
        (1, "user1", 10.0),
        (1, "user2", 5.0),
        (2, "user1", 7.5),
        (2, "user3", 12.5),
        (3, "user2", 10.0),
    ]

    result = analyze_results(data)

    assert result["total_bonus_per_user"] == {
        "user1": 17.5,
        "user2": 15.0,
        "user3": 12.5,
    }

    expected_avg = (10.0 + 5.0 + 7.5 + 12.5 + 10.0) / 3
    assert result["average_daily_bonus"] == expected_avg

    top = result["top_referrers"]
    assert len(top) == 3
    assert top[0][0] == "user1" and top[0][1] == 17.5
    assert top[1][0] == "user2" and top[1][1] == 15.0
    assert top[2][0] == "user3" and top[2][1] == 12.5

def test_analyze_results_empty():
    result = analyze_results([])
    assert result["total_bonus_per_user"] == {}
    assert result["average_daily_bonus"] == 0  
    assert result["top_referrers"] == []

def test_analyze_results_zero_bonus():
    data = [(1, "user1", 0.0), (1, "user1", 0.0)]
    result = analyze_results(data)
    assert result["total_bonus_per_user"] == {"user1": 0.0}
    assert result["average_daily_bonus"] == 0.0
    assert result["top_referrers"] == [("user1", 0.0)]
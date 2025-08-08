# tests/test_visualization.py
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from source.visualization import plot_cumulative_bonus, plot_top_referrers

@pytest.fixture(autouse=True)
def mock_plt_show(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *args, **kwargs: None)

def test_plot_cumulative_bonus_runs():
    data = [
        (1, 'UserA', 10),
        (2, 'UserB', 15),
        (3, 'UserA', 20),
        (3, 'UserC', 5)
    ]
    plot_cumulative_bonus(data, show_plot=False)
    plot_cumulative_bonus(data, show_plot=True)

def test_plot_top_referrers_runs():
    analysis_results = {
        'top_referrers': [
            ('UserA', 100),
            ('UserB', 80),
            ('UserC', 50)
        ]
    }
    plot_top_referrers(analysis_results, show_plot=False)
    plot_top_referrers(analysis_results, show_plot=True)
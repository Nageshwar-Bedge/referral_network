# source/analysis.py
from collections import defaultdict

def analyze_results(simulation_data):
    """
    Analyze simulation results.

    Args:
        simulation_data (list): List of tuples (day, user_id, bonus)

    Returns:
        dict: Analysis results including total_bonus_per_user, average_daily_bonus, and top_referrers.
    """
    total_bonus_per_user = defaultdict(float)
    daily_totals = defaultdict(float)

    for day, user_id, bonus in simulation_data:
        total_bonus_per_user[user_id] += bonus
        daily_totals[day] += bonus

    if len(daily_totals) == 0:
        avg_daily_bonus = 0.0
    else:
        avg_daily_bonus = sum(daily_totals.values()) / len(daily_totals)

    top_referrers = sorted(total_bonus_per_user.items(), key=lambda x: x[1], reverse=True)

    return {
        "total_bonus_per_user": dict(total_bonus_per_user),
        "average_daily_bonus": avg_daily_bonus,
        "top_referrers": top_referrers[:5]
    }
# source/simulation.py
from typing import Callable, Optional, List

def simulate_expected_cumulative(initial_referrers: int, capacity: int, p: float, days: int) -> List[float]:
    cumulative = [0.0] * (days + 1)
    expected_active = float(initial_referrers)
    total_remaining_capacity = float(initial_referrers * capacity)

    for day in range(1, days + 1):
        if expected_active <= 0 or total_remaining_capacity <= 0:
            cumulative[day] = cumulative[day-1]
            continue
        expected_new = min(p * expected_active, total_remaining_capacity)
        cumulative[day] = cumulative[day-1] + expected_new
        total_remaining_capacity -= expected_new
        expected_active = initial_referrers * (total_remaining_capacity / (initial_referrers * capacity))
    return cumulative

def days_to_target(initial_referrers: int, capacity: int, p: float, target_total: float, max_days: int = 10_000) -> Optional[int]:
    cumulative = simulate_expected_cumulative(initial_referrers, capacity, p, max_days)
    for day, val in enumerate(cumulative):
        if val >= target_total:
            return day
    return None

def min_bonus_for_target(days: int, target_hires: int,
                         adoption_prob: Callable[[float], float],
                         eps: float = 1e-3,
                         initial_referrers: int = 100,
                         capacity: int = 10,
                         max_bonus: int = 100000) -> Optional[int]:

    lo, hi, best = 0, max_bonus, None
    if simulate_expected_cumulative(initial_referrers, capacity, adoption_prob(hi), days)[-1] < target_hires:
        return None

    while lo <= hi:
        mid = (lo + hi) // 2
        p_mid = adoption_prob(mid)
        cum = simulate_expected_cumulative(initial_referrers, capacity, p_mid, days)[-1]
        if cum + eps >= target_hires:
            best = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return best if best % 10 == 0 else ((best // 10) + 1) * 10
# main.py
from source.simulation import simulate_expected_cumulative, days_to_target, min_bonus_for_target
from source.analysis import analyze_results
from source.visualization import plot_cumulative_bonus, plot_top_referrers

def main():
    print("\n=== Mercor Referral Network Simulation ===")

    initial_referrals = int(input("Enter initial referrals: "))
    capacity = int(input("Enter capacity per referrer : "))
    days = int(input("Enter simulation days: "))
    referral_rate = float(input("Enter daily referral rate (0-1): "))

    if not (0 <= referral_rate <= 1):
        print("Error: Referral rate must be between 0 and 1.")
        return

    print("\n--- Simulation: Expected Cumulative Bonus ---")

    daily_totals = simulate_expected_cumulative(initial_referrals, capacity, referral_rate, days)

    for day, total in enumerate(daily_totals[1:], start=1):
        print(f"Day {day}: {total:.2f}")

    simulation_data = []
    prev = 0
    for day, cum_total in enumerate(daily_totals[1:], start=1):
        daily_bonus = cum_total - prev
        prev = cum_total
        simulation_data.append((day, "User1", daily_bonus))

    results = analyze_results(simulation_data)
    print(f"\nAverage daily bonus: ${results['average_daily_bonus']:.2f}")
    print("Top referrers:")
    for user, total_bonus in results['top_referrers']:
        print(f"  {user}: ${total_bonus:.2f}")

    plot_cumulative_bonus(simulation_data)
    plot_top_referrers(results)

    print("\n--- Target Analysis ---")
    target_amount = float(input("Enter target bonus amount: "))

    days_needed = days_to_target(initial_referrals, capacity, referral_rate, target_amount)
    print(f"Days to reach {target_amount}: {days_needed}")

    def adoption_prob(bonus):
        return min(0.99, 0.01 * bonus)

    min_bonus = min_bonus_for_target(
        days,
        target_amount,
        adoption_prob,
        initial_referrers=initial_referrals,
        capacity=capacity,
        max_bonus=10000
    )

    if min_bonus is None:
        print(f"Target not achievable with any bonus up to max limit")
    else:
        print(f"Minimum bonus needed to reach target in {days} days: ${min_bonus}")

if __name__ == "__main__":
    main()
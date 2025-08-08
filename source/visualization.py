# source/visualization.py
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_cumulative_bonus(simulation_data, show_plot=True):
    cumulative_by_day = defaultdict(float)
    for day, user, bonus in simulation_data:
        cumulative_by_day[day] += bonus

    days = sorted(cumulative_by_day.keys())
    cum_values = []
    total = 0
    for d in days:
        total += cumulative_by_day[d]
        cum_values.append(total)

    plt.figure(figsize=(10,6))
    plt.plot(days, cum_values, marker='o')
    plt.title("Cumulative Bonus Over Days")
    plt.xlabel("Day")
    plt.ylabel("Cumulative Bonus ($)")
    plt.grid(True)
    if show_plot:
        plt.show()
    plt.close()

def plot_top_referrers(analysis_results, show_plot=True):
    top = analysis_results.get('top_referrers', [])
    users = [u for u, b in top]
    bonuses = [b for u, b in top]

    plt.figure(figsize=(10,6))
    plt.bar(users, bonuses, color='skyblue')
    plt.title("Top Referrers by Total Bonus")
    plt.xlabel("User")
    plt.ylabel("Total Bonus ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    if show_plot:
        plt.show()
    plt.close()
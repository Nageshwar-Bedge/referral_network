# Mercor Referral Network Simulation

## Overview

This project simulates and analyzes a referral network with bonus incentives. It models the expected cumulative bonuses over time based on initial referrers, referral capacities, and daily referral rates. The project includes modules for:

- **Referral Network**: Core logic to manage referrals and prevent cycles.
- **Simulation**: Models expected cumulative bonuses and calculates minimum bonuses to achieve targets.
- **Analysis**: Aggregates simulation data and provides metrics like average bonuses and top referrers.
- **Visualization**: Generates plots for cumulative bonuses and top referrers.
- **Main Script**: Command-line interface to run simulations and view results interactively.
---

## Features

- Prevents invalid referrals such as self-referrals and cycles.
- Simulates daily cumulative bonus growth with capacity constraints.
- Calculates minimum bonus needed to reach a target within a given timeframe.
- Analyzes simulation data to highlight top performers.
- Visualizes results with clear charts.
- Fully tested with pytest for reliability.
---

## Language & Setup

- **Language:** Python 3.9+
- **Dependencies:** `pytest` for testing

### Setup Instructions

1. Create and activate a virtual environment:

- On **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- On **Linux/macOS**:
  ```bash
  python -m venv venv
  source venv/bin/activate
  ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
## Usage

Run the main simulation program:

   ```bash
   python main.py
   ```
- You will be prompted to enter:
- Initial number of referrers
- Capacity per referrer
- Simulation days
- Daily referral rate (0-1)
- Target bonus amount
- The program will simulate and display cumulative bonuses per day, average bonuses, top referrers, and calculate the minimum bonus required to hit your target.


## Testing
Run the full test suite using pytest:
```bash
pytest --cov=source --cov-report=term-missing
```
This will run all tests and show coverage reports for the source folder.


## Design Choices
  ### Data Structure
  - The referral network is represented as a directed graph using adjacency lists (dict[str, set[str]]) for efficient access and insertion.

  - A users set tracks all unique users in the network.

  - A parent dictionary enforces the rule that each candidate has exactly one referrer, ensuring uniqueness.

  - Sets in adjacency lists prevent duplicate referrals and speed up membership checks.

 ### API Design
  - add_user(user: str): Adds a new user to the network.

  - add_referral(referrer: str, candidate: str) -> bool: Adds a referral edge while enforcing constraints:

    - No self-referrals allowed.

    - Each candidate can have only one referrer.

    - Prevents cycles to maintain a Directed Acyclic Graph (DAG).

  - get_direct_referrals(user: str) -> List[str]: Returns sorted direct referrals of a user.

  - _reachable(src: str, dst: str) -> bool: Internal BFS to check if dst is reachable from src, used for cycle detection.

  - Additional methods provide analytics like total referral counts, top referrers, unique reach maximization, and centrality metrics.

## Folder Structure
```
├── main.py
├── README.md
├── requirements.txt
├── source
│   ├── analysis.py
│   ├── referral_network.py
│   ├── simulation.py
│   └── visualization.py
└── tests
    ├── test_analysis.py
    ├── test_referral_network.py
    ├── test_simulation.py
    └── test_visualization.py

```

## Dependencies
- Python 3.9+
- matplotlib
- pytest (for testing)

See requirements.txt for the full list.

## Approach and Time Spent

### Approach

To simulate and analyze the referral network with bonus incentives, I designed the system around a directed graph data structure representing users and their referrals. The core challenge was to prevent invalid referrals such as self-referrals and cycles, ensuring the network remains a Directed Acyclic Graph (DAG).

- **Referral Network Module**: Handles user addition, referral creation with constraints, and provides analytics like top referrers and reach.
- **Simulation Module**: Models the growth of cumulative bonuses over time using parameters like referral capacity and daily referral rate.
- **Analysis Module**: Aggregates simulation results to provide averages and insights.
- **Visualization Module**: Generates clear charts to visualize bonus growth and top performers.
- **Main Script**: Provides an interactive CLI for running simulations with user input.

I focused on modular design for easy maintenance and testing. The use of adjacency lists and sets ensured efficient lookup and cycle detection via BFS. The test suite comprehensively validates functionality, constraints, and edge cases to ensure robustness.

### Approximate Time Spent

- Project Planning & Design: 2 hours  
- Core Implementation (Referral Network, Simulation, Analysis, Visualization): 8 hours  
- Writing Tests & Validation: 3 hours  
- Documentation & Final Refinements: 1 hour
  
**Total Time:** Approximately 14 hours
---

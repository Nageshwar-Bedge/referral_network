# source/referral_network.py
from collections import deque, defaultdict
from typing import Dict, Set, List, Tuple

class ReferralNetwork:
    def __init__(self):
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        self.parent: Dict[str, str] = {}
        self.users: Set[str] = set()

    # ---------- Part 1 ----------
    def add_user(self, user: str) -> None:
        self.users.add(user)

    def add_referral(self, referrer: str, candidate: str) -> bool:
        self.add_user(referrer)
        self.add_user(candidate)

        if referrer == candidate:
            return False
        if candidate in self.parent:
            return False
        if self._reachable(candidate, referrer):
            return False

        self.adj[referrer].add(candidate)
        self.parent[candidate] = referrer
        return True

    def get_direct_referrals(self, user: str) -> List[str]:
        return sorted(list(self.adj.get(user, set())))

    def _reachable(self, src: str, dst: str) -> bool:
        if src == dst:
            return True
        seen = set()
        dq = deque([src])
        while dq:
            u = dq.popleft()
            seen.add(u)
            for v in self.adj.get(u, []):
                if v == dst:
                    return True
                dq.append(v)
        return False

    # ---------- Part 2 ----------
    def downstream_reach_set(self, user: str) -> Set[str]:
        """Return all direct + indirect referrals."""
        result = set()
        dq = deque([user])
        while dq:
            u = dq.popleft()
            for v in self.adj.get(u, []):
                if v not in result:
                    result.add(v)
                    dq.append(v)
        return result

    def total_referral_count(self, user: str) -> int:
        return len(self.downstream_reach_set(user))

    def top_k_by_reach(self, k: int) -> List[Tuple[str, int]]:
        counts = [(u, self.total_referral_count(u)) for u in self.users]
        counts.sort(key=lambda x: (-x[1], x[0]))
        return counts[:k]

    # ---------- Part 3 ----------
    def unique_reach_greedy(self, k: int) -> List[Tuple[str, int]]:
        """Greedy selection to maximize coverage."""
        reach_sets = {u: self.downstream_reach_set(u) for u in self.users}
        covered = set()
        selected = []
        for _ in range(min(k, len(self.users))):
            best_user, best_gain = None, -1
            for u, rset in reach_sets.items():
                gain = len(rset - covered)
                if gain > best_gain:
                    best_gain, best_user = gain, u
            if best_user is None or best_gain == 0:
                break
            selected.append((best_user, best_gain))
            covered |= reach_sets[best_user]
            del reach_sets[best_user]
        return selected

    def flow_centrality(self) -> List[Tuple[str, int]]:
        """Naive shortest-path betweenness-like measure."""
        users = list(self.users)
        dist = {s: {u: None for u in users} for s in users}

        # BFS for each source
        for s in users:
            dq = deque([s])
            dist[s][s] = 0
            while dq:
                u = dq.popleft()
                for v in self.adj.get(u, []):
                    if dist[s][v] is None:
                        dist[s][v] = dist[s][u] + 1
                        dq.append(v)

        score = {u: 0 for u in users}
        for s in users:
            for t in users:
                if s == t or dist[s][t] is None:
                    continue
                for v in users:
                    if v in (s, t) or dist[s][v] is None or dist[v][t] is None:
                        continue
                    if dist[s][v] + dist[v][t] == dist[s][t]:
                        score[v] += 1

        return sorted(score.items(), key=lambda x: (-x[1], x[0]))

    def summary(self) -> str:
        lines = ["Users:", ", ".join(sorted(self.users)), "Edges:"]
        for u in sorted(self.adj.keys()):
            lines.append(f"  {u} -> {', '.join(sorted(self.adj[u]))}")
        return "\n".join(lines)
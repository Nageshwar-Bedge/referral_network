# tests/test_referral_network.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from source.referral_network import ReferralNetwork

def test_add_and_constraints():
    net = ReferralNetwork()
    assert net.add_referral("A", "B")
    assert not net.add_referral("A", "A")
    assert not net.add_referral("C", "B")
    assert net.add_referral("B", "C")
    assert not net.add_referral("C", "A")

def test_reach_and_top_k():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("B", "C")
    net.add_referral("A", "D")
    assert net.total_referral_count("A") == 3
    top = net.top_k_by_reach(1)
    assert top[0][0] == "A" and top[0][1] == 3

def test_influencer_metrics():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("B", "C")
    net.add_referral("A", "D")
    net.add_referral("D", "E")
    assert isinstance(net.unique_reach_greedy(2), list)
    assert isinstance(net.flow_centrality(), list)

def test_self_referral_and_cycle():
    net = ReferralNetwork()
    assert net.add_referral("A", "B")
    assert not net.add_referral("B", "B")
    assert not net.add_referral("B", "A")

def test_get_direct_referrals_empty():
    net = ReferralNetwork()
    assert net.get_direct_referrals("NonExistentUser") == []

def test_downstream_reach_set_empty():
    net = ReferralNetwork()
    net.add_user("A")
    assert net.downstream_reach_set("A") == set()

def test_unique_reach_greedy_and_flow_centrality_edge():
    net = ReferralNetwork()
    net.add_user("A")
    assert net.unique_reach_greedy(1) == []
    assert net.flow_centrality() == [("A", 0)]

def test_summary_and_add_referral_branches():
    net = ReferralNetwork()
    assert net.add_referral("X", "Y")
    assert not net.add_referral("X", "X")
    assert not net.add_referral("Z", "Y")
    net.add_referral("Y", "Z")
    summary_str = net.summary()
    assert "Users:" in summary_str
    assert "Edges:" in summary_str
    assert "X -> Y" in summary_str
    assert "Y -> Z" in summary_str

def test_self_referral_explicit():
    net = ReferralNetwork()
    assert not net.add_referral("A", "A")

def test_unique_referrer_explicit():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    assert not net.add_referral("C", "B")

def test_self_referral_explicit_coverage():
    net = ReferralNetwork()
    assert not net.add_referral("User1", "User1")

def test_unique_referrer_explicit_coverage():
    net = ReferralNetwork()
    net.add_referral("User1", "User2")
    assert not net.add_referral("User3", "User2")

def test_self_referral_line_37():
    net = ReferralNetwork()
    assert net.add_referral("UserX", "UserX") is False

def test_unique_referrer_line_43():
    net = ReferralNetwork()
    net.add_referral("UserA", "UserB")
    assert net.add_referral("UserC", "UserB") is False

def test_reachable_src_equals_dst():
    net = ReferralNetwork()
    assert net._reachable("UserA", "UserA") is True

def test_reachable_with_seen_continue():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("B", "C")
    net.adj["C"].add("A")
    assert net._reachable("A", "C") is True

def test_reachable_line_43_seen_continue():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("B", "C")
    net.adj["C"].add("A")
    assert net._reachable("A", "C") is True

def test_reachable_line_43_covered():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("B", "C")
    net.adj["C"].add("A")
    assert net._reachable("A", "C") is True

def test_reachable_seen_node_continue():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    net.add_referral("A", "C")
    net.add_referral("B", "D")
    net.add_referral("C", "D")
    assert net._reachable("A", "D") is True

def test_unique_referrer_line_43():
    net = ReferralNetwork()
    net.add_referral("A", "B")
    assert not net.add_referral("C", "B")
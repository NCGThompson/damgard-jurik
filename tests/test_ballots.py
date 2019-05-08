#!/usr/bin/env python3
"""
test.py
Boucher, Govedič, Saowakon, Swanson 2019

Unit tests for ballots.

"""
import unittest

from cryptovote.ballots import Ballot, CandidateOrderBallot, FirstPreferenceBallot, CandidateEliminationBallot, \
    candidate_elimination_to_candidate_order, candidate_order_to_candidate_elimination, candidate_order_to_first_preference
from cryptovote.damgard_jurik import keygen, threshold_decrypt


class TestBallots(unittest.TestCase):
    def test_shuffle(self):
        lists = [
            [0, 1, 2, 3, 4, 5, 6],
            [10, 11, 12, 13, 14, 15, 16],
            ['0', '1', '2', '3', '4', '5', '6']
        ]

        # it is a random function so we must test it more than once

        for _ in range(5):
            result = Ballot.shuffle(lists[0], lists[1], lists[2])

            for i in range(3):
                l_r = result[i]
                l = lists[i]
                self.assertEqual(len(l_r), len(l), "Length of the outputted list must be the same")
                self.assertSetEqual(set(l_r), set(l), "The outputted list must still contain the same elements")

            expected_1 = [10 + i for i in result[0]]
            expected_2 = [str(i) for i in result[0]]

            self.assertEqual(result[1], expected_1,
                             "Elements in the second list must maintain their relative order to the first one")
            self.assertEqual(result[2], expected_2,
                             "Elements in the third list must maintain their relative order to the first one")


class TestCandidateOrderBallot(unittest.TestCase):
    def setUp(self):
        self.public_key, self.private_key_shares = keygen(n_bits=64, s=3, threshold=5, n_shares=9)

    def test_toFirstPreferenceBallot_01(self):

        candidates = [1, 2, 3]
        preferences = [3, 1, 2]
        weight = 1
        first_preferences = [0, weight, 0]

        ballot = CandidateOrderBallot(candidates[:], [self.public_key.encrypt(pref) for pref in preferences], self.public_key.encrypt(weight))

        result = candidate_order_to_first_preference(ballot, self.private_key_shares, self.public_key)

        self.assertIsInstance(result, FirstPreferenceBallot, "The returned ballot must be of type FirstPreferenceBallot")

        self.assertListEqual(result.candidates, candidates, "The candidates list must match")

        self.assertListEqual([threshold_decrypt(preference, self.private_key_shares) for preference in result.preferences], preferences, "The preferences list must match")

        self.assertListEqual([threshold_decrypt(weight, self.private_key_shares) for weight in result.weights], first_preferences, "The weights list must match")

    def test_toFirstPreferenceBallot_02(self):
        candidates = [0, 1, 2, 3, 4, 5]
        preferences = [1, 5, 0, 2, 4, 3]
        weight = 8
        first_preferences = [0, 0, weight, 0, 0, 0]

        ballot = CandidateOrderBallot(candidates[:], [self.public_key.encrypt(pref) for pref in preferences],
                                      self.public_key.encrypt(weight))

        result = candidate_order_to_first_preference(ballot, self.private_key_shares, self.public_key)

        self.assertIsInstance(result, FirstPreferenceBallot, "The returned ballot must be of type FirstPreferenceBallot")

        self.assertListEqual(result.candidates, candidates, "The candidates list must match")

        self.assertListEqual([threshold_decrypt(preference, self.private_key_shares) for preference in result.preferences], preferences, "The preferences list must match")

        self.assertListEqual([threshold_decrypt(weight, self.private_key_shares) for weight in result.weights], first_preferences, "The weights list must match")

    def test_toCandidateElimination_01(self):
        candidates = [1, 2, 3]
        preferences = [3, 1, 2]
        weight = 1
        eliminated = [0, 0, 1]
        post_eliminated = [0, 1, 0]
        
        ballot = CandidateOrderBallot(candidates[:], [self.public_key.encrypt(pref) for pref in preferences],
                                      self.public_key.encrypt(weight))

        result = candidate_order_to_candidate_elimination(ballot, eliminated, self.private_key_shares, self.public_key)

        self.assertIsInstance(result, CandidateEliminationBallot, "The returned ballot must be of type CandidateEliminationBallot")

        self.assertListEqual([threshold_decrypt(preference, self.private_key_shares) for preference in result.preferences], sorted(preferences), "The preferences list must match")

        self.assertListEqual([threshold_decrypt(eliminated_i, self.private_key_shares) for eliminated_i in result.eliminated], post_eliminated, "The eliminated list must match")

        self.assertEqual(threshold_decrypt(result.weight, self.private_key_shares), weight, "The weight must match")


class TestCandidateEliminationBallot(unittest.TestCase):
    def test_toCandidateOrderBallot_01(self):
        public_key, private_key_shares = keygen(n_bits=64, s=3, threshold=5, n_shares=9)

        candidates = [1, 2, 3]
        preferences = [3, 1, 2]
        weight = 1
        eliminated = [0, 0, 1]
        post_eliminated = [0, 1, 0]

        ballot = CandidateEliminationBallot([public_key.encrypt(cand) for cand in candidates], [public_key.encrypt(pref) for pref in preferences],[public_key.encrypt(elim) for elim in post_eliminated],
                                            public_key.encrypt(weight))

        result = candidate_elimination_to_candidate_order(ballot, private_key_shares)

        self.assertIsInstance(result, CandidateOrderBallot,
                              "The returned ballot must be of type CandidateOrderBallot")

        self.assertListEqual([threshold_decrypt(preference, private_key_shares) for preference in result.preferences], preferences)

        self.assertListEqual(result.candidates, candidates, "The candidates lists must match")

        self.assertEqual(threshold_decrypt(result.weight, private_key_shares), weight, "The weight must match")


if __name__ == '__main__':
    unittest.main(verbosity=3)

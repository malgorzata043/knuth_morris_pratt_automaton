"""Tests for the KMP automaton.

Run with: PYTHONPATH=src python -m unittest discover -s tests
"""

import unittest

from knuth_morris_pratt_automaton import KMPAutomaton


class TestConstruction(unittest.TestCase):
    def test_rejects_non_string_pattern(self):
        with self.assertRaises(TypeError):
            KMPAutomaton(123, "ab")

    def test_rejects_non_string_alphabet(self):
        with self.assertRaises(TypeError):
            KMPAutomaton("abc", ["a", "b", "c"])

    def test_rejects_duplicate_alphabet(self):
        with self.assertRaises(ValueError):
            KMPAutomaton("ab", "aab")

    def test_num_states(self):
        a = KMPAutomaton("abc", "abc")
        self.assertEqual(a.num_states, 4)

    def test_properties(self):
        a = KMPAutomaton("abc", "abc")
        self.assertEqual(a.pattern, "abc")
        self.assertEqual(a.alphabet, "abc")


class TestTransition(unittest.TestCase):
    def test_basic_transitions(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.transition(0, "a"), 1)
        self.assertEqual(a.transition(1, "b"), 2)
        self.assertEqual(a.transition(0, "b"), 0)
        self.assertEqual(a.transition(2, "a"), 2)

    def test_state_out_of_range(self):
        a = KMPAutomaton("ab", "ab")
        with self.assertRaises(ValueError):
            a.transition(-1, "a")
        with self.assertRaises(ValueError):
            a.transition(99, "a")

    def test_symbol_outside_alphabet_resets_to_zero(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.transition(1, "z"), 0)
        self.assertEqual(a.transition(2, "z"), 0)


class TestSearch(unittest.TestCase):
    def test_simple_match(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.search("ab"), [0])

    def test_no_match(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.search("ba"), [])

    def test_multiple_matches(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.search("ababab"), [0, 2, 4])

    def test_overlapping_matches(self):
        a = KMPAutomaton("aa", "a")
        self.assertEqual(a.search("aaaa"), [0, 1, 2])

    def test_full_text_match(self):
        a = KMPAutomaton("abc", "abc")
        self.assertEqual(a.search("abc"), [0])

    def test_rejects_non_string_text(self):
        a = KMPAutomaton("ab", "ab")
        with self.assertRaises(TypeError):
            a.search(123)


class TestEmptyPattern(unittest.TestCase):
    def test_empty_pattern_matches_every_position(self):
        a = KMPAutomaton("", "ab")
        self.assertEqual(a.search("ab"), [0, 1, 2])

    def test_empty_pattern_empty_text(self):
        a = KMPAutomaton("", "")
        self.assertEqual(a.search(""), [0])

    def test_empty_pattern_count(self):
        a = KMPAutomaton("", "ab")
        self.assertEqual(a.count("ab"), 3)

    def test_empty_pattern_contains(self):
        a = KMPAutomaton("", "ab")
        self.assertTrue(a.contains("ab"))


class TestCountAndContains(unittest.TestCase):
    def test_count(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.count("ababab"), 3)

    def test_count_zero(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.count("xxx"), 0)

    def test_contains_true(self):
        a = KMPAutomaton("abc", "abc")
        self.assertTrue(a.contains("xxabcxx"))

    def test_contains_false(self):
        a = KMPAutomaton("abc", "abc")
        self.assertFalse(a.contains("xxabxx"))


class TestCharactersOutsideAlphabet(unittest.TestCase):
    def test_outside_char_does_not_break_search(self):
        a = KMPAutomaton("ab", "ab")
        self.assertEqual(a.search("zabzabz"), [1, 4])

    def test_search_with_abc_alphabet(self):
        a = KMPAutomaton("abc", "abc")
        self.assertEqual(a.search("abcabc"), [0, 3])


class TestRepeatingPattern(unittest.TestCase):
    def test_self_overlapping_pattern(self):
        a = KMPAutomaton("aba", "ab")
        self.assertEqual(a.search("ababa"), [0, 2])

    def test_long_repeating(self):
        a = KMPAutomaton("aaa", "a")
        self.assertEqual(a.search("aaaaa"), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()

# knuth_morris_pratt_automaton

A deterministic string-matching automaton for a fixed pattern over a known alphabet. Preprocessing builds the full transition table in O(m·|Σ|) by simulating the KMP failure function, so scanning a text takes exactly one table lookup per character with no backtracking.

## Usage

```python
from knuth_morris_pratt_automaton import KMPAutomaton

auto = KMPAutomaton("ab", "ab")
print(auto.search("ababab"))  # [0, 2, 4]
print(auto.count("ababab"))   # 3
print(auto.contains("ba"))    # False

# Inspect a single transition (state 1, symbol 'b' -> accepting state 2)
print(auto.transition(1, "b"))  # 2
```

## Why this exists

Standard KMP scans the text with an on-the-fly failure function: each character may trigger several failure-link traversals (amortized O(1), but not constant per symbol). This library precomputes every `(state, symbol)` transition up front so the scan loop is a single array indexing per input character. The trade-off is memory: the table is `O(m·|Σ|)` where `Σ` is the alphabet you supply. Use this when you scan many texts against the same pattern and want predictable, branch-light scanning.

## Alphabet

The alphabet is an explicit string of distinct characters passed at construction. Characters in the text that are outside this alphabet always reset the automaton to state 0, because they cannot extend any prefix of the pattern. If a text may contain characters not in the pattern's own character set, include them in the alphabet (they get their own columns) or accept the reset behaviour.

## Edge cases

- An empty pattern matches at every position (indices 0..len(text) inclusive).
- Overlapping occurrences are reported: `KMPAutomaton("aa", "a").search("aaaa")` returns `[0, 1, 2]`.
- Passing a duplicate character in the alphabet raises `ValueError`.

## Running tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## API

- `KMPAutomaton(pattern: str, alphabet: str)` — construct the automaton.
- `.search(text: str) -> list[int]` — start indices of all (overlapping) occurrences.
- `.count(text: str) -> int` — number of occurrences.
- `.contains(text: str) -> bool` — whether the pattern occurs at least once.
- `.transition(state: int, symbol: str) -> int` — next state from `state` on `symbol`; symbols outside the alphabet return 0.
- `.pattern`, `.alphabet`, `.num_states` — read-only properties.

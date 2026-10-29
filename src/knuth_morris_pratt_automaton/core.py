from __future__ import annotations


class KMPAutomaton:
    __slots__ = ("_pattern", "_alphabet", "_symbol_index", "_trans", "_m")

    def __init__(self, pattern: str, alphabet: str) -> None:
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a str")
        if not isinstance(alphabet, str):
            raise TypeError("alphabet must be a str")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("alphabet must contain distinct characters")

        self._pattern = pattern
        self._alphabet = alphabet
        self._m = len(pattern)
        self._symbol_index = {ch: i for i, ch in enumerate(alphabet)}
        size = self._m + 1
        self._trans = [[0] * len(alphabet) for _ in range(size)]

        self._build()

    def _failure_function(self) -> list[int]:
        m = self._m
        pattern = self._pattern
        fail = [0] * m
        k = 0
        for i in range(1, m):
            while k > 0 and pattern[i] != pattern[k]:
                k = fail[k - 1]
            if pattern[i] == pattern[k]:
                k += 1
            fail[i] = k
        return fail

    def _build(self) -> None:
        pattern = self._pattern
        m = self._m
        alphabet = self._alphabet
        idx = self._symbol_index
        fail = self._failure_function()

        for q in range(m + 1):
            for c in alphabet:
                col = idx[c]
                if q == m:
                    self._trans[q][col] = m
                elif q < m and c == pattern[q]:
                    self._trans[q][col] = q + 1
                else:
                    if q == 0:
                        self._trans[q][col] = 0
                    else:
                        self._trans[q][col] = self._trans[fail[q - 1]][col]

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def alphabet(self) -> str:
        return self._alphabet

    @property
    def num_states(self) -> int:
        return self._m + 1

    def transition(self, state: int, symbol: str) -> int:
        if not 0 <= state <= self._m:
            raise ValueError("state out of range")
        col = self._symbol_index.get(symbol)
        if col is None:
            return 0
        return self._trans[state][col]

    def search(self, text: str) -> list[int]:
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        if self._m == 0:
            return list(range(len(text) + 1))

        trans = self._trans
        idx = self._symbol_index
        m = self._m
        state = 0
        out: list[int] = []
        for i, ch in enumerate(text):
            col = idx.get(ch)
            if col is not None:
                state = trans[state][col]
            else:
                state = 0
            if state == m:
                out.append(i - m + 1)
                state = fail_get(self, state, idx, trans)
        return out

    def count(self, text: str) -> int:
        return len(self.search(text))

    def contains(self, text: str) -> bool:
        if self._m == 0:
            return True
        if not isinstance(text, str):
            raise TypeError("text must be a str")
        trans = self._trans
        idx = self._symbol_index
        m = self._m
        state = 0
        for ch in text:
            col = idx.get(ch)
            if col is not None:
                state = trans[state][col]
            else:
                state = 0
            if state == m:
                return True
        return False


def fail_get(auto: KMPAutomaton, state: int, idx, trans) -> int:
    fail = auto._failure_function()
    return trans[fail[state - 1]][0] if fail and state > 0 else 0

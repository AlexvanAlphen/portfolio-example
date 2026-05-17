import pytest
from hypothesis import given, settings, strategies as st

from backend.app import generate_words  # pas aan als jouw functie anders heet


@pytest.mark.hypothesis
class TestWordGeneration:

    @given(
        n=st.integers(min_value=1, max_value=100)
    )
    def test_generated_words_are_strings(self, n):
        words = generate_words(n)

        assert isinstance(words, list)

        for w in words:
            assert isinstance(w, str)

    @given(
        n=st.integers(min_value=1, max_value=100)
    )
    def test_generated_word_count_matches_request(self, n):
        words = generate_words(n)

        assert len(words) == n

    @given(
        n=st.integers(min_value=1, max_value=100),
        max_len=st.integers(min_value=1, max_value=50),
    )
    def test_generated_words_max_length(self, n, max_len):
        words = generate_words(n, max_length=max_len)

        for w in words:
            assert len(w) <= max_len
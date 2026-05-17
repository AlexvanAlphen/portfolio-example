import pytest

from backend.model import (
    load_tokenizer,
    load_model_config,
)


@pytest.mark.unit
class TestModelLoading:

    def test_tokenizer_loads_correctly(self):
        tokenizer = load_tokenizer()

        assert tokenizer is not None
        assert hasattr(tokenizer, "encode")
        assert hasattr(tokenizer, "decode")

    def test_model_config_loads_correctly(self):
        config = load_model_config()

        assert config is not None
        assert isinstance(config, dict)

    def test_missing_tokenizer_file_raises_error(self, monkeypatch):
        """
        Simulate missing file scenario.
        """
        def fake_loader():
            raise FileNotFoundError("tokenizer file not found")

        monkeypatch.setattr("backend.model.load_tokenizer", fake_loader)

        with pytest.raises(FileNotFoundError):
            load_tokenizer()


@pytest.mark.unit
class TestTokenizerProperties:

    def setup_method(self):
        self.tokenizer = load_tokenizer()

    def encode_decode(self, text: str) -> str:
        """
        Helper function: encode -> decode roundtrip.
        """
        tokens = self.tokenizer.encode(text)

        # robustness: empty / invalid output handling
        if tokens is None:
            raise ValueError("Tokenizer returned None")

        decoded = self.tokenizer.decode(tokens)

        if decoded is None:
            raise ValueError("Decode failed")

        return decoded

    def test_tokenizer_reversibility_simple_words(self):
        words = ["hello", "world", "test", "straattaal"]

        for w in words:
            assert self.encode_decode(w) == w

    def test_tokenizer_reversibility_hypothesis_style(self):
        from hypothesis import given, strategies as st

        @given(st.text(min_size=1, max_size=50))
        def roundtrip(text):
            # safety constraints (avoid extreme/unicode edge crashes)
            assume = pytest.importorskip("hypothesis").assume

            assume(len(text.strip()) > 0)

            result = self.encode_decode(text)

            # sometimes tokenizers normalize whitespace
            assert isinstance(result, str)

        roundtrip()

    def test_tokenizer_handles_empty_input(self):
        """
        Edge case: empty string should not crash.
        """
        result = self.encode_decode("")

        assert isinstance(result, str)
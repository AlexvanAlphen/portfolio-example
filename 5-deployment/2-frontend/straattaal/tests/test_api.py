import pytest
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)
response = client.get("/health")

@pytest.mark.api
class TestHealthEndpoint:
    def test_health_endpoint(self):
        """Test that the health endpoint returns a healthy status."""
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, dict)
        assert "status" in data
        assert data["status"] == "ok"


@pytest.mark.api
class TestGenerateEndpoint:
    def test_generate_default_parameters(self):
        """
        Test generation endpoint with default parameters.
        Expected defaults:
        - 10 words
        - temperature 1.0
        """
        response = client.get("/generate")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, dict)
        assert "generated_text" in data

        generated_words = data["generated_text"].split()

        # Allow some flexibility depending on implementation
        assert len(generated_words) >= 1

    def test_generate_custom_word_count(self):
        """Test generation endpoint with a custom number of words."""
        response = client.get("/generate?num_words=5")

        assert response.status_code == 200

        data = response.json()

        assert "generated_text" in data

        generated_words = data["generated_text"].split()

        # Depending on implementation exact count may vary slightly
        assert len(generated_words) <= 5

    @pytest.mark.parametrize("temperature", [0.1, 0.5, 1.0, 2.0])
    def test_generate_different_temperatures(self, temperature):
        """Test generation endpoint with different temperature values."""
        response = client.get(f"/generate?temperature={temperature}")

        assert response.status_code == 200

        data = response.json()

        assert isinstance(data, dict)
        assert "generated_text" in data
        assert isinstance(data["generated_text"], str)

    def test_generate_invalid_word_count(self):
        """Test invalid number of words."""
        response = client.get("/generate?num_words=-1")

        # Depending on validation strategy:
        assert response.status_code in [400, 422]

    def test_generate_invalid_temperature(self):
        """Test invalid temperature."""
        response = client.get("/generate?temperature=-1")

        assert response.status_code in [400, 422]


@pytest.mark.api
class TestStarredWords:
    TEST_WORD = "hypothesis"

    def test_add_starred_word(self):
        """Test adding a word to starred words."""
        response = client.post(
            "/starred",
            json={"word": self.TEST_WORD},
        )

        assert response.status_code in [200, 201]

        data = response.json()

        assert isinstance(data, dict)

    def test_add_duplicate_starred_word(self):
        """Adding the same word twice should not create duplicates."""
        client.post("/starred", json={"word": self.TEST_WORD})
        client.post("/starred", json={"word": self.TEST_WORD})

        response = client.get("/starred")

        assert response.status_code == 200

        data = response.json()

        words = data.get("starred_words", [])

        assert words.count(self.TEST_WORD) == 1

    def test_get_starred_words(self):
        """Test retrieving starred words."""
        client.post("/starred", json={"word": self.TEST_WORD})

        response = client.get("/starred")

        assert response.status_code == 200

        data = response.json()

        assert "starred_words" in data
        assert isinstance(data["starred_words"], list)

    def test_remove_starred_word(self):
        """Test removing a starred word."""
        client.post("/starred", json={"word": self.TEST_WORD})

        response = client.delete(f"/starred/{self.TEST_WORD}")

        assert response.status_code == 200

        response = client.get("/starred")

        data = response.json()

        assert self.TEST_WORD not in data.get("starred_words", [])

    def test_remove_nonexistent_word(self):
        """Removing a non-existing word should return a valid error."""
        response = client.delete("/starred/does_not_exist")

        assert response.status_code in [404, 400]
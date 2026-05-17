import pytest
import requests


BASE_URL = "http://localhost:8000"


@pytest.mark.integration
class TestIntegrationWorkflow:

    def test_complete_workflow(self):
        # 1. Generate words
        gen_res = requests.get(f"{BASE_URL}/generate")
        assert gen_res.status_code == 200

        words = gen_res.json().get("generated_text", "").split()
        assert len(words) > 0

        word = words[0]

        # 2. Star a word
        star_res = requests.post(
            f"{BASE_URL}/starred",
            json={"word": word},
        )
        assert star_res.status_code in [200, 201]

        # 3. Verify starred list
        list_res = requests.get(f"{BASE_URL}/starred")
        assert list_res.status_code == 200

        starred = list_res.json().get("starred_words", [])
        assert word in starred

        # 4. Unstar word
        del_res = requests.delete(f"{BASE_URL}/starred/{word}")
        assert del_res.status_code == 200

        # 5. Verify removal
        list_res2 = requests.get(f"{BASE_URL}/starred")
        assert list_res2.status_code == 200

        starred2 = list_res2.json().get("starred_words", [])
        assert word not in starred2


@pytest.mark.integration
class TestIntegrationErrors:

    def test_invalid_generate_input(self):
        res = requests.get(f"{BASE_URL}/generate?num_words=-5")

        assert res.status_code in [400, 422]

    def test_invalid_starred_input(self):
        res = requests.post(
            f"{BASE_URL}/starred",
            json={"word": ""},
        )

        assert res.status_code in [400, 422]
# tests/conftest.py
import os
import pytest
@pytest.fixture(scope="session")
def api_config():
    return {
        # switch to another address
        "base_url": "https://api.wallester.com/v1", 
        "api_key": os.getenv("WALLESTER_API_KEY", "your_key_here"),
        "card_id": os.getenv("WALLESTER_CARD_ID", "your_card_id_here")
    }
import os
import importlib
import sys
from pathlib import Path
from fastapi.testclient import TestClient


def test_register_and_login(tmp_path):
    # Use a temporary database for isolation
    os.environ['DB_PATH'] = str(tmp_path / 'test.db')
    os.environ['SECRET_KEY'] = 'testsecret'

    # Ensure the backend package can be imported when running from repo root
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

    # Import the app after setting env vars so init_db uses the temp DB
    import backend.main as main
    importlib.reload(main)

    client = TestClient(main.app)

    # Register a new user
    register_resp = client.post('/register', json={'username': 'testuser', 'password': 'pw'})
    assert register_resp.status_code == 200

    # Request a token using the same credentials
    token_resp = client.post('/token', json={'username': 'testuser', 'password': 'pw'})
    assert token_resp.status_code == 200
    data = token_resp.json()
    assert data.get('access_token')

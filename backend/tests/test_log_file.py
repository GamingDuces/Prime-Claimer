import json
import importlib
from pathlib import Path


def test_log_claims(tmp_path, monkeypatch):
    monkeypatch.setenv('AMZ_LOGFILE', str(tmp_path/'log.json'))
    mod = importlib.reload(importlib.import_module('backend.claim_prime_gaming'))
    mod.log_claims('user@example.com', ['Game A'])
    data = json.loads(Path(tmp_path/'log.json').read_text())
    assert 'user@example.com' in data
    assert 'Game A' in data['user@example.com']


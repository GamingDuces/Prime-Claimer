import importlib

def test_module_loads():
    mod = importlib.import_module('backend.claim_prime_gaming')
    assert hasattr(mod, 'login')
    assert hasattr(mod, 'claim_games')

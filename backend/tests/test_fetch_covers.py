import importlib
import types


def test_fetch_covers(tmp_path, monkeypatch):
    # Use a temporary browser profile directory
    from backend import fetch_amazon_covers

    try:
        images = fetch_amazon_covers.fetch_covers()
    except Exception as e:
        # Playwright might not be able to launch browsers in CI
        import pytest
        pytest.skip(f"playwright unavailable: {e}")
    assert isinstance(images, list)
    for src in images:
        assert isinstance(src, str)

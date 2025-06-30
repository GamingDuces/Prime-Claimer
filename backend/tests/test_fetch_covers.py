import importlib
import types


def test_fetch_covers(tmp_path, monkeypatch):
    # Use a temporary browser profile directory
    from backend import fetch_amazon_covers

    try:
        images = fetch_amazon_covers.fetch_covers()
    except Exception as e:
        # Network or browser failures should not crash the test
        assert False, f"fetch_covers raised an exception: {e}"
    assert isinstance(images, list)
    for src in images:
        assert isinstance(src, str)

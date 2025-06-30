# Prime Claimer Backend

## Setup

1. `pip install -r requirements.txt`
   - für Tests zusätzlich `pip install httpx`
2. `.env.example` kopieren zu `.env`
3. `python -m playwright install`
4. `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --workers 4`

## Tests

Nach Installation der Abhängigkeiten können die Backend-Tests mit `pytest` ausgeführt werden:

```bash
pytest
```

Die Tests nutzen FastAPIs `TestClient` und benötigen keine weitere Konfiguration.
Am einfachsten lässt du sie aus dem Backend-Verzeichnis mit `pytest` laufen.

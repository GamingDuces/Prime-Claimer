# Prime Claimer Backend

## Setup

1. `pip install -r requirements.txt`
2. `.env.example` kopieren zu `.env`
3. `python -m playwright install`
4. `gunicorn -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 --workers 4`

Zusätzlich steht mit `claim_prime_gaming.py` ein kleines Skript zur Verfügung,
das wie im Projekt [free-games-claimer](https://github.com/vogler/free-games-claimer)
automatisch die aktuell kostenlosen Prime-Gaming-Spiele einlöst. Vor dem
Aufruf müssen die Umgebungsvariablen `AMZ_EMAIL` und `AMZ_PASSWORD` gesetzt
werden. Optional kann `AMZ_OTPKEY` für Zwei-Faktor-Logins genutzt werden.
Die Titel werden in `data/prime-gaming.json` gespeichert. Über `AMZ_NOTIFY`
kann eine [Apprise](https://github.com/caronc/apprise) URL gesetzt werden,
um nach erfolgreichen Claims Benachrichtigungen zu erhalten.

## Tests

Nach Installation der Abhängigkeiten können die Backend-Tests mit `pytest` ausgeführt werden:

```bash
pytest
```

Die Tests nutzen FastAPIs `TestClient` und benötigen keine weitere Konfiguration.

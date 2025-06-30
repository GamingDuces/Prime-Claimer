# Prime Claimer Discord Bot

## Setup

1. Bot im Discord Developer Portal erstellen und Token eintragen
2. `.env.example` kopieren zu `.env` und ausfüllen
3. `pip install -r requirements.txt`
4. `python bot.py`

Der Befehlsprefix des Bots kann über die Umgebungsvariable
`DISCORD_COMMAND_PREFIX` angepasst werden (Standard: `!`).

Um sich zu registrieren, nutzen Nutzer den Befehl `!registrieren`. Daraufhin
wird eine Anfrage an die in `DISCORD_ADMIN_IDS` hinterlegten Admins geschickt.
Erst nachdem einer der Admins den Befehl `!approve <user_id>` ausführt, wird der
Account erstellt und das zufällige Passwort per Direktnachricht verschickt.

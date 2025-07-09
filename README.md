# Prime Claimer

This repository contains the services that make up **Prime Claimer**, an automated tool to redeem Amazon Prime Gaming rewards.

## Components

- **[backend](backend/README.md):** FastAPI application providing the REST API and core logic.
- **[frontend](frontend/README.md):** React based web interface to interact with the service.
- **[discord-bot](discord-bot/README.md):** Bot that allows users to register and trigger claims via Discord.

## Running with Docker Compose

Create the required `.env` files by copying `backend/.env.example`, `discord-bot/.env.example` and the repository root `.env.example` to `.env` in their respective folders. Afterwards build and start the stack:

```bash
docker-compose build
docker-compose up
```

The backend will be available on port `8000` and the frontend on `5173`. For more information about each component, check their individual READMEs.

### Google Home and SmartThings Tokens

To enable notifications or automations with Google Home or Samsung SmartThings you need to provide API tokens in the root `.env` file.

1. **Google Home**
   - Visit the [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project and enable the *Home Graph API*
   - Create OAuth credentials for a desktop application and obtain a refresh token
   - Add the token to `GOOGLE_HOME_TOKEN` in your `.env`

2. **Samsung SmartThings**
   - Navigate to [SmartThings](https://account.smartthings.com/tokens) and log in
   - Generate a Personal Access Token with the required scopes (e.g. `devices`)
   - Add the token to `SMARTTHINGS_TOKEN` in your `.env`

After updating the environment file restart the containers so the applications can pick up the new tokens.

## Claim Script

The repository now contains a helper script to automatically claim the currently
free games from Prime Gaming. The script lives in
`backend/claim_prime_gaming.py` and uses Playwright similar to the approach from
[free-games-claimer](https://github.com/vogler/free-games-claimer).

Set your Amazon credentials via environment variables before running:

```bash
export AMZ_EMAIL="you@example.com"
export AMZ_PASSWORD="mypassword"
export AMZ_OTPKEY="BASE32SECRET"  # optional
python backend/claim_prime_gaming.py
```

The script logs in, claims available games and prints the titles of the claimed
offers. Claimed titles are stored in `data/prime-gaming.json`. Set `AMZ_NOTIFY`
to an [Apprise](https://github.com/caronc/apprise) URL to receive a notification
after claiming.

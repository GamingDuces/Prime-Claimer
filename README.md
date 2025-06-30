# Prime Claimer

This repository contains the services that make up **Prime Claimer**, an automated tool to redeem Amazon Prime Gaming rewards.

## Components

- **[backend](backend/README.md):** FastAPI application providing the REST API and core logic.
- **[frontend](frontend/README.md):** React based web interface to interact with the service.
- **[discord-bot](discord-bot/README.md):** Bot that allows users to register and trigger claims via Discord.

## Running with Docker Compose

Create the required `.env` files by copying `backend/.env.example` and `discord-bot/.env.example` to `.env` in their respective folders. Afterwards build and start the stack:

```bash
docker-compose build
docker-compose up
```

The backend will be available on port `8000` and the frontend on `5173`. For more information about each component, check their individual READMEs.

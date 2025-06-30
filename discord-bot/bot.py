import os
import discord
import requests
from discord.ext import commands, tasks
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
STATS_CHANNEL_ID = int(os.getenv("STATS_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Nutzer registrieren sich mit /registrieren
@bot.command(name="registrieren")
async def registrieren(ctx):
    user = ctx.author
    # Backend informieren
    res = requests.post(f"{BACKEND_URL}/register", json={
        "username": str(user),
        "password": "changeme123",  # In Realität sollte das sicher generiert/übermittelt werden!
        "email": f"{user.name}@discord"
    })
    if res.status_code == 200:
        await user.send("Dein Account wurde im Prime Claimer System angelegt! Nutze das Web-Interface für den Login.")
    else:
        await user.send("Registrierung fehlgeschlagen oder Account existiert bereits.")

# DM bei Session-Verfall/Statistiken
async def notify_user(user_id, message):
    user = await bot.fetch_user(user_id)
    if user:
        await user.send(message)

# Beispiel: einmal am Tag Statistik posten (kannst du anpassen)
@tasks.loop(hours=24)
async def weekly_stats():
    channel = bot.get_channel(STATS_CHANNEL_ID)
    if channel:
        res = requests.get(f"{BACKEND_URL}/admin/logs")  # z. B. Log-Analyse
        if res.status_code == 200:
            logs = res.json()
            await channel.send(f"Wöchentliche Statistiken: {len(logs)} Einträge.")
        else:
            await channel.send("Konnte keine Statistiken abrufen.")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} ist online!")
    weekly_stats.start()

if __name__ == "__main__":
    bot.run(TOKEN)
# This is a Discord bot that interacts with a backend service to manage user registrations and send notifications.
# It uses the discord.py library for bot functionality and requests for HTTP communication with the backend.
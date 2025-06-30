import os
import discord
import aiohttp
import secrets
from typing import Optional, Dict
from discord.ext import commands, tasks
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
STATS_CHANNEL_ID = int(os.getenv("STATS_CHANNEL_ID", "0"))
ADMIN_IDS = [int(x) for x in os.getenv("DISCORD_ADMIN_IDS", "").split(",") if x]

intents = discord.Intents.default()
intents.messages = True
intents.members = True
COMMAND_PREFIX = os.getenv("DISCORD_COMMAND_PREFIX", "!")
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

session: Optional[aiohttp.ClientSession] = None
pending_registrations: Dict[int, str] = {}

# Nutzer stellen eine Registrierungsanfrage mit /registrieren
@bot.command(name="registrieren")
async def registrieren(ctx):
    """Meldet eine Registrierungsanfrage an die Admins."""
    user = ctx.author
    if user.id in pending_registrations:
        await ctx.send("Deine Registrierungsanfrage wird bereits bearbeitet.")
        return

    pending_registrations[user.id] = str(user)
    await ctx.send("Registrierungsanfrage wurde an die Admins gesendet.")

    for admin_id in ADMIN_IDS:
        admin = await bot.fetch_user(admin_id)
        if admin:
            await admin.send(
                f"{user} möchte sich registrieren. "
                f"Bestätige mit `{COMMAND_PREFIX}approve {user.id}`."
            )

# Admins können eine Anfrage mit /approve <user_id> bestätigen
@bot.command(name="approve")
async def approve(ctx, user_id: int):
    """Legt den Nutzer im Backend an, wenn ein Admin zustimmt."""
    if ctx.author.id not in ADMIN_IDS:
        return

    if user_id not in pending_registrations:
        await ctx.send("Keine offene Registrierungsanfrage.")
        return

    user = await bot.fetch_user(user_id)
    if not user:
        await ctx.send("Benutzer nicht gefunden.")
        return

    global session
    if session is None:
        session = aiohttp.ClientSession()

    password = secrets.token_urlsafe(12)
    payload = {
        "username": str(user),
        "password": password,
        "email": f"{user.name}@discord"
    }

    try:
        async with session.post(f"{BACKEND_URL}/register", json=payload) as res:
            if res.status == 200:
                await user.send(
                    "Dein Account wurde im Prime Claimer System angelegt! "
                    f"Passwort: `{password}`"
                )
                await ctx.send(f"{user} wurde registriert.")
            else:
                await ctx.send("Registrierung fehlgeschlagen oder Account existiert bereits.")
    except aiohttp.ClientError:
        await ctx.send("Fehler bei der Registrierung.")
    finally:
        pending_registrations.pop(user_id, None)

# DM bei Session-Verfall/Statistiken
async def notify_user(user_id, message):
    user = await bot.fetch_user(user_id)
    if user:
        await user.send(message)

# Einfache Statusabfrage des Backends
@bot.command(name="status")
async def status(ctx):
    """Zeigt einen kurzen Debug-Status des Backends an."""
    global session
    if session is None:
        session = aiohttp.ClientSession()
    try:
        async with session.get(f"{BACKEND_URL}/admin/debug") as res:
            if res.status == 200:
                data = await res.json()
                text = "\n".join(f"{k}: {v}" for k, v in data.items())
                await ctx.send(f"Backend-Status:\n{text}")
            else:
                await ctx.send("Konnte Status nicht abrufen.")
    except aiohttp.ClientError:
        await ctx.send("Fehler beim Verbinden zum Backend.")

# Beispiel: einmal am Tag Statistik posten (kannst du anpassen)
@tasks.loop(hours=24)
async def weekly_stats():
    """Postet wöchentlich einfache Statistiken aus dem Backend."""
    global session
    if session is None:
        session = aiohttp.ClientSession()

    channel = bot.get_channel(STATS_CHANNEL_ID)
    if channel:
        try:
            async with session.get(f"{BACKEND_URL}/admin/logs") as res:
                if res.status == 200:
                    logs = await res.json()
                    await channel.send(
                        f"Wöchentliche Statistiken: {len(logs)} Einträge.")
                else:
                    await channel.send("Konnte keine Statistiken abrufen.")
        except aiohttp.ClientError:
            await channel.send("Fehler beim Abrufen der Statistiken.")

@bot.event
async def on_ready():
    global session
    if session is None:
        session = aiohttp.ClientSession()
    print(f"Bot {bot.user} ist online!")
    weekly_stats.start()

if __name__ == "__main__":
    bot.run(TOKEN)

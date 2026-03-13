import discord
import requests

# ── CONFIG ────────────────────────────────────────────────────────────────────
# Fill in your own tokens and IDs below.

# 1. Create a Discord bot at https://discord.com/developers/applications
#    → Bot → Token → Copy
DISCORD_TOKEN = "YOUR_DISCORD_BOT_TOKEN"

# 2. Create a Telegram bot via @BotFather, then message your bot and visit:
#    https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#    to find your chat_id.
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID   = "YOUR_TELEGRAM_CHAT_ID"

# 3. Right-click a Discord channel → Copy Channel ID.
#    Add as many as you want. Empty list = disabled.
MONITORED_CHANNELS = [
    # 123456789012345678,  # example-channel
]

# 4. Right-click a Discord user → Copy User ID.
#    These users will trigger alerts across ALL channels.
MONITORED_USERS = [
    # 123456789012345678,  # example-user
]

# ── TELEGRAM ──────────────────────────────────────────────────────────────────

def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

# ── MONITOR ───────────────────────────────────────────────────────────────────

class Monitor(discord.Client):

    async def on_ready(self):
        print(f"Monitoring as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        in_watched_channel = message.channel.id in MONITORED_CHANNELS
        is_watched_user    = message.author.id in MONITORED_USERS

        if not in_watched_channel and not is_watched_user:
            return

        content = message.content or "[no text — image/embed/file]"
        server  = message.guild.name if message.guild else "DM"

        alert = (
            f"Discord Alert\n"
            f"Server:  {server}\n"
            f"Channel: #{message.channel.name}\n"
            f"User:    {message.author.name}\n"
            f"──────────────────\n"
            f"{content}"
        )

        print(alert)
        send_telegram(alert)


Monitor().run(DISCORD_TOKEN)

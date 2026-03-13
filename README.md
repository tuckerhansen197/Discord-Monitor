# Discord → Telegram Monitor

Forwards messages from specific Discord channels (or users) to your Telegram chat in real time.

## Setup

### 1. Install dependencies

```bash
pip install discord.py requests
```

### 2. Create a Discord bot

1. Go to https://discord.com/developers/applications
2. Click **New Application** → give it a name → **Create**
3. Go to **Bot** → click **Reset Token** → copy the token
4. Under **Privileged Gateway Intents**, enable **Message Content Intent**
5. Go to **OAuth2 → URL Generator**, select **bot** scope, then select **Read Messages/View Channels** and **Read Message History** permissions
6. Copy the generated URL and open it in your browser to invite the bot to your server

### 3. Create a Telegram bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
2. Follow the prompts and copy the bot token
3. Message your new bot (send it anything)
4. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and find your `chat_id` in the response

### 4. Configure the script

Open `monitor.py` and fill in:

- `DISCORD_TOKEN` — your Discord bot token
- `TELEGRAM_BOT_TOKEN` — your Telegram bot token
- `TELEGRAM_CHAT_ID` — your Telegram chat ID
- `MONITORED_CHANNELS` — channel IDs to watch (right-click channel → Copy Channel ID)
- `MONITORED_USERS` — (optional) user IDs to watch across all channels

### 5. Run it

```bash
python monitor.py
```

You should see `Monitoring as <your bot name>` and start receiving Telegram alerts.

## Tips

- **Enable Developer Mode** in Discord (Settings → Advanced → Developer Mode) to copy channel/user IDs
- You can monitor as many channels and users as you want
- To run 24/7, host it on a cloud server (any cheap VPS works) or use `screen`/`tmux` to keep it running

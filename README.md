# Discord → Telegram Monitor

Forwards messages from specific Discord channels (or users) to your Telegram chat in real time.

## Setup

### 1. Install dependencies

```bash
pip install discord.py requests
```

### 2. Get your Discord token

This runs under your own Discord account — no bot needed. You just need your account token.

1. Open Discord in your **browser** (not the desktop app)
2. Press `F12` to open Developer Tools → go to the **Network** tab
3. Type anything in any Discord channel
4. In the Network tab, click on one of the requests to `discord.com`
5. Under **Request Headers**, find `Authorization` — that value is your token

> **Keep your token private.** Anyone with it can access your Discord account. Never share it or post it publicly.

### 3. Create a Telegram bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
2. Follow the prompts and copy the bot token
3. Message your new bot (send it anything)
4. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` and find your `chat_id` in the response

### 4. Configure the script

Open `monitor.py` and fill in:

- `DISCORD_TOKEN` — your Discord account token (from step 2)
- `TELEGRAM_BOT_TOKEN` — your Telegram bot token
- `TELEGRAM_CHAT_ID` — your Telegram chat ID
- `MONITORED_CHANNELS` — channel IDs to watch (right-click channel → Copy Channel ID)
- `MONITORED_USERS` — (optional) user IDs to watch across all channels

### 5. Run it

```bash
python monitor.py
```

You should see `Monitoring as <your Discord username>` and start receiving Telegram alerts.

## Hosting 24/7 (Oracle Cloud — Free Tier)

Oracle Cloud offers an always-free VM that's perfect for running this bot. Here's how to set it up.

### 1. Create an Oracle Cloud account

1. Go to https://www.oracle.com/cloud/free/ and sign up
2. You'll need a credit card for verification but the free tier won't charge you

### 2. Create a VM instance

1. In the Oracle Cloud dashboard, go to **Compute → Instances → Create Instance**
2. Change the image to **Ubuntu** (recommended)
3. Under **Shape**, pick the **Ampere A1** (ARM) shape — it's always-free
4. Download the SSH key pair when prompted (save the `.key` file somewhere safe)
5. Click **Create** and wait for the instance to be running
6. Copy the **Public IP Address** from the instance details

### 3. Connect to your server

```bash
# Make your key file secure
chmod 400 ~/path/to/your-key.key

# Connect (replace with your IP)
ssh -i ~/path/to/your-key.key ubuntu@YOUR_SERVER_IP
```

### 4. Install Python and dependencies

```bash
sudo apt update && sudo apt install -y python3 python3-pip
pip3 install discord.py requests
```

### 5. Upload the script

From your local machine (not the server):

```bash
scp -i ~/path/to/your-key.key monitor.py ubuntu@YOUR_SERVER_IP:~/monitor.py
```

Or just copy-paste the contents into a file on the server:

```bash
nano ~/monitor.py
# paste the configured script, then Ctrl+X → Y → Enter to save
```

### 6. Set up auto-start with systemd

This makes the bot start automatically on boot and restart if it crashes.

```bash
sudo nano /etc/systemd/system/discord-monitor.service
```

Paste the following:

```ini
[Unit]
Description=Discord Telegram Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Save the file (Ctrl+X → Y → Enter), then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable discord-monitor
sudo systemctl start discord-monitor
```

### 7. Verify it's running

```bash
# Check status
sudo systemctl status discord-monitor

# View live logs
sudo journalctl -u discord-monitor -f
```

### Useful commands

```bash
# Stop the bot
sudo systemctl stop discord-monitor

# Restart after editing monitor.py
sudo systemctl restart discord-monitor

# Check recent logs
sudo journalctl -u discord-monitor --since "1 hour ago"
```

## Tips

- **Enable Developer Mode** in Discord (Settings → Advanced → Developer Mode) to copy channel/user IDs
- You can monitor as many channels and users as you want
- The systemd service will auto-restart the bot if it crashes and start it on server reboot
- Oracle Cloud free tier VMs stay running indefinitely — no time limits

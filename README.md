# Discord backend for Errbot

This is the Discord backend for [Errbot](https://errbot.io).

## Quick Setup

### 1. Install the backend
Inside your Errbot directory (and your virtual environment), run:
```bash
pip install err-backend-discord
```

### 2. Create Discord App & Invite Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a **New Application**.
2. Go to the **Bot** tab, scroll to **Privileged Gateway Intents**, and toggle **ON**:
   - `SERVER MEMBERS INTENT`
   - `MESSAGE CONTENT INTENT`
3. Click **Reset Token** (or **Copy**) to get your bot token.
4. Invite the bot to your server using this URL template (replace `YOUR_CLIENT_ID` with the ID from the **General Information** tab):
   `https://discord.com/oauth2/authorize?scope=bot&permissions=0&client_id=YOUR_CLIENT_ID`

### 3. Basic Configuration
Add this to your `config.py`:
```python
BACKEND = 'Discord'

BOT_IDENTITY = {
    'token': 'YOUR_BOT_TOKEN_HERE',
    'initial_intents': 'default',
    'intents': ['members', 'message_content'],
}

BOT_ADMINS = ('@YourDiscordUsername',) # Note the @ prefix
```

### 4. Start Errbot
```bash
errbot
```

## Documentation

Visit the [official documentation](https://err-backend-discord.readthedocs.io/) where you'll find detailed information on:
 - Installation
 - Configuration
 - User Guide
 - Developer Guide

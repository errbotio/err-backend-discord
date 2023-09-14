# Discord backend for Errbot

This is the Discord backend for errbot.

## Quick Start

It is recommended to install errbot into a Python virtual environment.  The steps are as follows:
_Note: This example assume the virtual environment is created as `/opt/errbot` but you can adapt the path to your needs._

1. Create and activate the virtual environment.

```
python3 -m venv /opt/errbot
. /opt/errbot/bin/activate
```

2. Install errbot and slackv3.
```
pip install errbot[discord]
```

3. Initialise errbot.
```
errbot --init
```

4. Edit `config.py` to configure the backend with the correct Slack credentials. (See the official documentation of details on how to configure the backend for RTM vs Events)
```
BACKEND = "Discord"

BOT_IDENTITY = {
    "token": "xxxxxxxxxxxxxxxxxxxxxxxx.xxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxx_I",
    "initial_intents": "default",
    "intents": ["members", "-presences", "message_content"]
}
```

5. Start errbot
```
errbot -c config.py
```

# Documentation

Visit the [official documentation](https://err-backend-discord.readthedocs.io/) where you'll find information on the following topics:
 - Installation
 - Configuration
 - User Guide
 - Developer Guide

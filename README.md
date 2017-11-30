[![Updates](https://pyup.io/repos/github/gbin/err-backend-discord/shield.svg)](https://pyup.io/repos/github/gbin/err-backend-discord/)

This is a backend for Discord (http://discordapp.com) for errbot (http://errbot.io).

It allows you to use errbot from Discord but it is a work in progress.

**This project is in need of a regular user of Discord familiar with Python to take it under his/her wing!**

It is Python 3.4+ only.

## Installation

```
git clone https://github.com/gbin/err-backend-discord.git
```

and add:

```
BACKEND = 'Discord'
BOT_EXTRA_BACKEND_DIR = '/path_to/err-backend-discord'
```

to your `config.py`

## Authentication

Create an application, then a bot user and you can directly use the token of the bot user in your `config.py`:

```
BOT_IDENTITY = {
    'token' : 'changeme'
}
```

For further information about getting a bot user into a server please see: https://discordapp.com/developers/docs/topics/oauth2. You can use [this tool](https://discordapi.com/permissions.html) to generate a proper invitation link.


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

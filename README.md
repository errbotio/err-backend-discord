This is a backend for Discord (http://discordapp.com) for errbot (http://errbot.io).

It allows you to use errbot from Discord but it is a work in progress.

**This project is in need of a regular user of Discord familiar with Python to take it under his/her wing!**

It is Python 3.4+ only.

## Installation

```
git checkout https://github.com/gbin/err-backend-discord.git
```

and add:

```
BACKEND = 'Discord'
BOT_EXTRA_BACKEND_DIR = '/path_to/err-backend-discord'
```

to your config.py

## Authentication

Create a bot user then you can directly user the email and password of the bot user.

```
BOT_IDENTITY = {
    'email' : 'bot@domaine.tld'
    'password' : 'changeme'
}
```

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

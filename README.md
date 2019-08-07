# Errbot - Discord

This is a [Discord](http://discordapp.com) back-end for [Errbot](http://errbot.io).  It allows you to use errbot from Discord to execute commands.
[![Updates](https://pyup.io/repos/github/gbin/err-backend-discord/shield.svg)](https://pyup.io/repos/github/gbin/err-backend-discord/)

**This project is currently under development!**
Active progress is being made under the `development` branch and will be merged to `master` once it is stable.  You are welcome to try the development branch to help test and report any issues encountered with it.

## Installation
An errbot instance is required to install the discord back-end.  See the errbot installation [documentation](http://errbot.io/en/latest/user_guide/setup.html#option-2-installing-errbot-in-a-virtualenv-preferred) for details.

### Requirements
 * Python 3.6 or later
 * Discord.py 1.2.3 or later

### Virtual Environment
The steps below are to install the discord back-end in errbot's virtual environment.  In the examples below, the virtual environment was set to `/opt/errbot/virtualenv` and errbot initialised in `/opt/errbot`.  The "extra" back-end directory is set to `/opt/errbot/backend`.


1. If not already set, set errbot's `BOT_EXTRA_BACKEND_DIR` variable in `/opt/errbot/config.py` to the directory you will use to place additional back-ends.
```
BOT_EXTRA_BACKEND_DIR=/opt/errbot/backend
```
2. Set the back-end to use `Discord`.
```
BACKEND = 'Discord'
```
3. Clone repository to your errbot back-end directory.
```
cd /opt/errbot/backend
git clone https://github.com/gbin/err-backend-discord.git
```
4. Install back-end dependencies (errbot's virtual environment must be activated to install the dependencies into it).
```
source /opt/errbot/virtualenv/bin/activate
cd err-backend-discord
pip install -r requirements.txt
deactivate
```
5. Set the bot's token (see _Create a discord application_ for information on how to get the token).
```
BOT_IDENTITY = {
 'token' : 'changeme'
}
```

## Create a discord application
For further information about getting a bot user into a server please see: https://discordapp.com/developers/docs/topics/oauth2. You can use [this tool](https://discordapi.com/permissions.html) to generate a proper invitation link.
The reactiflux community have written a quick start guide to [creating a discord bot and getting a token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

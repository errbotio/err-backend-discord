.. _configuration:

Configuration
========================================================================

Errbot
------------------------------------------------------------------------

The configuration requirements for the Discord backend are quite simple.  Set the ``BACKEND`` to ``Discord`` and fill in ``BOT_IDENTITY`` dictionary with the discord token in the ``token`` key.
::

    BACKEND = "Discord"

    BOT_IDENTITY = {
        'token' : '<token_provided_from_discord_web_interface>'
    }



Discord
------------------------------------------------------------------------

Discord API terms of use can evolve at any point in time.  Fortunately, the team that provides the ``discord`` module does a great job at insulating errbot
from a lot of these subtle changes.  However, there are changes that are significant enough to require extra steps to get errbot to work as desired with discord.

Gateway Intents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enable **Server members intent** for your bot on the Discord website.  See `privileged-intents <https://discordpy.readthedocs.io/en/latest/intents.html?highlight=intents#privileged-intents>`_ page for the required steps.

Discord application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a bot user accouont for use with errbot, you can see the required permission settings in the `oauth2 <https://discordapp.com/developers/docs/topics/oauth2>`_ page.

Discord provides a `tool <https://discordapi.com/permissions.html>`_ that can be used to generate a proper invitation link.

The reactiflux community have written a quick start guide to `creating a discord bot and getting a token <https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token>`_

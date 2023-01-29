.. _user_guide:

User Guide
========================================================================

Message destination (User, Channel and Guild)
------------------------------------------------------------------------

Communication with a specific person or group of people requires a method to express the
destination for a message.  Security mechanisms also require a method to express people and groups
in a non ambiguous way also.

Person
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Human to human communication is performed by a special format: ``username`` followed a ``#`` and 4 digits.
This format is not used by the discord API, which uses 18+ digit identification.
::

        <@userid>                      -> Person
        @user#discriminator            -> Person

Channel
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Channel communication is expressed as a hash ``#`` followed by the channel name.  The format is not
used by the discord API, which uses an 18+ digit identificaiton.  An aspect of channel communication that is
not directy exposed thought the discord API, is when the bot operates in multiple servers a.k.a. guilds.  It
is possible that a channel name is not unique between multiple servers, e.g. ``#general`` can exist on server1
and server2, but the bot must be able to target the correct channel.  The format that the discord backend has
opted to use is the double ``#``.

::

        <#channelid>                   -> Room
        #channel                       -> Room (a uniquely identified channel on any guild)
        #channel#guild_id              -> Room (a channel on a specific guild)

Guild
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not available.  Such a target will probably not be supported in the future.


Troubleshooting
------------------------------------------------------------------------

privileged intents not explicitly enabled in the developer portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal.  It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page.  If this is not possible, then consider disabling the privileged intents instead.

This is caused by a mismatch between the intents requested by errbot-backend-discord and the Discord application intent settings.  Give the application the permissions it needs or disable them in the configuration.

failed to lookup user
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    ValueError: Failed to get the user <18_digit_id>

This error can be caused when the bot has not been allowed access to the ``member`` privileged intent.

Bot ignores all messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When running with debug logs enable, it's possible to see the message event received from Discord.  The event field ``content`` is empty.

::

    17:27:06 DEBUG    discord.gateway           For Shard ID None: WebSocket Event: { "t": "MESSAGE_CREATE", <snip>... "content": "", <snip>... }}

This indicates the bot has not been allowed access to the ``message_content`` privileged intent.


Acknowledgements
------------------------------------------------------------------------

This backend uses the `python-discord <https://pypi.org/project/python-discord/>`_ module.  We are most grateful to the dedicated and talented team that provide such a top class project.

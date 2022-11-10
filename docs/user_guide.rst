.. _user_guide:

User Guide
========================================================================



Troubleshooting
------------------------------------------------------------------------

privileged intents not explicitly enabled in the developer portal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    discord.errors.PrivilegedIntentsRequired: Shard ID None is requesting privileged intents that have not been explicitly enabled in the developer portal. It is recommended to go to https://discord.com/developers/applications/ and explicitly enable the privileged intents within your application's page. If this is not possible, then consider disabling the privileged intents instead.

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

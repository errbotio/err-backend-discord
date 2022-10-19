.. _installation:

Installation
========================================================================

Requirements
------------------------------------------------------------------------

 * Python 3.7 or later
 * Discord.py 1.7.3 or later
 
Python Virtual Environment
------------------------------------------------------------------------

The following steps describe how to install errbot and the discord backend into an isolated python virtual environment.

These instructions assume you have access to discord with a bot account configured.  For information on how to setup the bot account see https://discordpy.readthedocs.io/en/stable/discord.html

    1. Create a virtual environment for errbot.
    ::

        python3 -m venv <path_to_virtualenv>
        source <path_to_virtualenv>/bin/activate

    2. Install errbot and discord backend.
    ::

        pip install errbot err-backend-discord

    3. Initialise errbot and configure discord.
    ::

        errbot --init

    4. See the :ref:`configuration` section for configuration details.

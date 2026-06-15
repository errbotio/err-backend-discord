.. _bot_creation:

Creating a Discord Bot
========================================================================

To use Errbot with Discord, you need to create a Discord Application and a Bot user. Follow these steps to get your token and set up your bot correctly.

1. Create a Discord Application
-------------------------------

1. Log in to the `Discord Developer Portal <https://discord.com/developers/applications>`_.
2. Click the **New Application** button in the top right.
3. Give your application a name and click **Create**.

2. Set Up a Bot User
--------------------

1. On the left sidebar, click on the **Bot** tab.
2. Scroll down to the **Privileged Gateway Intents** section.
3. Toggle **ON** the following intents:
    *   **Server Members Intent**: Required for Errbot to look up members in a guild.
    *   **Message Content Intent**: **CRITICAL**. Required for Errbot to see and process commands.
4. Click **Save Changes**.

3. Get Your Bot Token
---------------------

1. Still on the **Bot** tab, find the **Token** section.
2. Click **Reset Token** (or **Copy** if it's already visible) to get your bot's secret token.
3. **Keep this token safe!** Do not share it or commit it to version control.

4. Invite Your Bot to Your Server (Quick Start)
-----------------------------------------------

To invite your bot to a server you manage without pre-configuring complex permissions, follow these steps:

1. Get your **Client ID** from the **General Information** tab of your application in the Developer Portal.
2. Use the following URL template, replacing ``YOUR_CLIENT_ID_HERE`` with your actual Client ID:

   ``https://discord.com/oauth2/authorize?scope=bot&permissions=0&client_id=YOUR_CLIENT_ID_HERE``

3. Paste the completed URL into your browser.
4. Select the server you want to add the bot to and click **Authorize**.

External Resources
------------------

For a more detailed guide with screenshots, you can also refer to the Reactiflux community's wiki:
`Creating a discord bot and getting a token <https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token>`_

import json
import logging
import os
import pdb
import sys
from tempfile import mkdtemp

import pytest
from errbot.backends.base import Message
from errbot.bootstrap import bot_config_defaults
from mock import MagicMock

from err_backend_discord.discordlib.room import DiscordRoom

log = logging.getLogger(__name__)

try:
    from err_backend_discord import DiscordBackend

    class MockedDiscordBackend(DiscordBackend):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.test_msgs = []
            self.bot_identifier = MagicMock()

except SystemExit:
    log.exception("Can't import discord backend for testing")


@pytest.fixture
def backend():
    # make up a config.
    tempdir = mkdtemp()
    # reset the config every time
    sys.modules.pop("errbot.config-template", None)
    __import__("errbot.config-template")
    config = sys.modules["errbot.config-template"]
    bot_config_defaults(config)
    config.BOT_DATA_DIR = tempdir
    config.BOT_LOG_FILE = os.path.join(tempdir, "log.txt")
    config.BOT_EXTRA_PLUGIN_DIR = []
    config.BOT_LOG_LEVEL = logging.DEBUG
    config.BOT_IDENTITY = BOT_IDENTITY = {
        "token": "token_abcd",
        "initial_intents": "default",
        "intents": [],
    }
    config.BOT_ASYNC = False
    config.BOT_PREFIX = "!"
    config.CHATROOM_FN = "test_room"

    discord_backend = MockedDiscordBackend(config)
    return discord_backend


def todo_build_identifier(backend):
    raise NotImplementedError


def todo_extract_identifiers(backend):
    raise NotImplementedError


def todo_send_message(backend):
    raise NotImplementedError

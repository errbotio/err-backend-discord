import json
import logging
import os
import sys

from errbot.backends.base import RoomDoesNotExistError

import pytest
from mock import MagicMock

from discordlib.person import DiscordPerson

log = logging.getLogger(__name__)


@pytest.fixture
def person():
    return MagicMock()


def test_wrong_userid():
    raise NotImplementedError


def test_create_person_without_args():
    DiscordPerson(user_id="0123456789012345678")


def test_create_person_with_username_only():
    DiscordPerson(username="someone")


def test_create_person_with_discriminator_only():
    DiscordPerson(discriminator="#1234")


def test_create_person_with_id():
    DiscordPerson(user_id="0123456789012345678")


def test_create_person_username_and_discriminator():
    DiscordPerson(username="someone", discriminator="1234")


def test_wrong_channelid():
    raise NotImplementedError


def test_username():
    raise NotImplementedError


def test_username_not_found():
    raise NotImplementedError


def test_fullname():
    raise NotImplementedError


def test_fullname_not_found():
    raise NotImplementedError


def test_email():
    raise NotImplementedError


def test_email_not_found():
    raise NotImplementedError


def test_channelname():
    raise NotImplementedError


def test_channelname_channel_not_found():
    raise NotImplementedError


def test_domain():
    raise NotImplementedError


def test_aclattr():
    raise NotImplementedError


def test_person():
    raise NotImplementedError


def test_to_string():
    raise NotImplementedError


def test_equal():
    raise NotImplementedError


def test_hash():
    raise NotImplementedError

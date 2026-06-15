import logging
import re

import pytest
from err_backend_discord.discordlib.person import DiscordPerson
from mock import MagicMock, patch

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def mock_client():
    with patch("err_backend_discord.discordlib.person.DiscordPerson.client", MagicMock()) as mock:
        yield mock


def test_wrong_userid():
    with pytest.raises(ValueError):
        DiscordPerson(user_id="123")


def test_create_person_without_args():
    with pytest.raises(ValueError):
        DiscordPerson()


def test_create_person_with_username_only():
    with pytest.raises(LookupError):
        DiscordPerson(username="someone")


def test_create_person_with_discriminator_only():
    with pytest.raises(ValueError):
        DiscordPerson(discriminator="#1234")


def test_create_person_with_id(mock_client):
    mock_user = MagicMock()
    mock_user.id = 123456789012345678
    mock_client.get_user.return_value = mock_user
    person = DiscordPerson(user_id="123456789012345678")
    assert person.id == 123456789012345678


def test_create_person_with_17_digit_id(mock_client):
    mock_user = MagicMock()
    mock_user.id = 12345678901234567
    mock_client.get_user.return_value = mock_user
    person = DiscordPerson(user_id="12345678901234567")
    assert person.id == 12345678901234567


def test_create_person_username_and_discriminator(mock_client):
    mock_user = MagicMock()
    mock_user.id = 123456789012345678
    mock_user.name = "someone"
    mock_user.discriminator = "1234"

    with patch.object(DiscordPerson, "resolve_username", return_value=mock_user):
        mock_client.get_user.return_value = mock_user
        person = DiscordPerson(username="someone", discriminator="1234")
        assert person.id == 123456789012345678
        assert person.username == "someone"

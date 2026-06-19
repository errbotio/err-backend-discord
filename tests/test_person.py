import logging
import re

import pytest
from mock import MagicMock, patch

from err_backend_discord.discordlib.person import DiscordPerson

log = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def mock_client():
    with patch("err_backend_discord.discordlib.person.DiscordPerson.client", MagicMock()) as mock:
        yield mock


def test_wrong_userid():
    with pytest.raises(ValueError):
        DiscordPerson(user_id="abc")


def test_create_person_without_args():
    with pytest.raises(ValueError):
        DiscordPerson()


def test_create_person_with_username_only():
    with pytest.raises(LookupError):
        DiscordPerson(username="someone")


def test_create_person_with_discriminator_only():
    with pytest.raises(ValueError):
        DiscordPerson(discriminator="#1234")


@pytest.mark.parametrize(
    "id_val",
    [
        123456789012345,  # 15 digits
        1234567890123456,  # 16 digits
        12345678901234567,  # 17 digits
        123456789012345678,  # 18 digits
        12345678901234567890,  # 20 digits
    ],
)
def test_create_person_with_valid_id(mock_client, id_val):
    mock_user = MagicMock()
    mock_user.id = id_val
    mock_client.get_user.return_value = mock_user
    person = DiscordPerson(user_id=str(id_val))
    assert person.id == id_val


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

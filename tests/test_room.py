import logging

import pytest
from err_backend_discord.discordlib.room import DiscordRoom
from mock import MagicMock

log = logging.getLogger(__name__)


@pytest.fixture
def discord_room():
    room = DiscordRoom
    setattr(room, "client", MagicMock())
    return room


def test_create_room_without_arguments():
    with pytest.raises(ValueError) as excinfo:
        DiscordRoom()
    assert "A name or channel id + guild id is required to create a Room." in str(excinfo.value)


def test_create_room_with_name_only():
    with pytest.raises(ValueError) as excinfo:
        DiscordRoom(channel_name="#testing_ground")
    assert "A name or channel id + guild id is required to create a Room." in str(excinfo.value)


def test_create_room_with_guild_only():
    with pytest.raises(ValueError) as excinfo:
        DiscordRoom(guild_id="1234567890123456789")
    assert "A name or channel id + guild id is required to create a Room." in str(excinfo.value)


def test_create_room_with_id(discord_room):
    room = discord_room(channel_id="1234567890132456789")
    assert room.id == 1234567890132456789


def test_create_room_with_name_and_guild_id(discord_room):
    mock_guild = MagicMock()
    mock_channel = MagicMock()
    mock_channel.name = "#testing_ground"
    mock_channel.id = 1234567890132456789
    mock_guild.channels = [mock_channel]
    DiscordRoom.client.get_guild.return_value = mock_guild

    room = discord_room(channel_name="#testing_ground", guild_id="2345678901234567890")
    assert room.id == 1234567890132456789

import sys
import logging

from typing import List, Optional, Union


from errbot.backends.base import (
    Room,
    RoomOccupant,
    RoomError,
)

from discordlib.person import (
    DiscordSender,
    DiscordPerson,
)


log = logging.getLogger(__name__)

try:
    import discord
except ImportError:
    log.exception("Could not start err-backend-discord")
    log.fatal("The required discord module could not be found.")
    sys.exit(1)


class DiscordRoom(Room, DiscordSender):
    """
    DiscordRoom objects can be in two states:

    1. They exist and we have a channel_id of that room
    2. They don't currently exist and we have a channel name and guild
    """

    @classmethod
    def from_id(cls, channel_id):
        channel = DiscordRoom.client.get_channel(channel_id)

        if channel is None:
            raise ValueError(f"Channel id:{channel_id} doesn't exist!")

        return cls(channel.name, channel.guild.id)

    def __init__(self, channel_name: str = None, guild_id: str = None, channel_id: str = None):
        """
        Allows to specify an existing room (via name + guild or via id) or allows the
        creation of a future room by specifying a name and guild to create the channel in.

        :param channel_name:
        :param guild_id:
        :param channel_id:
        """

        if channel_id:
            self._channel_id = int(channel_id)
            self._channel_name = None
            self._guild_id = None
        else:
            if DiscordRoom.client.get_guild(int(guild_id)) is None:
                raise ValueError(f"Can't find guild id {guild_id} to init DiscordRoom")

            self._guild_id = guild_id
            self._channel_name = channel_name
            self._channel_id = self.channel_name_to_id()  # Can be None if channel doesn't exist

        self.discord_channel = DiscordRoom.client.get_channel(self._channel_id)

    def get_discord_object(self):
        return self.discord_channel

    def channel_name_to_id(self):
        """
        Channel names are non-unique across Discord. Hence we require a guild name to uniquely
        identify a room id

        :return: ID of the room
        """
        matching = [
            channel
            for channel in DiscordRoom.client.get_all_channels()
            if self._channel_name == channel.name
            and channel.guild.id == self._guild_id
            and isinstance(channel, discord.TextChannel)
        ]

        if len(matching) == 0:
            return None

        if len(matching) > 1:
            log.warning(
                "Multiple matching channels for channel"
                f"name {self._channel_name} in guild id {self._guild_id}"
            )

        return matching[0].id

    @property
    def created_at(self):
        return discord.utils.snowflake_time(self.id)

    def invite(self, *args) -> None:
        if not self.exists:
            raise RuntimeError("Can't invite to a non-existent channel")

        for identifier in args:
            if not isinstance(identifier, DiscordPerson):
                raise RuntimeError("Can't invite non Discord Users")

            asyncio.run_coroutine_threadsafe(
                self.discord_channel.set_permissions(identifier.discord_user(), read_messages=True),
                loop=DiscordRoom.client.loop,
            )

    @property
    def joined(self) -> bool:
        log.error("Not implemented")
        return True

    def leave(self, reason: str = None) -> None:
        """
        Can't just leave a room
        :param reason:
        :return:
        """
        log.error("Not implemented")

    async def create_room(self):
        guild = DiscordRoom.client.get_guild(self._guild_id)

        channel = await guild.create_text_channel(self._channel_name)

        log.info(f"Created channel {self._channel_name} in guild {guild.name}")

        self._channel_id = channel.id

    def create(self) -> None:
        if self.exists:
            log.warning(f"Tried to create {self._channel_name} which already exists.")
            raise RoomError("Room exists")

        asyncio.run_coroutine_threadsafe(self.create_room(), loop=DiscordRoom.client.loop).result(
            timeout=5
        )

    def destroy(self) -> None:
        if not self.exists:
            log.warning(f"Tried to destroy {self._channel_name} which doesn't exist.")
            raise RoomError("Room doesn't exist")

        asyncio.run_coroutine_threadsafe(
            self.discord_channel.delete(reason="Bot deletion command"),
            loop=DiscordRoom.client.loop,
        ).result(timeout=5)

    def join(self, username: str = None, password: str = None) -> None:
        """
        All public channels are already joined. Only private channels can be joined and we
        need an invite for that.
        :param username:
        :param password:
        :return:
        """
        log.warning(
            "Can't join channels.  Public channels are automatically joined"
            " and private channels are invite only."
        )

    @property
    def topic(self) -> str:
        if not self.exists:
            return ""

        topic = self.discord_channel.topic
        topic = "" if topic is None else topic

        return topic

    @property
    def occupants(self) -> List[RoomOccupant]:
        if not self.exists:
            return []

        occupants = []
        for member in self.discord_channel.members:
            occupants.append(DiscordRoomOccupant(member.id, self._channel_id))

        return occupants

    @property
    def exists(self) -> bool:
        return None not in [self._channel_id, DiscordRoom.client.get_channel(self._channel_id)]

    @property
    def guild(self):
        """
        Gets the guild_id this channel belongs to. None if it doesn't exist
        :return: Guild id or None
        """
        return self._guild_id

    @property
    def name(self) -> str:
        """
        Gets the channels' name

        :return: channels' name
        """
        if self._channel_id is None:
            return self._channel_name
        else:
            self._channel_name = DiscordRoom.client.get_channel(self._channel_id).name
            return self._channel_name

    @property
    def id(self):
        """
        Can return none if not created
        :return: Channel ID or None
        """
        return self._channel_id

    async def send(self, content: str = None, embed: discord.Embed = None):
        if not self.exists:
            raise RuntimeError("Can't send a message on a non-existent channel")
        if not isinstance(self.discord_channel, discord.abc.Messageable):
            raise RuntimeError(
                f"Channel {self.name}[id:{self._channel_id}] doesn't support sending text messages"
            )

        await self.discord_channel.send(content=content, embed=embed)

    def __str__(self):
        return f"<#{self.id}>"

    def __eq__(self, other: "DiscordRoom"):
        if not isinstance(other, DiscordRoom):
            return False

        return None not in [other.id, self.id] and other.id == self.id


class DiscordRoomOccupant(DiscordPerson, RoomOccupant):
    def __init__(self, user_id: str, channel_id: str):
        super().__init__(user_id)

        self._channel = DiscordRoom.from_id(channel_id)

    @property
    def room(self) -> DiscordRoom:
        return self._channel

    async def send(self, content: str = None, embed: discord.Embed = None):
        await self.room.send(content=content, embed=embed)

    def __eq__(self, other):
        return (
            isinstance(other, DiscordRoomOccupant)
            and other.id == self.id
            and other.room.id == self.room.id
        )

    def __str__(self):
        return f"{super().__str__()}@{self._channel.name}"


class DiscordCategory(DiscordRoom):
    def channel_name_to_id(self):
        """
        Channel names are non-unique across Discord. Hence we require a guild name to
        uniquely identify a room id.

        :return: ID of the room
        """
        matching = [
            channel
            for channel in DiscordCategory.client.get_all_channels()
            if self._channel_name == channel.name
            and channel.guild.id == self._guild_id
            and isinstance(channel, discord.CategoryChannel)
        ]

        if len(matching) == 0:
            return None

        if len(matching) > 1:
            log.warning(
                "Multiple matching channels for channel name"
                f" {self._channel_name} in guild id {self._guild_id}"
            )

        return matching[0].id

    def create_subchannel(self, name: str) -> DiscordRoom:
        category = self.get_discord_object()

        if not isinstance(category, discord.CategoryChannel):
            raise RuntimeError("Category is not a discord category object")

        text_channel = asyncio.run_coroutine_threadsafe(
            category.create_text_channel(name), loop=DiscordCategory.client.loop
        ).result(timeout=5)

        return DiscordRoom.from_id(text_channel.id)

    async def create_room(self):
        guild = DiscordCategory.client.get_guild(self._guild_id)

        channel = await guild.create_category(self._channel_name)

        log.info(f"Created category {self._channel_name} in guild {guild.name}")

        self._channel_id = channel.id

    def join(self, username: str = None, password: str = None) -> None:
        raise RuntimeError("Can't join categories")

    def leave(self, reason: str = None) -> None:
        raise RuntimeError("Can't leave categories")

    @property
    def joined(self) -> bool:
        raise RuntimeError("Can't join categories")

    @property
    def topic(self) -> str:
        raise RuntimeError("Can't set category topic")

    @property
    def occupants(self) -> List[RoomOccupant]:
        raise NotImplementedError("Not implemented yet")

    def invite(self, *args) -> None:
        raise RuntimeError("Can't invite to categories")

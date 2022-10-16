import re
import sys
import logging

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from errbot.backends.base import Person

log = logging.getLogger(__name__)

try:
    import discord
except ImportError:
    log.exception("Could not start err-backend-discord")
    log.fatal("The required discord module could not be found.")
    sys.exit(1)


class DiscordSender(ABC, discord.abc.Snowflake):
    """
    DiscordSender's client property is used to share a single discord instance
    with all classes.  It is populated when the backend is initialised.
    """

    client = None

    @abstractmethod
    async def send(self, content: str = None, embed: discord.Embed = None):
        raise NotImplementedError

    @abstractmethod
    def get_discord_object(self) -> discord.abc.Messageable:
        raise NotImplementedError


class DiscordPerson(Person, DiscordSender):
    @classmethod
    def username_and_discriminator_to_userid(cls, username: str, discriminator: str) -> str:
        return discord.utils.find(
            lambda m: m.name == username and m.discriminator == discriminator,
            DiscordPerson.client.get_all_members(),
        )

    def __init__(self, user_id: str):
        """
        @user_id: _must_ be a string representation of a Discord Snowflake (an integer).
        """
        if not re.match(r"[0-9]+", str(user_id)):
            raise ValueError(f"Invalid Discord user id {type(user_id)} {user_id}.")
        self._user_id = user_id

    def get_discord_object(self) -> discord.abc.Messageable:
        return self.discord_user()

    @property
    def created_at(self):
        return discord.utils.snowflake_time(self.id)

    @property
    def person(self) -> str:
        return str(self)

    @property
    def id(self) -> str:
        return self._user_id

    def discord_user(self) -> discord.User:
        return DiscordPerson.client.get_user(self._user_id)

    @property
    def username(self) -> str:
        """Convert a Discord user ID to their user name"""
        user = self.discord_user()

        if user is None:
            log.error(f"Cannot find user with ID {self._user_id}")
            return f"<{self._user_id}>"

        return user.name

    nick = username

    @property
    def client(self) -> None:
        return None

    @property
    def fullname(self) -> Optional[str]:
        usr = self.discord_user()

        if usr is None:
            raise ValueError("Discord user is not defined.")

        return f"{usr.name}#{usr.discriminator}"

    @property
    def aclattr(self) -> str:
        return self.fullname

    async def send(
        self,
        content: str = None,
        tts: bool = False,
        embed: discord.Embed = None,
        file: discord.File = None,
        files: List[discord.File] = None,
        delete_after: float = None,
        nonce: int = None,
        allowed_mentions: discord.AllowedMentions = None,
        reference: Union[discord.Message, discord.MessageReference] = None,
        mention_author: Optional[bool] = None,
    ):
        await self.discord_user().send(
            content=content,
            tts=tts,
            embed=embed,
            file=file,
            files=files,
            delete_after=delete_after,
            nonce=nonce,
            allowed_mentions=allowed_mentions,
            reference=reference,
            mention_author=mention_author,
        )

    def __eq__(self, other):
        return isinstance(other, DiscordPerson) and other.aclattr == self.aclattr

    def __str__(self):
        return f"{self.fullname}"

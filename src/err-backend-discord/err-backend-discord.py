import asyncio
import logging
import sys

from errbot.core import ErrBot
from errbot.backends.base import (
    Person,
    Message,
    Presence,
    ONLINE,
    OFFLINE,
    AWAY,
    DND,
)

from discordlib.person import (
    DiscordSender,
    DiscordPerson,
)
from discordlib.room import (
    DiscordRoom,
    DiscordRoomOccupant,
    DiscordCategory,
)

log = logging.getLogger(__name__)

try:
    import discord
except ImportError:
    log.exception("Could not start err-backend-discord")
    log.fatal("The required discord module could not be found.")
    sys.exit(1)

COLOURS = {
    "red": 0xFF0000,
    "green": 0x008000,
    "yellow": 0xFFA500,
    "blue": 0x0000FF,
    "white": 0xFFFFFF,
    "cyan": 0x00FFFF,
}


class DiscordBackend(ErrBot):
    """
    Discord backend for Errbot.
    """

    client = None

    def __init__(self, config):
        super().__init__(config)

        self.token = config.BOT_IDENTITY.get("token", None)

        if not self.token:
            log.fatal(
                "You need to set a token entry in the BOT_IDENTITY"
                " setting of your configuration."
            )
            sys.exit(1)

        self.bot_identifier = None

        intents = discord.Intents.default()
        intents.members = True

        DiscordBackend.client = discord.Client(intents=intents)

        # Use dependency injection to make discord client available to submodule classes.
        DiscordCategory.client = DiscordBackend.client
        DiscordRoomOccupant.client = DiscordBackend.client
        DiscordRoom.client = DiscordBackend.client
        DiscordPerson.client = DiscordBackend.client
        DiscordSender.client = DiscordBackend.client

        # Register discord event coroutines.
        for func in [
            self.on_ready,
            self.on_message,
            self.on_member_update,
            self.on_message_edit,
            self.on_member_update,
        ]:
            DiscordBackend.client.event(func)

    def set_message_size_limit(self, limit=2000, hard_limit=2000):
        """
        Discord supports up to 2000 characters per message.
        """
        super().set_message_size_limit(limit, hard_limit)

    async def on_error(self, event, *args, **kwargs):
        super().on_error(event, *args, **kwargs)
        # A stub entry in case special error handling is required.
        pass

    async def on_ready(self):
        """
        Discord client ready event handler
        """
        # Call connect only after successfully connected and ready to service Discord events.
        self.connect_callback()

        log.debug(
            f"Logged in as {DiscordBackend.client.user.name}, {DiscordBackend.client.user.id}"
        )
        if self.bot_identifier is None:
            self.bot_identifier = DiscordPerson(DiscordBackend.client.user.id)

        for channel in DiscordBackend.client.get_all_channels():
            log.debug(f"Found channel: {channel}")

    async def on_message_edit(self, before, after):
        """
        Edit message event handler
        """
        log.warning("Message editing not supported.")

    async def on_message(self, msg: discord.Message):
        """
        Message event handler
        """
        err_msg = Message(msg.content, extras=msg.embeds)

        if isinstance(msg.channel, discord.abc.PrivateChannel):
            err_msg.frm = DiscordPerson(msg.author.id)
            err_msg.to = self.bot_identifier
        else:
            err_msg.to = DiscordRoom.from_id(DiscordBackend.client, msg.channel.id)
            err_msg.frm = DiscordRoomOccupant(DiscordBackend.client, msg.author.id, msg.channel.id)

        if self.process_message(err_msg):
            # Message contains a command
            recipient = err_msg.frm

            if not isinstance(recipient, DiscordSender):
                raise ValueError("Message object from is not a DiscordSender")

            async with recipient.get_discord_object().typing():
                self._dispatch_to_plugins("callback_message", err_msg)

        if msg.mentions:
            self.callback_mention(
                err_msg,
                [
                    DiscordRoomOccupant(DiscordBackend.client, mention.id, msg.channel.id)
                    for mention in msg.mentions
                ],
            )

    def is_from_self(self, msg: Message) -> bool:
        """
        Test if message is from the bot instance.
        """
        other = msg.frm

        if not isinstance(other, DiscordPerson):
            return False

        return other.id == self.bot_identifier.id

    async def on_member_update(self, before, after):
        """
        Member update event handler
        """
        if before.status != after.status:
            person = DiscordPerson(after.id)

            log.debug(f"Person {person} changed status to {after.status} from {before.status}")
            if after.status == discord.Status.online:
                self.callback_presence(Presence(person, ONLINE))
            elif after.status == discord.Status.offline:
                self.callback_presence(Presence(person, OFFLINE))
            elif after.status == discord.Status.idle:
                self.callback_presence(Presence(person, AWAY))
            elif after.status == discord.Status.dnd:
                self.callback_presence(Presence(person, DND))
        else:
            log.debug("Unrecognised member update, ignoring...")

    def query_room(self, room):
        """
        Query room.

        This method implicitly assume the bot is in one guild server.

        ##category -> a category
        #room -> Creates a room

        :param room:
        :return:
        """
        if len(DiscordBackend.client.guilds) == 0:
            log.error(f"Unable to join room '{room}' because no guilds were found!")
            return None

        guild = DiscordBackend.client.guilds[0]

        room_name = room
        if room_name.startswith("##"):
            return DiscordCategory(room_name[2:], guild.id)
        elif room_name.startswith("#"):
            return DiscordRoom(room_name[1:], guild.id)
        else:
            return DiscordRoom(room_name, guild.id)

    def send_message(self, msg: Message):
        super().send_message(msg)

        if not isinstance(msg.to, DiscordSender):
            raise RuntimeError(
                f"{msg.to} doesn't support sending messages."
                f"  Expected DiscordSender object but got {type(msg.to)}."
            )

        log.debug(
            f"Message to:{msg.to}({type(msg.to)}) from:{msg.frm}({type(msg.frm)}),"
            f" is_direct:{msg.is_direct} extras: {msg.extras} size: {len(msg.body)}"
        )

        for message in [
            msg.body[i : i + self.message_size_limit]
            for i in range(0, len(msg.body), self.message_size_limit)
        ]:
            asyncio.run_coroutine_threadsafe(
                msg.to.send(content=message), loop=DiscordBackend.client.loop
            )

    def send_card(self, card):
        recipient = card.to

        if not isinstance(recipient, DiscordSender):
            raise RuntimeError(
                f"{recipient} doesn't support sending messages."
                f"  Expected {DiscordSender} but got {type(recipient)}"
            )

        if card.color:
            color = COLOURS.get(card.color, int(card.color.replace("#", "0x"), 16))
        else:
            color = None

        # Create Embed object
        em = discord.Embed(title=card.title, description=card.body, color=color)

        if card.image:
            em.set_image(url=card.image)

        if card.thumbnail:
            em.set_thumbnail(url=card.thumbnail)

        if card.fields:
            for key, value in card.fields:
                em.add_field(name=key, value=value, inline=True)

        asyncio.run_coroutine_threadsafe(
            recipient.send(embed=em), loop=DiscordBackend.client.loop
        ).result(5)

    def build_reply(self, mess, text=None, private=False, threaded=False):
        response = self.build_message(text)

        if mess.is_direct:
            response.frm = self.bot_identifier
            response.to = mess.frm
        else:
            if not isinstance(mess.frm, DiscordRoomOccupant):
                raise RuntimeError("Non-Direct messages must come from a room occupant")

            response.frm = DiscordRoomOccupant(self.bot_identifier.id, mess.frm.room.id)
            response.to = DiscordPerson(mess.frm.id) if private else mess.to
        return response

    def serve_once(self):
        try:
            DiscordBackend.client.loop.run_until_complete(DiscordBackend.client.start(self.token))
        except KeyboardInterrupt:
            DiscordBackend.client.loop.run_until_complete(DiscordBackend.client.logout())
            pending = asyncio.Task.all_tasks()
            gathered = asyncio.gather(*pending)
            # noinspection PyBroadException
            try:
                gathered.cancel()
                DiscordBackend.client.loop.run_until_complete(gathered)

                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except Exception:
                pass
            self.disconnect_callback()
            return True

    def change_presence(self, status: str = ONLINE, message: str = ""):
        log.debug(f'Presence changed to {status} and activity "{message}".')
        activity = discord.Activity(name=message)
        DiscordBackend.client.change_presence(status=status, activity=activity)

    def prefix_groupchat_reply(self, message, identifier: Person):
        message.body = f"@{identifier.nick} {message.body}"

    def rooms(self):
        return [
            DiscordRoom.from_id(channel.id) for channel in DiscordBackend.client.get_all_channels()
        ]

    @property
    def mode(self):
        return "discord"

    def build_identifier(self, string_representation: str):
        """
        This needs a major rethink/rework since discord bots can be in different
        Guilds so room name clashes are certainly possible. For now we are only
        uniquely identifying users

        Valid forms of strreps:
        user#discriminator      -> Person
        #channel@guild_id       -> Room

        :param string_representation:
        :return: Identifier

        Room Example: #general@12345678901234567 -> Sends a message to the
                   #general channel of the guild with id 12345678901234567
        """
        if not string_representation:
            raise ValueError("Empty strrep")

        if string_representation.startswith("#"):
            strrep_split = string_representation.split("@")
            return DiscordRoom(strrep_split[0][1:], int(strrep_split[1]))

        if "#" in str(string_representation):
            user, discriminator = str(string_representation).split("#")
        else:
            raise ValueError("No Discriminator")
        log.debug(f"Build_identifier {string_representation}")
        member = DiscordPerson.username_and_discriminator_to_userid(user, discriminator)

        return DiscordPerson(user_id=member.id)

    def upload_file(self, msg, filename):
        with open(filename, "r") as f:

            dest = None
            if msg.is_direct:
                dest = DiscordPerson(msg.frm.id).get_discord_object()
            else:
                dest = msg.to.get_discord_object()

            log.info(f"Sending file {filename} to user {msg.frm}")
            asyncio.run_coroutine_threadsafe(
                dest.send(file=discord.File(f, filename=filename)),
                loop=self.client.loop,
            )

    def history(self, channelname, before=None):
        mychannel = discord.utils.get(self.client.get_all_channels(), name=channelname)

        async def gethist(mychannel, before=None):
            return [i async for i in self.client.logs_from(mychannel, limit=10, before=before)]

        future = asyncio.run_coroutine_threadsafe(gethist(mychannel, before), loop=self.client.loop)
        return future.result(timeout=None)

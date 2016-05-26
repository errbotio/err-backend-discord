from typing import Any

from errbot.backends.base import Person, Message, Room, RoomOccupant
from errbot.errBot import ErrBot
import logging
import sys
import discord
import asyncio

# Can't use __name__ because of Yapsy
log = logging.getLogger('errbot.backends.discord')


class DiscordPerson(discord.User, Person):

    def __init__(self, username=None, id_=None, discriminator=None, avatar=None):
        super().__init__(username=username, id=id_, discriminator=discriminator, avatar=avatar)

    @property
    def person(self) -> str:
        return self.discriminator

    @property
    def aclattr(self) -> str:
        return self.id

    @property
    def nick(self) -> str:
        return self.name

    @property
    def fullname(self) -> str:
        return self.name

    @property
    def client(self) -> str:
        return None

    @staticmethod
    def from_user(user: discord.User):
        return DiscordPerson(user.name, user.id, user.discriminator, user.avatar)

    def __eq__(self, other):
        return isinstance(other, DiscordPerson) and other.person == self.person


class DiscordRoom(Room):
    def __init__(self, name, channel: discord.Channel=None):
        self.name = name
        self.channel = channel

    @staticmethod
    def from_channel(channel: discord.Channel):
        if channel.is_private:
            raise ValueError('You cannot build a Room from a private channel')
        return DiscordRoom(channel.name, channel)

    def __str__(self):
        return '#' + self.name

    def __eq__(self, other):
        return other.name == self.name


class DiscordRoomOccupant(DiscordPerson, RoomOccupant):
    def __init__(self, username=None, id_=None, discriminator=None, avatar=None, room: DiscordRoom=None):
        super().__init__(username=username, id_=id_, discriminator=discriminator, avatar=avatar)
        self._room = room

    @property
    def room(self) -> Any:
        return self._room

    @staticmethod
    def from_user_and_channel(user: discord.User, channel: discord.Channel):
        return DiscordRoomOccupant(username=user.name,
                                   id_ =user.id,
                                   discriminator=user.discriminator,
                                   avatar=user.avatar,
                                   room=DiscordRoom.from_channel(channel))

    def __eq__(self, other):
        return isinstance(other, DiscordRoomOccupant) and str(other) == str(self)

    def __str__(self):
        return super().__str__() + '@' + self._room.name


class DiscordBackend(ErrBot):
    """
    This is the Discord backend for Errbot.
    """

    def __init__(self, config):
        super().__init__(config)
        identity = config.BOT_IDENTITY

        self.email = identity.get('email', None)
        self.password = identity.get('password', None)
        self.rooms_to_join = config.CHATROOM_PRESENCE

        if not self.email or not self.password:
            log.fatal('You need to set a email and a password entry in the BOT_IDENTITY setting of your configuration.')
            sys.exit(1)
        self.bot_identifier = None

        self.client = discord.Client()
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)

    async def on_ready(self):
        log.debug('Logged in as %s, %s' % (self.client.user.name, self.client.user.id))
        self.bot_identifier = DiscordPerson.from_user(self.client.user)
        for channel in self.client.get_all_channels():
            log.debug('Found channel: %s', channel)

    async def on_message(self, msg: discord.Message):
        err_msg = Message(msg.content)
        if msg.channel.is_private:
            err_msg.frm = DiscordPerson.from_user(msg.author)
            err_msg.to = self.bot_identifier
        else:
            err_msg.to = DiscordRoom.from_channel(msg.channel)
            err_msg.frm = DiscordRoomOccupant.from_user_and_channel(msg.author, msg.channel)

        log.debug('Received message %s' % msg)
        self.callback_message(err_msg)

    def build_identifier(self, strrep: str):
        """
        Valid forms of strreps:

        user#discriminator@room -> RoomOccupant
        user#discriminator      -> Person
        user@room               -> (Ambiguous) RoomOccupant
        user                    -> (Ambiguous) Person
        #room                   -> Room

        :param strrep:
        :return:
        """
        if not strrep:
            raise ValueError('Empty strrep')

        if strrep.startswith('#'):
            return DiscordRoom(strrep[1:])

        if '@' in strrep:
            user_and_discrim, room = strrep.split('@')
        else:
            user_and_discrim = strrep
            room = None

        if '#' in user_and_discrim:
            user, discriminator = user_and_discrim.split('#')
        else:
            user = user_and_discrim
            discriminator = None

        if room:
            return DiscordRoomOccupant(username=user, discriminator=discriminator, room=DiscordRoom(room))

        return DiscordPerson(username=user, discriminator=discriminator)

    def query_room(self, room):
        return self.build_identifier(room)  # backward compatibility.

    def send_message(self, msg):
        log.debug('Send:\n%s\nto %s' % (msg.body, msg.to))
        if msg.is_direct:
            co = self.client.send_message(destination=msg.to, content=msg.body)
        else:
            co = self.client.send_message(destination=msg.to.room.channel, content=msg.body)
        self.client.loop.create_task(co)
        super().send_message(msg)

    def build_reply(self, mess, text=None, private=False):
        response = self.build_message(text)
        response.frm = mess.to
        response.to = mess.frm
        if private:
            response.to = self.build_identifier(mess.frm.nick)
        return response

    def serve_once(self):
        self.connect_callback()
        try:
            self.client.run(self.email, self.password)
        except KeyboardInterrupt:
            log.info("Interrupt received, shutting down..")
            return True
        finally:
            self.disconnect_callback()

    def change_presence(self, status, message):
        log.warn("Presence is not implemented on the discord backend.")
        pass

    def prefix_groupchat_reply(self, message, identifier):
        message.body = '@{0} {1}'.format(identifier.nick, message.body)

    def rooms(self):
        return None

    @property
    def mode(self):
        return 'discord'

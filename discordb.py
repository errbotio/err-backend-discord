from typing import Any, List

from errbot.backends.base import Person, Message, Room, RoomOccupant, Presence, ONLINE, OFFLINE, AWAY, DND
from errbot.errBot import ErrBot
import logging
import sys
import discord
import asyncio

# Can't use __name__ because of Yapsy
log = logging.getLogger('errbot.backends.discord')

# Discord message size limit.
DISCORD_MESSAGE_SIZE_LIMIT = 2000

COLORS = {
    'red': 0xFF0000,
    'green': 0x008000,
    'yellow': 0xFFA500,
    'blue': 0x0000FF,
    'white': 0xFFFFFF,
    'cyan': 0x00FFFF
}  # Discord doesn't know its colors

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
    def invite(self, *args) -> None:
        log.error('Not implemented')

    @property
    def joined(self) -> bool:
        log.error('Not implemented')
        return True

    def leave(self, reason: str = None) -> None:
        log.error('Not implemented')

    def create(self) -> None:
        log.error('Not implemented')

    def destroy(self) -> None:
        log.error('Not implemented')

    def join(self, username: str = None, password: str = None) -> None:
        log.error('Not implemented')

    @property
    def topic(self) -> str:
        log.error('Not implemented')
        return ''

    @property
    def occupants(self) -> List[RoomOccupant]:
        log.error('Not implemented')
        return []

    @property
    def exists(self) -> bool:
        log.error('Not implemented')
        return True

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

    @staticmethod
    def from_user_and_room(user: discord.User, room: DiscordRoom):
        return DiscordRoomOccupant(username=user.name,
                                   id_ =user.id,
                                   discriminator=user.discriminator,
                                   avatar=user.avatar,
                                   room=room)

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

        self.token = identity.get('token', None)
        self.rooms_to_join = config.CHATROOM_PRESENCE

        if not self.token:
            log.fatal('You need to set a token entry in the BOT_IDENTITY setting of your configuration.')
            sys.exit(1)
        self.bot_identifier = None

        self.client = discord.Client()
        self.on_ready = self.client.event(self.on_ready)
        self.on_message = self.client.event(self.on_message)
        self.on_member_update = self.client.event(self.on_member_update)

    @asyncio.coroutine
    def on_ready(self):
        log.debug('Logged in as %s, %s' % (self.client.user.name, self.client.user.id))
        self.bot_identifier = DiscordPerson.from_user(self.client.user)
        for channel in self.client.get_all_channels():
            log.debug('Found channel: %s', channel)

    @asyncio.coroutine
    def on_message(self, msg: discord.Message):
        err_msg = Message(msg.content)
        if msg.channel.is_private:
            err_msg.frm = DiscordPerson.from_user(msg.author)
            err_msg.to = self.bot_identifier
        else:
            err_msg.to = DiscordRoom.from_channel(msg.channel)
            err_msg.frm = DiscordRoomOccupant.from_user_and_channel(msg.author, msg.channel)

        log.debug('Received message %s' % msg)
        self.callback_message(err_msg)
        if msg.mentions:
            self.callback_mention(err_msg,
                                  [DiscordRoomOccupant.from_user_and_channel(mention, msg.channel)
                                   for mention in msg.mentions])

    @asyncio.coroutine
    def on_member_update(self, before, after):
        if before.status != after.status:
            person = DiscordPerson.from_user(after)
            log.debug('Person %s changed status to %s from %s' % (person, after.status, before.status))
            if after.status == discord.Status.online:
                self.callback_presence(Presence(person, ONLINE))
            elif after.status == discord.Status.offline:
                self.callback_presence(Presence(person, OFFLINE))
            elif after.status == discord.Status.idle:
                self.callback_presence(Presence(person, AWAY))
            elif after.status == discord.Status.dnd:
                self.callback_presence(Presence(person, DND))
        else:
            log.debug('Unrocognized member update, ignoring...')

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
            recipient = msg.to
        else:
            if msg.to.channel is None:
                msg.to.channel = discord.utils.get(self.client.get_all_channels(), name=msg.to.name)
            recipient = msg.to.channel
        for message in [msg.body[i:i+DISCORD_MESSAGE_SIZE_LIMIT] for i in range(0, len(msg.body), DISCORD_MESSAGE_SIZE_LIMIT)]:
            self.client.loop.create_task(self.client.send_typing(recipient))
            self.client.loop.create_task(self.client.send_message(destination=recipient, content=message))

            super().send_message(msg)

    def send_card(self, card):
        if isinstance(card.to, RoomOccupant):
            card.to = card.to.room

        recipient = discord.utils.get(self.client.get_all_channels(), name=card.to.name)

        if card.color:
            color = COLORS[card.color] if card.color in COLORS else int(card.color.replace('#', '0x'), 16)
        else:
            color = None

        em = discord.Embed(title=card.title, description=card.summary, color=color)

        if card.image:
            em.set_image(url=card.image)

        if card.thumbnail:
            em.set_thumbnail(url=card.thumbnail)

        if card.fields:
            for key, value in card.fields:
                em.add_field(name=key, value=value, inline=True)

        self.client.loop.create_task(self.client.send_typing(recipient))
        self.client.loop.create_task(self.client.send_message(destination=recipient, embed=em))
        # in tests : check if card format is ok (i.e. if Embed.to_dict is as excepted)


    def build_reply(self, mess, text=None, private=False, threaded=False):
        log.debug('Threading is %s' % threaded)
        response = self.build_message(text)
        if mess.is_direct:
            response.frm = self.bot_identifier
            response.to = mess.frm
        else:
            response.frm = DiscordRoomOccupant.from_user_and_room(self.bot_identifier, response.to)
            response.to = DiscordPerson.from_user(mess.frm) if private else mess.to
        return response

    def serve_once(self):
        self.connect_callback()
        # Hehe client.run cannot be used as we need more control.
        try:
            self.client.loop.run_until_complete(self.client.start(self.token))
        except KeyboardInterrupt:
            self.client.loop.run_until_complete(self.client.logout())
            pending = asyncio.Task.all_tasks()
            gathered = asyncio.gather(*pending)
            try:
                gathered.cancel()
                self.client.loop.run_until_complete(gathered)

                # we want to retrieve any exceptions to make sure that
                # they don't nag us about it being un-retrieved.
                gathered.exception()
            except:
                pass
            self.disconnect_callback()
            return True

    def change_presence(self, status, message):
        log.debug('Presence changed to %s and game "%s".' % (status, message))
        self.client.change_presence(status=status, game=message)

    def prefix_groupchat_reply(self, message, identifier):
        message.body = '@{0} {1}'.format(identifier.nick, message.body)

    def rooms(self):
        return [DiscordRoom(channel.name) for channel in self.client.get_all_channels()]

    @property
    def mode(self):
        return 'discord'

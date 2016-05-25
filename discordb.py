from errbot.backends.base import Person
from errbot.errBot import ErrBot
import logging
import sys
import discord

# Can't use __name__ because of Yapsy
log = logging.getLogger('errbot.backends.discord')


class DiscordPerson(discord.User, Person):

    def __init__(self, name=None, id_=None, discriminator=None, avatar=None):
        super().__init__(name=name, id=id_, discriminator=discriminator, avatar=avatar)

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
    def from_discord(user: discord.User):
        return DiscordPerson(user.name, user.id, user.discriminator, user.avatar)


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
            log.fatal(
                    'You need to set your auth token in the BOT_IDENTITY setting of '
                    'your configuration. '
            )
            sys.exit(1)
        self.bot_identifier = None

        self.client = discord.Client()
        self.on_ready = self.client.event(self.on_ready)

    async def on_ready(self):
        log.debug('Logged in as %s, %s' % (self.client.user.name, self.client.user.id))
        self.bot_identifier = DiscordPerson.from_discord(self.client.user)

    def build_identifier(self, strrep):
        return DiscordPerson(strrep, None, None, None)

    def query_room(self, room):
        # TODO: maybe we can query the room resource only
        return None

    def send_message(self, mess):
        super().send_message(mess)

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
            self.client.run(self.token)
        except KeyboardInterrupt:
            log.info("Interrupt received, shutting down..")
            return True
        finally:
            self.disconnect_callback()

    def change_presence(self, status, message):
        log.warn("Presence is not implemented on the discord backend.")
        pass

    def prefix_groupchat_reply(self, message, identifier):
        message.body = '{0}: {1}'.format(identifier.nick, message.body)

    def rooms(self):
        return None

    @property
    def mode(self):
        return 'discord'

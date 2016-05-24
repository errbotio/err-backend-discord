from errbot.backends.base import Identifier
from errbot.errBot import ErrBot
import logging
import time
import sys
from errbot.rendering import md
import discord

# Can't use __name__ because of Yapsy
log = logging.getLogger('errbot.backends.discord')


class DiscordIdentifier(Identifier):
    pass


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

    def build_identifier(self, strrep):
        return DiscordIdentifier()

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

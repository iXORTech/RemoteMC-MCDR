from remotemc_mcdr.util.reply_util import reply_to_source
from remotemc_mcdr.util.version_util import *


def show_help(source: CommandSource):
    help_msg_lines = ["\n",
                      i18n("in_game.help_message.line1", get_version()) + "\n",
                      i18n("in_game.help_message.line2") + "\n",
                      i18n("in_game.help_message.line3") + "\n",
                      i18n("in_game.help_message.line4") + "\n",
                      i18n("in_game.help_message.line5") + "\n",
                      i18n("in_game.help_message.line6") + "\n",
                      i18n("in_game.help_message.line7") + "\n",
                      i18n("in_game.help_message.line8") + "\n"]
    reply_to_source(source, help_msg_lines)

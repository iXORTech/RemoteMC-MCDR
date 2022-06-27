import re

from remotemc_mcdr.constants import *

from remotemc_mcdr.util.i18n_util import *


def show_help(source: CommandSource):
    help_msg_lines = ['\n',
                      i18n('in_game.help_message.line1', VERSION) + '\n',
                      i18n('in_game.help_message.line2') + '\n',
                      i18n('in_game.help_message.line3') + '\n',
                      i18n('in_game.help_message.line4') + '\n',
                      i18n('in_game.help_message.line5') + '\n']
    help_msg_rtext = RTextList()
    for line in help_msg_lines:
        result = re.search(r'(?<=§7)!![\w ]*(?=§)', line)
        if result is not None:
            help_msg_rtext.append(
                RText(line).c(RAction.suggest_command, result.group()).h(
                    i18n('in_game.click_to_use_command', result.group())))
        else:
            help_msg_rtext.append(line)
    source.reply(help_msg_rtext)

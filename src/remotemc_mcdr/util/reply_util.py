import re

from mcdreforged.command.command_source import CommandSource
from mcdreforged.minecraft.rtext.style import RAction
from mcdreforged.minecraft.rtext.text import RTextList, RText

from remotemc_mcdr.util.i18n_util import i18n


def reply_to_source(source: CommandSource, msg_lines: list[str]):
    msg_rtext = RTextList()
    for line in msg_lines:
        result = re.search(r"(?<=§7)!![\w ]*(?=§)", line)
        if result is not None:
            msg_rtext.append(
                RText(line).c(RAction.suggest_command, result.group()).h(
                    i18n("in_game.click_to_use_command", result.group())))
        else:
            msg_rtext.append(line)
    source.reply(msg_rtext)

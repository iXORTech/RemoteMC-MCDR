import re

from mcdreforged.api.all import *

from remotemc_mcdr.constants import *


def show_help(source: CommandSource):
    help_msg_lines = '''
-------------------- RemoteMC-MCDR v{0} --------------------
MCDReforged Plugin of RemoteMC Series
§7!!remotemc §rShow this help message
§7!!msg §3<Message> §rSend message to all Minecraft servers and chat groups in the network
§7!!broadcast §3<Message> §rBroadcast to all Minecraft servers and chat groups in the network
'''.format(VERSION).splitlines(True)
    help_msg_rtext = RTextList()
    for line in help_msg_lines:
        result = re.search(r'(?<=§7)!![\w ]*(?=§)', line)
        if result is not None:
            help_msg_rtext.append(
                RText(line).c(RAction.suggest_command, result.group()).h(
                    'Click to use command §7{}§r'.format(result.group())))
        else:
            help_msg_rtext.append(line)
    source.reply(help_msg_rtext)

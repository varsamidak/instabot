"""
    instabot example

    Workflow:
        1) unfollows users that don't follow you.
"""

import argparse
import os
import sys
from instabot import Bot, utils

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()

bot= Bot()
bot.logger.info("searching non archived documents")
non_archived = bot.toArchive.set - bot.archived.set
f = utils.file("non-archived.txt")
f.save_list(non_archived)
bot.logger.info("done")

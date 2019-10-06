"""
    instabot example

    Workflow:
        Block bots. That makes them unfollow you -> You have clear account.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

bot.logger.info(
    "This script will block bots. "
    "So they will no longer be your follower. "
    "Bots are those users who:\n"
    " * have less than 10 followers\n"
    " * have no profile pic\n"
    " * have stopwords in user's info: "
    " %s " % str(bot.stop_words)
)
bot.search_bots()

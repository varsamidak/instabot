"""
    instabot example

    Workflow:
        Save users' followers into a file.
"""
import os
import sys
import argparse

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot, utils

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

myBotFollowers = []
bots = utils.file("myBotFollowers.txt")
for username in args.users:
    followers = bot.get_user_followers(username, 500)
    for follower in followers:
        user_info = bot.get_user_info(follower)
        myBotFollowers.append(follower)
    bots.save_list(myBotFollowers)
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
myFollowers = []
myFollowing = []
foler = utils.file("myFollowers.txt")
foling = utils.file("myFollowing.txt")
for username in args.users:
    followers = bot.get_user_followers(username, 100000)
    for follower in followers:
        myFollowers.append(follower)
    foler.save_list(myFollowers)
    followings = bot.get_user_following(username, 100000)
    for following in followings:
        myFollowing.append(following)
    foling.save_list(myFollowing)
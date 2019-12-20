"""
    instabot example

    Workflow:
        Save user' unfollowers into a file.
"""
import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot, utils  # noqa: E402

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-u", type=str, help="username")
parser.add_argument("-p", type=str, help="password")
parser.add_argument("-proxy", type=str, help="proxy")
args = parser.parse_args()

bot = Bot()
bot.login(username=args.u, password=args.p, proxy=args.proxy)

f = utils.file("non-followers.txt")
f2 = utils.file("whitelist-id.txt")
whitelisters = []
for user in list(bot.whitelist_file.set):
    bot.small_delay()
    user_id = bot.convert_to_user_id(user)
    whitelisters.append(user_id)
f2.save_list(whitelisters)

non_followers = list(bot.following_file.set - bot.whitelist_file.set - bot.friends_file.set - bot.followers_file.set)
non_followers_names = []

for user in non_followers:
    name = bot.get_username_from_user_id(user)
    non_followers_names.append(name)
    print(name)
    bot.small_delay()


f.save_list(non_followers_names)

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
followerAndMedia = []
f = utils.file("usersToFollow.txt")
for username in args.users:
    followers = bot.get_user_following(username, 7000)
    for follower in followers:
        media = []
        sum_media = ""
        media = bot.get_last_user_medias(follower, 3)
        sum_media = ':'.join(str(m) for m in media)
        followerAndMedia.append(follower + ":" + sum_media)
    f.save_list(followerAndMedia)

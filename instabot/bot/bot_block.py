import random
from instabot import utils

from tqdm import tqdm


def block(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if not self.reached_limit("blocks"):
        self.delay("block")
        if self.api.block(user_id):
            self.total["blocks"] += 1
            return True
    else:
        self.logger.info("Out of blocks for today.")
    return False


def unblock(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    if not self.reached_limit("unblocks"):
        self.delay("unblock")
        if self.api.unblock(user_id):
            self.total["unblocks"] += 1
            return True
    else:
        self.logger.info("Out of blocks for today.")
    return False


def block_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to block %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.block(user_id):
            self.error_delay()
            broken_items = user_ids[user_ids.index(user_id):]
            break
    self.logger.info("DONE: Total blocked %d users." % self.total["blocks"])
    return broken_items


def unblock_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unblock %d users." % len(user_ids))
    for user_id in tqdm(user_ids):
        if not self.unblock(user_id):
            self.error_delay()
            broken_items.append(user_id)
    self.logger.info(
        "DONE: Total unblocked %d users." % self.total["unblocks"]
    )
    return broken_items


def block_bots(self):
    self.logger.info("Going to block bots.")
    bots = self.read_list_from_file('myBotFollowers.txt')
    for user in tqdm(bots):
        self.block(user)

def search_bots(self):
    self.logger.info("Searching bots...")
    your_followers = self.get_user_followers('276887698')
    bots = []
    for user in tqdm(your_followers[-500:]):
        if not self.check_not_bot(user):
            self.logger.info(
                "Found bot: "
                "https://instagram.com/%s/"
                % self.get_user_info(user)["username"]
            )
            bots.append(user)
    botsFile = utils.file("myBotFollowers.txt")
    botsFile.save_list(bots)

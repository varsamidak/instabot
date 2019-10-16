import time
from tqdm import tqdm
import time
import random

def follow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    msg = " ===> Going to follow `user_id`: {}.".format(user_id)
    self.console_print(msg)
    if not self.check_user(user_id):
        return False
    if not self.reached_limit("follows"):
        if self.blocked_actions["follows"]:
            self.logger.warning("YOUR `FOLLOW` ACTION IS BLOCKED")
            if self.blocked_actions_protection:
                self.logger.warning(
                    "blocked_actions_protection ACTIVE. "
                    "Skipping `follow` action."
                )
                return False
        self.delay("follow")
        _r = self.api.follow(user_id)
        if _r == "feedback_required":
            self.logger.error("`Follow` action has been BLOCKED...!!!")
            if not self.blocked_actions_sleep:
                if self.blocked_actions_protection:
                    self.logger.warning("Activating blocked actions \
                        protection for `Follow` action.")
                    self.blocked_actions["follows"] = True
            else:
                if self.sleeping_actions["follows"] \
                        and self.blocked_actions_protection:
                    self.logger.warning("This is the second blocked \
                        `Follow` action.")
                    self.logger.warning("Activating blocked actions \
                        protection for `Follow` action.")
                    self.sleeping_actions["follows"] = False
                    self.blocked_actions["follows"] = True
                else:
                    self.logger.info("`Follow` action is going to sleep \
                        for %s seconds." % self.blocked_actions_sleep_delay)
                    self.sleeping_actions["follows"] = True
                    time.sleep(self.blocked_actions_sleep_delay)
            return False
        if _r:
            msg = "===> FOLLOWED <==== `user_id`: {}.".format(user_id)
            self.console_print(msg, "green")
            self.total["follows"] += 1
            self.followed_file.append(user_id)
            if user_id not in self.following:
                self.following.append(user_id)
            if self.blocked_actions_sleep and self.sleeping_actions["follows"]:
                self.logger.info("`Follow` action is no longer sleeping.")
                self.sleeping_actions["follows"] = False
            return True
    else:
        self.logger.info("Out of follows for today.")
    return False


def follow_users(self, results, bot):
    broken_items = []
    user_ids = []
    medias = []
    skipped = self.skipped_file
    followed = self.followed_file
    unfollowed = self.unfollowed_file
    following = self.following_file
    followers = self.followers_file
    if self.reached_limit('follows'):
        self.logger.info("Out of follows for today.")
        return
    for line in results:
        splitLine = line.split(':')
        user_id = splitLine[0]
        if user_id not in skipped.set and user_id not in followed.set and user_id not in unfollowed.set and user_id not in following.set and user_id not in followers.set:
            user_ids.append(splitLine[0])
            if len(splitLine) > 3:
                medias.append([splitLine[1], splitLine[2], splitLine[3]])
            else:
                medias.append([])

    msg = "Going to follow {} users.".format(len(user_ids))
    self.logger.info(msg)
    skipped = self.skipped_file
    followed = self.followed_file
    unfollowed = self.unfollowed_file
    self.console_print(msg, "green")

    # Remove skipped and already followed and unfollowed list from user_ids
    user_ids = list(
        set(user_ids) - skipped.set - followed.set - unfollowed.set
    )
    user_ids = user_ids[:nfollows] if nfollows else user_ids
    msg = (
        "After filtering followed, unfollowed and "
        "`{}`, {} user_ids left to follow."
    ).format(skipped.fname, len(user_ids))
    self.console_print(msg, "green")
    for user_id in tqdm(user_ids, desc="Processed users"):
        if self.reached_limit("follows"):
            self.logger.info("Out of follows for today.")
            break
        random_sleep = round(random.uniform(40, 120), 2)
        if random.randint(1,10) == 10:
            watch_random_stories(bot, idx, user_ids)
        if not self.follow(user_ids[idx]):
            random_sleep = round(random.uniform(3, 5), 2)
            if self.api.last_response.status_code == 404:
                self.console_print(
                    "404 error user {user_id} doesn't exist.", "red"
                )
                broken_items.append(user_id)

            elif self.api.last_response.status_code == 200:
                broken_items.append(user_ids[idx])
                continue

            elif self.api.last_response.status_code not in (400, 429):
                # 400 (block to follow) and 429 (many request error)
                # which is like the 500 error.
                try_number = 3
                error_pass = False
                for _ in range(try_number):
                    time.sleep(60)
                    error_pass = self.follow(user_ids[idx])
                    if error_pass:
                        break
                if not error_pass:
                    self.error_delay()
                    i = user_ids.index(user_ids[idx])
                    broken_items += user_ids[i:]
                    break
        if medias[idx]:
            sampling = random.sample(medias[idx], random.randint(1,3))
            bot.like_medias(sampling, False)
        self.logger.info("Waiting for {} sec...".format(random_sleep))
        time.sleep(random_sleep)
    self.logger.info("DONE: Followed {} users in total.".format(self.total['follows']))
    return broken_items


def watch_random_stories(bot, idx, user_ids):
    if bot.api.get_user_feed(user_ids[idx]):
        if bot.api.last_json["items"]:
            user_media = random.choice(bot.api.last_json["items"])
    else:
        print("Can't get feed of user_id=%s" % user_ids[idx])
        return True
    if user_media:
        if not bot.api.get_media_likers(media_id=user_media["pk"]):
            bot.logger.info(
                "Can't get media likers of media_id='%s' by user_id='%s'"
                % (user_media["id"], user_ids[idx])
            )
            return True
    likers = bot.api.last_json["users"]
    liker_ids = [
                    str(u["pk"])
                    for u in likers
                    if not u["is_private"] and "latest_reel_media" in u
                ][:10]
    if bot.watch_users_reels(liker_ids):
        bot.logger.info("Total stories viewed: %d" % bot.total["stories_viewed"])


def follow_followers(self, user_id, nfollows=None):
    self.logger.info("Follow followers of: {}".format(user_id))
    if self.reached_limit("follows"):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    followers = self.get_user_followers(user_id, nfollows)
    followers = list(set(followers) - set(self.blacklist))
    if not followers:
        self.logger.info(
            "{} not found / closed / has no followers.".format(user_id)
        )
    else:
        self.follow_users(followers[:nfollows])


def follow_following(self, user_id, nfollows=None):
    self.logger.info("Follow following of: {}".format(user_id))
    if self.reached_limit("follows"):
        self.logger.info("Out of follows for today.")
        return
    if not user_id:
        self.logger.info("User not found.")
        return
    followings = self.get_user_following(user_id)
    if not followings:
        self.logger.info(
            "{} not found / closed / has no following.".format(user_id)
        )
    else:
        self.follow_users(followings[:nfollows])


def approve_pending_follow_requests(self):
    pending = self.get_pending_follow_requests()
    if pending:
        for u in tqdm(pending, desc="Approving users"):
            user_id = u["pk"]
            username = u["username"]
            self.api.approve_pending_friendship(user_id)
            if self.api.last_response.status_code != 200:
                self.logger.error("Could not approve {}".format(username))
        self.logger.info("DONE: {} people approved.".format(len(pending)))
        return True


def reject_pending_follow_requests(self):
    pending = self.get_pending_follow_requests()
    if pending:
        for u in tqdm(pending, desc="Rejecting users"):
            user_id = u["pk"]
            username = u["username"]
            self.api.reject_pending_friendship(user_id)
            if self.api.last_response.status_code != 200:
                self.logger.error("Could not approve {}".format(username))
        self.logger.info("DONE: {} people rejected.".format(len(pending)))
        return True

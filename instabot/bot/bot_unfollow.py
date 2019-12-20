from tqdm import tqdm
import time
import random

def unfollow(self, user_id):
    user_id = self.convert_to_user_id(user_id)
    user_info = self.get_user_info(user_id)

    if not user_info:
        self.logger.info("Can't get user_id=%s info" % str(user_id))
        return True  # No user_info

    username = user_info.get("username")

    self.console_print(
        "===> Going to unfollow `user_id`: {} with username: {}".format(
            user_id, username
        )
    )

    if self.check_user(user_id, unfollowing=True):
        return True  # whitelisted user
    if not self.reached_limit("unfollows"):
        if self.blocked_actions["unfollows"]:
            self.logger.warning("YOUR `UNFOLLOW` ACTION IS BLOCKED")
            if self.blocked_actions_protection:
                self.logger.warning(
                    "blocked_actions_protection ACTIVE. "
                    "Skipping `unfollow` action."
                )
                return False
        self.delay("unfollow")
        _r = self.api.unfollow(user_id)
        if _r == "feedback_required":
            self.logger.error("`Unfollow` action has been BLOCKED...!!!")
            if not self.blocked_actions_sleep:
                if self.blocked_actions_protection:
                    self.logger.warning("Activating blocked actions \
                        protection for `Unfollow` action.")
                    self.blocked_actions["unfollows"] = True
            else:
                if self.sleeping_actions["unfollows"] \
                        and self.blocked_actions_protection:
                    self.logger.warning("This is the second blocked \
                        `Unfollow` action.")
                    self.logger.warning("Activating blocked actions \
                        protection for `Unfollow` action.")
                    self.sleeping_actions["unfollows"] = False
                    self.blocked_actions["unfollows"] = True
                else:
                    self.logger.info("`Unfollow` action is going to sleep \
                        for %s seconds." % self.blocked_actions_sleep_delay)
                    self.sleeping_actions["unfollows"] = True
                    time.sleep(self.blocked_actions_sleep_delay)
            return False
        if _r:
            msg = "===> Unfollowed, `user_id`: {}, user_name: {}"
            self.console_print(msg.format(user_id, username), "yellow")
            self.unfollowed_file.append(user_id)
            self.total["unfollows"] += 1
            if user_id in self.following:
                self.following.remove(user_id)
            if self.blocked_actions_sleep \
                    and self.sleeping_actions["unfollows"]:
                self.logger.info("`Unfollow` action is no longer sleeping.")
                self.sleeping_actions["unfollows"] = False
            return True
    else:
        self.logger.info("Out of unfollows for today.")
    return False


def unfollow_users(self, user_ids):
    broken_items = []
    self.logger.info("Going to unfollow {} users.".format(len(user_ids)))
    user_ids = set(map(str, user_ids))
    filtered_user_ids = list(set(user_ids) - set(self.whitelist))
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info(
            "After filtration by whitelist {} users left.".format(
                len(filtered_user_ids)
            )
        )
    for user_id in tqdm(filtered_user_ids, desc="Processed users"):
        if not self.unfollow(user_id):
            self.error_delay()
            i = filtered_user_ids.index(user_id)
            broken_items = filtered_user_ids[i:]
            break
    self.logger.info("DONE: Total unfollowed {} users.".format(
        self.total["unfollows"])
    )
    return broken_items


def unfollow_non_followers(self, n_to_unfollows=None):
    self.logger.info("Unfollowing non-followers.")
    self.console_print(" ===> Start unfollowing non-followers <===", "red")
    non_followers = set(self.following_file) - set(self.followers_file) - self.friends_file.set - \
                    set(self.whitelist_file)
    non_followers = list(non_followers)
    for user_id in tqdm(non_followers[:n_to_unfollows]):
        if self.reached_limit("unfollows"):
            self.logger.info("Out of unfollows for today.")
            break
        self.unfollow(user_id)
    self.console_print(" ===> Unfollow non-followers done! <===", "red")

def unfollow_everyone(self):
    self.unfollow_users(self.following)

def search_noobs(self):
    following = self.get_user_following('276887698')
    friends = self.read_list_from_file('friends.txt')
    pro = self.read_list_from_file('pro-users.txt')
    whitelist = self.read_list_from_file('whitelist.txt')
    mass = self.read_list_from_file('usersMassfollowers.txt')
    noobs = self.read_list_from_file('users-noobs.txt')
    lessfollowers = self.read_list_from_file('users-withLessFollowers.txt')
    for user in following:
        if user not in friends and user not in pro and user not in mass and user not in whitelist and user not in noobs\
                and user not in lessfollowers:
            user_info = self.get_user_info(user)
            time.sleep(5)
            if user_info["media_count"] < 40 or user_info["follower_count"] < 1200 and float(
                    user_info["follower_count"]) / float(user_info["following_count"]) <= 2.2 or user_info[
                "following_count"] == 0 or (
                    user_info["is_business"] == False and float(user_info["follower_count"]) / float(
                    user_info["following_count"]) <= 1.7 and float(user_info["follower_count"]) / float(
                    user_info["following_count"]) >= 1) or (
                    user_info["is_business"] == True and float(user_info["follower_count"]) / float(
                    user_info["following_count"]) <= 1.5 and float(user_info["follower_count"]) / float(
                    user_info["following_count"]) >= 1):
                self.console_print("\n %s is insta-noob!" % user_info["username"])
                nooblist_adder(self, user, user_info["username"])
            elif user_info["follower_count"] < user_info["following_count"]:
                unfollow_adder(self, user, user_info["username"])
            elif user_info["following_count"] > 2500 and user_info["follower_count"] < 10000:
                massfollower_adder(self, user, user_info)
            else:
                prolist_adder(self, user, user_info["username"])

def prolist_adder(self, user, user_id):
    # user_id = self.convert_to_user_id(user_id)
    skipped = self.read_list_from_file('pro-users.txt')
    if user_id not in skipped:
        with open('pro-users.txt', "a") as file:
            self.console_print('\n\033[93m %s is insta-pro... \033[0m'
                               % user_id)
            # Append user_is to the end of skipped.txt
            file.write(str(user) + "\n")
            self.console_print('Done adding %s to pro-users.txt' % user_id)
    return

def unfollow_adder(self, user, user_id):
    # user_id = self.convert_to_user_id(user_id)
    skipped = self.read_list_from_file('users-withLessFollowers.txt')
    if user_id not in skipped:
        with open('users-withLessFollowers.txt', "a") as file:
            self.console_print('\n\033[93m %s is unfollow-user... \033[0m'
                               % user_id)
            # Append user_is to the end of skipped.txt
            file.write(str(user_id) + ":" + str(user) + "\n")
            self.console_print('Done adding %s to users-withLessFollowers.txt' % user_id)
    return

def nooblist_adder(self, user, user_id):
    # user_id = self.convert_to_user_id(user_id)
    skipped = self.read_list_from_file('users-noobs.txt')
    if user_id not in skipped:
        with open('users-noobs.txt', "a") as file:
            self.console_print('\n\033[93m Add user_id %s to NoobsList... \033[0m'
                               % user_id)
            # Append user_is to the end of skipped.txt
            file.write(str(user_id) + ":" + str(user) + "\n")
            self.console_print('Done adding %s to users-noobs.txt' % user_id)
    return

def massfollower_adder(self, user, user_info):
    # user_id = self.convert_to_user_id(user_id)
    skipped = self.read_list_from_file('userMassfollowers-Details.txt')
    if user_info["username"] not in skipped:
        with open('usersMassfollowers-Details.txt', "a") as file:
            self.console_print('\n\033[93m %s is a Mass Follower! \033[0m'
                               % user_info["username"])
            # Append user_is to the end of skipped.txt
            file.write(
                str(user) + ": " + user_info["username"] + " : " + str(user_info["follower_count"]) + " : " + str(
                    user_info["following_count"]) + "\n")
            self.console_print('Done adding %s to userMassfollowers-Details' % user_info["username"])
        with open('usersMassfollowers.txt', "a") as file:
            # Append user_is to the end of skipped.txt
            file.write(str(user) + "\n")
    return

def delete_requests(self, users):
    broken_items = []
    self.logger.info("Going to unrequest %d users." % len(users))
    user_ids = []
    for user in users:
        user_id = self.convert_to_user_id(user)
        user_ids.append(user_id)
        time.sleep(1)
    user_ids = set(map(str, user_ids))
    myFollowers = self.read_list_from_file('myFollowers.txt')
    filtered_user_ids = list(set(user_ids) - set(myFollowers))
    self.total_unfollowed = 0
    if len(filtered_user_ids) != len(user_ids):
        self.logger.info(
            "After filtration by whitelist %d users left." % len(filtered_user_ids))
    for user_id in tqdm(filtered_user_ids, desc='Processed users'):
        user_info = self.get_user_info(user_id)
        if not user_info:
            continue
        if self.block(user_id):
            self.console_print('\033[93m===> BLOCKED , user_id: %s , user_name: %s \033[0m\n' % (
                user_id, user_info["username"]))
            self.total_unfollowed += 1
            time.sleep(round(random.uniform(5, 10), 2))
        if self.unblock(user_id):
            self.console_print('\033[93m===> UN-BLOCKED , user_id: %s , user_name: %s \033[0m\n' % (
                user_id, user_info["username"]))
            time.sleep(round(random.uniform(5, 10), 2))
        else:
            return False
    self.logger.info("DONE: Total unrequested %d users. " %self.total_unfollowed)
    return broken_items

def unfollow_usersWithLessFollowers(self):
    users = self.read_list_from_file('users-withLessFollowers.txt')
    users_ids = []
    for user in users:
        users_ids.append(user.split(":")[1])
    self.unfollow_users(users_ids)

def unrequest_users(self):
    requests = self.read_list_from_file('requests.txt')
    self.delete_requests(requests)
import datetime
import os
import tqdm

def get_tsv_line(dictionary):
    line = ""
    for key in sorted(dictionary):
        line += str(dictionary[key]) + "\t"
    return line[:-1] + "\n"


def get_header_line(dictionary):
    line = "\t".join(sorted(dictionary))
    return line + "\n"


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory) and directory:
        os.makedirs(directory)


def dump_data(data, path):
    ensure_dir(path)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(get_header_line(data))
            f.write(get_tsv_line(data))
    else:
        with open(path, "a") as f:
            f.write(get_tsv_line(data))


def save_user_stats(self, username, path=""):
    if not username:
        username = self.api.username
    user_id = self.convert_to_user_id(username)
    infodict = self.get_user_info(user_id, use_cache=False)
    if infodict:
        data_to_save = {
            "date": str(datetime.datetime.now().replace(microsecond=0)),
            "followers": int(infodict["follower_count"]),
            "following": int(infodict["following_count"]),
            "medias": int(infodict["media_count"]),
        }
        file_path = os.path.join(path, "%s.tsv" % username)
        dump_data(data_to_save, file_path)
        self.logger.info("Stats saved at %s." % data_to_save["date"])
    return False

def analyze_media(self, username, amount, filtration = False):
    if not username:
        return False
    user_id = self.convert_to_user_id(username)
    medias = self.get_last_user_medias(user_id, amount)
    if not medias:
        self.logger.info(
            "None medias received: account is closed or medias have been filtered."
        )
        return False
    for media in medias:
        media_info = self.get_media_info(media)
        if media_info[0]["usertags"]:
            for t in media_info[0]["usertags"]["in"]:
                tag = t["user"]["username"]
                tags_adder(self, tag)
        text = media_info[0]["caption"]["text"] if media_info[0]["caption"] else ""
        quotes_adder(self, text)
    return False

def tags_adder(self, tag):
    tags = self.read_list_from_file('tags.txt')
    if tag not in tags:
        with open('tags.txt', "a") as file:
            self.console_print('\n\033[93m Add tag %s to Tags... \033[0m'
                               % tag)
            file.write(str(tag) + "\n")
            self.console_print('Done adding %s to tags.txt' % tag)
    return

def quotes_adder(self, quote):
    caption = self.read_list_from_file('quotes.txt')
    with open('quotes.txt', "a") as file:
        file.write(quote.encode('utf-8') + "\n" + "\n" + "*******************" + "\n" + "\n")
        self.console_print('Done adding to quotes.txt')
    return
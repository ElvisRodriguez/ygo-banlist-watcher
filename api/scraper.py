from bs4 import BeautifulSoup
from dotenv import dotenv_values
import hashlib
import requests

from path_resolver import get_full_path


CONFIG = dotenv_values(get_full_path(__file__, ".env"))


def get_banlist_data():
    response = requests.get(CONFIG["URL"])
    soup = BeautifulSoup(response.content, features="html.parser")
    javascript_tags = soup.select("script")
    banlist_tag, *_ = [tag for tag in javascript_tags if "Forbidden" in str(tag)]
    banlist_data = str(banlist_tag)
    return banlist_data


def check_previous_banlist_data(banlist_data):
    hash_data = hashlib.md5(banlist_data.encode())
    with open(get_full_path(__file__, "hashed_banlist_data.txt"), 'r') as file:
        previous_hash_data = file.readline().strip('\n')
        if hash_data.hexdigest() != previous_hash_data:
            print("Banlist Changed!")
            with open(get_full_path(__file__, "hashed_banlist_data.txt"), 'w') as file:
                file.write(hash_data.hexdigest())


if __name__ == "__main__":
    print("Checking banlist...")
    banlist_data = get_banlist_data()
    check_previous_banlist_data(banlist_data)
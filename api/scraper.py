import json
import unicodedata

from bs4 import BeautifulSoup
from dotenv import dotenv_values
import requests

CONFIG = dotenv_values(".env")

def get_card_data():
    """Scrape all card rows from current Yugioh F&L list tables

    Args:
        None
    Returns:
        cards (list iterator): All <tr> tags scraped from official YuGiOh page.
    """
    response = requests.get(CONFIG["URL"])
    soup = BeautifulSoup(response.content, features="html5lib")
    table_rows = [
        table_row for table_row in soup.select("[class^='cardlist']")]
    cards = list(filter(
        lambda tr: "cardlist_atitle" not in tr.attrs["class"], table_rows))
    return cards

def parse_card_name(card_name):
    """Remove unecessary whitespace and uppercasing from card's name.

    Args:
        card_name (str): Raw name of currently processed yugioh card.
    Returns:
        parsed_card_name (str): Parsed or "prettified" card name.
    """
    raw_words = card_name.lower().split(' ')
    non_empty_words = list(filter(lambda word: word != "", raw_words))
    parsed_card_name = ' '.join([word.title() for word in non_empty_words])
    return parsed_card_name 

def parse_card_type(card_type):
    """Parse card's type so that it matches one of json object's primary keys.

    Args:
        card_type (str): The type of yugioh card (monster, spell, trap).
    Returns:
        parsed_card_type (str): One of these strings:
            - monsters, spells, traps
    """
    lowercase_card_type = card_type.lower()
    # monster cards have sub types, presented as "monster/<subtype>"
    if "/" in lowercase_card_type:
        lowercase_card_type = "monster"
    parsed_card_type = f"{lowercase_card_type}s"
    return parsed_card_type

def is_new_list_change(raw_card_data):
    """

    Args:
        raw_card_data ([type]): [description]
    """
    card_data = list(map(
        lambda data: unicodedata.normalize("NFC", data), raw_card_data))
    if len(card_data[-1].strip()) != 0:
        return True
    return False

def process_cards(cards, short_list=False):
    """Processes each <tr> tag's children and extracts relevant card data.

    Args:
        cards (list iterator): All <tr> tags scraped from official YuGiOh page.
        short_list (bool): Flag; process only cards whose list status changed.
    Returns:
        banlist(dict): Current Yu-Gi-Oh F&L list in JSON format.
    """
    with open(CONFIG["TEMPLATE"], 'r') as banlist_template:
        banlist = json.load(banlist_template)
    for card in cards:
        card_type, card_name, status, *other = [
            td.text for td in card.findAll("td")]
        status = status.lower()
        card_type = parse_card_type(card_type)
        card_name = parse_card_name(card_name)
        if short_list:
            if is_new_list_change(other):
                banlist[status][card_type].append(card_name)
        else:
            banlist[status][card_type].append(card_name)
    return banlist


if __name__ == "__main__":
    cards = get_card_data()
    banlist = process_cards(cards)
    with open("banlist.json", 'w') as _banlist:
        json.dump(banlist, _banlist, indent=4)
    short_banlist = process_cards(cards, short_list=True)
    with open("short_banlist.json", 'w') as short_list:
        json.dump(short_banlist, short_list, indent=4)
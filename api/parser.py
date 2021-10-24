import json
import unicodedata

from dotenv import dotenv_values

from path_resolver import get_full_path
from scraper import BanlistScraper


CONFIG = dotenv_values(get_full_path(__file__, ".env"))


def parse_card_name(card_name):
    """Remove unecessary whitespace and uppercasing from card's name.

    Args:
        card_name (str): Raw name of currently processed yugioh card.
    Returns:
        parsed_card_name (str): Parsed or "prettified" card name.
    """
    raw_words = card_name.lower().split(' ')
    non_empty_words = list(filter(lambda word: word != '', raw_words))
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


def parse_update_text(update_text):
    """Extracts date from update text

    Args:
        update_text (str): Text of the form "UPDATED: MM/DD/YYYY".
    Returns:
        update_date (str): Date from update text in "YYYY-MM-DD" format.
    """
    useless_text, date = update_text.split(' ')
    date_components = date.split('/')
    padded_date = list(map(
        lambda component: "{:0>2}".format(component), date_components))
    month, day, year = padded_date
    update_date = f"{year}-{month}-{day}"
    return update_date


def is_new_list_change(raw_card_data):
    """Check if a card was recently added to or changed on the banlist.

    Args:
        raw_card_data (list: str): Unused columns extracted from page table.
    Returns:
        (bool): True only if the last table column has a non empty remark (str).
    """
    card_data = list(map(
        lambda data: unicodedata.normalize("NFC", data), raw_card_data))
    # Empty remarks are variable length strings consisting only of spaces.
    remark = card_data[-1].strip()
    # If the remark is not stripped down to an empty string, it's a new change.
    new_list_change = len(remark) != 0
    return new_list_change


def process_cards(cards, short_list=False):
    """Processes each <tr> tag's children and extracts relevant card data.

    Args:
        cards (list iterator): All <tr> tags scraped from official YuGiOh page.
        short_list (bool): Flag; process only cards whose list status changed.
    Returns:
        banlist(dict): Current Yu-Gi-Oh F&L list in JSON format.
    """
    template_path = get_full_path(__file__, CONFIG["TEMPLATE"])
    with open(template_path, 'r') as banlist_template:
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
    banlist_scraper = BanlistScraper()
    update_text = banlist_scraper.get_update_text()
    update_date = parse_update_text(update_text)
    cards = banlist_scraper.get_card_data()
    banlist = process_cards(cards)
    banlist_path = get_full_path(__file__, "banlist.json")
    with open(banlist_path, 'w') as _banlist:
        json.dump(banlist, _banlist, indent=4)
    short_banlist = process_cards(cards, short_list=True)
    shortlist_path = get_full_path(__file__, "short_banlist.json")
    with open(shortlist_path, 'w') as short_list:
        json.dump(short_banlist, short_list, indent=4)
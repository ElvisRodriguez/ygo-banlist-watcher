from os import set_blocking
import time

from dotenv import dotenv_values, set_key

import parser
from path_resolver import get_full_path
from scraper import BanlistScraper


CONFIG = dotenv_values(get_full_path(__file__, ".env"))
SECONDS = 300


def is_banlist_updated(banlist_scraper):
    """Checks if the banlist was updated and saves the date if so.

    Args:
        banlist_scraper(BanlistScraper):
            - Data scraper object that scrapes data from banlist.
    Returns:
        (bool): True if and only if the banlist was update today.
    """
    update_text = banlist_scraper.get_update_text()
    last_banlist_update = parser.parse_update_text(update_text)
    if CONFIG["LAST_BANLIST_DATE"] != last_banlist_update:
        set_key(
            get_full_path(__file__, ".env"),
            "LAST_BANLIST_DATE",
            last_banlist_update)
        return True
    return False


if __name__ == "__main__":
    while True:
        print("Scraping Yu-Gi-Oh official F&L list page...")
        banlist_scraper = BanlistScraper()
        if is_banlist_updated(banlist_scraper):
            print("Banlist update detected!")
            cards = banlist_scraper.get_card_data()
            print("Processing cards...")
            banlist = parser.process_cards(cards)
            short_banlist = parser.process_cards(cards, short_list=True)
            print("Saving banlist data...")
            parser.save_banlist_data(banlist, "banlist.json")
            parser.save_banlist_data(short_banlist, "short_banlist.json")
            print("Banlist data Saved!")
            break
        else:
            print(f"No updates detected. Sleeping for {SECONDS} seconds")
        time.sleep(SECONDS)
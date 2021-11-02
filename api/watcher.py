from datetime import datetime
import time

import parser
from scraper import BanlistScraper

SECONDS = 10

def is_banlist_updated(banlist_scraper):
    """Check if the banlist was updated today.

    Args:
        banlist_scraper(BanlistScraper):
            - Data scraper object that scrapes data from banlist.
    Returns:
        (bool): True if and only if the banlist was update today.
    """
    update_text = banlist_scraper.get_update_text()
    last_banlist_update = parser.parse_update_text(update_text)
    current_date = str(datetime.date(datetime.today()))
    return current_date == last_banlist_update


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
            break
        else:
            print(f"No updates detected. Sleeping for {SECONDS} seconds")
        time.sleep(SECONDS)
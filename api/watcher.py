from datetime import datetime

import parser
from scraper import BanlistScraper


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
    banlist_scraper = BanlistScraper()
    print(is_banlist_updated(banlist_scraper))
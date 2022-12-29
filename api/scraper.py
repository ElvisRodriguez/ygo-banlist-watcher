from bs4 import BeautifulSoup
from dotenv import dotenv_values
import requests

from path_resolver import get_full_path

CONFIG = dotenv_values(get_full_path(__file__, ".env"))

class BanlistScraper(object):
    def __init__(self):
        response = requests.get(CONFIG["URL"])
        self.soup = BeautifulSoup(response.content, features="lxml")
    
    def get_update_text(self):
        """Scrape the text containing the date of the last banlist update.

        Args:
            None.
        Returns:
            update_text(str): text of the form "UPDATED: MM/DD/YYYY".
        """
        raw_update_date = self.soup.select(".update_ttl")
        update_text = raw_update_date[0].text 
        return update_text
    
    def get_card_data(self):
        """Scrape all card rows from current Yugioh F&L list tables.

        Args:
            None.
        Returns:
            cards (list iterator): All <tr> tags scraped from banlist page.
        """
        table_rows = [
            table_row for table_row in self.soup.select("[class^='cardlist']")]
        cards = list(filter(
            lambda tr: "cardlist_atitle" not in tr.attrs["class"], table_rows))
        return cards

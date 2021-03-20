from ..utils import Scrape


def run():
    scrape_object = Scrape("https://www.topmba.com/emba-rankings/global/2018")
    scrape_object.get_list_of_universities()

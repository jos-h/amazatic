from bs4 import *
import requests
from pprint import pprint


class Scrape:
    def __init__(self, url):
        self.url = url

    def get_request_data(self):
        response = requests.get(self.url)
        return response.content if response.status_code == 200 else None

    def get_list_of_universities(self):
        data = self.get_request_data()

        if data:
            soup = BeautifulSoup(data, features="html.parser")
            # table_data = soup.find(class_="tab-pane tab-pane_js active")
            s = soup.find("div", {"id": "ranking-data-load"})
            # ss = s.findAll("div")
            pprint(s)

    def store_data_db(self):
        pass

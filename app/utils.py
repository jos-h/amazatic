from bs4 import *
import requests
from .models import University
from .serializers import *
from requests_html import HTMLSession
import re


class Scrape:
    def __init__(self, url):
        self.url = url
        self.xhr_request = 'https://www.topmba.com/sites/default/files/qs-rankings-data/en/330380.txt?1616404771?v=1616434965946'
        self.session = HTMLSession()
        self.new_url = re.findall(r"\w+://\w+.\w+.\w+/", url)[0]

    def get_request_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data_response = requests.get(self.xhr_request)
            if data_response.status_code == 200:
                r = self.session.get(self.xhr_request)
                college_links = []
                for i in r.html.links:
                    e = i.replace("\\", "")
                    e = e.replace('"', "")
                    if e not in college_links:
                        college_links.append(e)
                return data_response.json(), college_links

    def get_list_of_universities(self):
        request_data, college_links = self.get_request_data()
        try:
            if 'data' in request_data:
                self.store_data_db(request_data['data'], college_links)
        except KeyError as ke:
            print(ke.args)

    def store_data_db(self, response_dict, college_links):
        try:
            pattern_1 = r'<a[^>]*>(.*?)</a>'
            pattern_2 = r'/\w+/\w+-\w+'
            for each in response_dict:
                each.update(rank=each['rank_display'],
                            city=each['city'], country=each['country']
                            )
                if 'title' in each:
                    title = each['title']
                    link = re.findall(pattern_2, title)
                    name = re.findall(pattern_1, title)
                    if name:
                        name = name[0]
                        each.update(name=name)
                    if link:
                        link = link[0]
                        url = self.new_url + "/" + link
                        each.update(link_program_highlights=url+"#profile-avail-program")
                # serializer = UniversitySerializer(each)
                # if serializer.is_valid(raise_exception=True):
                #     serializer.save()
                self.fetch_program_highlights(url, each)
                break
        except Exception as e:
            print(e.args)

    def fetch_program_highlights(self, url, each):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            div_section = soup.find("div", {"class": 'view view-department-programs view-id-department_programs view-display-id-block_1'})
            # print(div_section)
            a_tag = div_section.find_all("a", href=True)
            program_links = [self.new_url + a['href'] for a in a_tag]
            print(program_links)
            self.fetch_details(program_links)

    def fetch_details(self, program_links):
        for link in program_links:
            soup = BeautifulSoup(requests.get(link).content, "html.parser")
            data = soup.find("div", {"class": "uni-info _norborder-bottom-mobile"})
            print(data)
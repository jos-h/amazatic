from ...utils import Scrape
from django.core.management.base import BaseCommand
from ...serializers import UserSerializer


class Command(BaseCommand):
    help = "Seed data of users"
    '''
    To create admin users using seed data by running
    python manage.py seed_data
    '''
    def handle(self, *args, **options):
        self.stdout.write("seed data")
        run_seed(self, options)
        self.stdout.write("done")


def run_seed(self, mode):
    scrape_object = Scrape("https://www.topmba.com/emba-rankings/global/2018")
    scrape_object.get_list_of_universities()

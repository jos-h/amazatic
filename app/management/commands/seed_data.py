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


def create_admin_users(user_dict):
    serializer = UserSerializer(data=user_dict)
    if serializer.is_valid(raise_exception=True):
        serializer.save()


def run_seed(self, mode):
    user_list = [
        {"username": "denis@gmail.com", "email": "denis@gmail.com", "password": "Kunal@1234",
         "full_name": "Denis Ritchie", "phone": "9762745422", "pin_code": 411028, "is_superuser": True
         },
        {"username": "john@gmail.com", "email": "john@gmail.com", "password": "john@1234",
         "full_name": "John Rambo", "phone": "8888888888", "pin_code": 400028, "is_superuser": True
         },
        {"username": "guido@gmail.com", "email": "guido@gmail.com", "password": "guido@1234",
         "full_name": "Guido Van Rossum", "phone": "8855447723", "pin_code": 410128, "is_superuser": True
         }
    ]
    for user_dict in user_list:
        create_admin_users(user_dict)

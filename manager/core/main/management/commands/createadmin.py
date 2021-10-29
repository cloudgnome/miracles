from django.core.management.base import BaseCommand, CommandError
from user.models import User
from getpass import getpass

class Command(BaseCommand):
    help = 'Create Super User'

    def handle(self, *args, **options):
        try:
            User.objects.get(name='Администратор',is_admin=True)
            print('User already exists.')
        except User.DoesNotExist:
            password = getpass('Enter password: ')
            user = User.objects.create(name='Администратор',is_admin=True)
            user.set_password(password)
            user.save()
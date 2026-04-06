from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create the app user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'prateek'       # ← change this to whatever you want
        password = 'yourpassword'  # ← change this to whatever you want
        email = 'b23bb1033@iitj.ac.in'  # ← change this

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'User "{username}" already exists.')
        else:
            User.objects.create_superuser(username=username, password=password, email=email)
            self.stdout.write(f'User "{username}" created successfully.')
from django.core.management.base import BaseCommand
from tenants_manager.models import Admin

class Command(BaseCommand):
    help = 'Create a public admin user'

    def handle(self, *args, **options):
        email = input("Email: ")
        username = input("Username: ")
        password = input("Password: ")
        Admin.objects.create_superuser(email=email, username=username, password=password)
        print("✅ Admin created successfully!")

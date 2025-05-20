from django.core.management.base import BaseCommand
from django.conf import settings
from users.models import UserProfile


class Command(BaseCommand):
    help = "Create missing UserProfile instances for existing users."

    def handle(self, *args, **kwargs):
        users_without_profiles = settings.AUTH_USER_MODEL.objects.filter(
            profile__isnull=True
        )
        for user in users_without_profiles:
            UserProfile.objects.create(user=user)
            self.stdout.write(f"Created profile for user {user.username}")
        self.stdout.write("Missing profiles created successfully.")

from django.core.management.base import BaseCommand
# from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings

# https://eli.thegreenplace.net/2014/02/15/programmatically-populating-a-django-database


# $ python manage.py populate_db
class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'Seeding Fake User Data'

    # Update Django Site

    def _update_default_site(self):
        qs = Site.objects.filter(domain__iexact='example.com')
        if qs.exists():
            qs.update(domain='https://localhost:8000/', name='bdonor.com')

    # Create Social App
    def _create_social_app(self):
        qs = SocialApp.objects.filter(provider__iexact='facebook')
        if not qs.exists():
            site_qs = Site.objects.filter(
                domain__iexact='https://localhost:8000/')
            if site_qs.exists():
                if settings.DEBUG:
                    client_id = settings.FACEBOOK_CLIENT_ID_DEV
                    secret = settings.FACEBOOK_SECRET_KEY_DEV
                else:
                    client_id = settings.FACEBOOK_CLIENT_ID_PROD
                    secret = settings.FACEBOOK_SECRET_KEY_PROD
                instance = SocialApp.objects.create(
                    provider='facebook', name='Facebook', client_id=client_id, secret=secret)
                instance.sites.set(site_qs)

    # Create Users

    def _create_users(self):
        # Default Users
        if not User.objects.filter(username__iexact='darkstarnmn').exists():
            u_dark = User(username='darkstarnmn',
                          email='darkstarnmn@gmail.com')
            u_dark.set_password("test12345")
            u_dark.save()
        if not User.objects.filter(username__iexact='test').exists():
            u_test = User(username='test',
                          email='test@user.com')
            u_test.set_password("test12345")
            u_test.save()

    def handle(self, *args, **options):
        self._update_default_site()
        self._create_social_app()
        self._create_users()

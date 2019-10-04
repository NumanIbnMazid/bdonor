
import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonor.settings.development')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonor.settings.pythonanywhere')

application = get_wsgi_application()

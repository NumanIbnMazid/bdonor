
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonar.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonar.settings.pythonanywhere')

application = get_wsgi_application()

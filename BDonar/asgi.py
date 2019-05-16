
import os
import django
from channels.routing import get_default_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonar.settings.development')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDonar.settings.pythonanywhere')

django.setup()

application = get_default_application()

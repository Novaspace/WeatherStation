"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import sys
import django
from channels.routing import get_default_application

sys.path.append("/home/pi/Dev/WeatherStation")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WeatherStation.settings")
django.setup()
application = get_default_application()

"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from backend.configurations.setup_python_path import setup_python_path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

setup_python_path()

application = get_wsgi_application()

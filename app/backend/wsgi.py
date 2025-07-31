"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import sentry_sdk
from configurations.django_config_parser import django_configs
from django.core.wsgi import get_wsgi_application

from backend.configurations.setup_python_path import setup_python_path

setup_python_path()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

sentry_sdk.init(
    dsn=django_configs.get("Sentry", "SENTRY_DSN"),
)

application = get_wsgi_application()

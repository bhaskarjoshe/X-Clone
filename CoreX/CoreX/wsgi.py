"""
WSGI config for CoreX project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CoreX.settings")

import os

if os.getenv("RUNNING_CELERY") != "true":
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

"""
ASGI config for CoreX project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CoreX.settings")

if os.getenv("RUNNING_CELERY") != "true":
    from django.core.asgi import get_asgi_application
    application = get_asgi_application()
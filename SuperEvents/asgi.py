"""
ASGI config for petr_ondra_patrik_finalni_projakt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petr_ondra_patrik_finalni_projakt.settings')

application = get_asgi_application()

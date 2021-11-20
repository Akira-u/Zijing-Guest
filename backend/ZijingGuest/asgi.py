"""
ASGI config for ZijingGuest project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import guard.routing
from guard.consumers import MyConsumer
from django.conf.urls import url

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ZijingGuest.settings')
application = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             # guard.routing.websocket_urlpatterns
#             url(r"^guard/ws/$",MyConsumer.as_asgi()),
#         ])
#     ),
# })

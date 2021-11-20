from . import consumers
from django.conf.urls import url

websocket_urlpatterns = [
    url(r'^/guard/ws/(?P<code>[^/]+)/$',consumers.MyConsumer),
]
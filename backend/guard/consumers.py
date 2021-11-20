import json
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import guard.wx_api
class MyConsumer(WebsocketConsumer):
    def connnect(self):
        log_info = code2Session(appId = guest_appId, appSecret = guest_appSecret, code = self.scope["url_route"]["kwargs"]["code"])
        self.conn_id = log_info.get("open_id")
        self.gourp_id = log_info.get("open_id")
        self.channel_layer.group_add(
            self.group_id,
            self.conn_id
        )
        # self.accpet()
        # print("connecting ",self.conn_id)
    def disconnect(self):
        self.channel_layer.group_discard(
            self.group_id,
            self.conn_id
        )

def notice(conn_id,msg):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(conn_id,msg)
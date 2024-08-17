from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class NotificationConsumer (WebsocketConsumer) :

    def connect(self):
        
        self.accept()
        self.user = self.scope['user']

        if self.user.is_anonymous:
            self.close()
            raise
        

        self.GROUP_NAME = f'notification__{self.user.id}'
        async_to_sync(self.channel_layer.group_add)(
            self.GROUP_NAME,
            self.channel_name,
        )


    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.GROUP_NAME,
            self.channel_name,
        )


    def notification (self, data):
        self.send(text_data=json.dumps(data['data']))
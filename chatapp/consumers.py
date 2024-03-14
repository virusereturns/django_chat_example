from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Code to handle connection establishment
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )  # Adds the user to the group
        await self.accept()  # Awaits the WebSocket connection

    async def disconnect(self, close_code):
        # Code to handle connection closure
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Code to handle incoming messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room = text_data_json['room']

        await self.channel_layer.group_send(
            self.room_group_name, # Sends the message to the group
            {
                'type': 'send_message',
                'message': message,
                'username': username,
                'room': room
            }
        )

    async def send_message(self, event):
        # Code to send messages to the client
        message = event['message']
        username = event['username']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room
        }))

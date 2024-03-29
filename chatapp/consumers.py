import json

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.timezone import now

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Room, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Code to handle connection establishment
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # Adds the user to the group
        await self.accept()  # Awaits the WebSocket connection

    async def disconnect(self, close_code):
        # Code to handle connection closure
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # Code to handle incoming messages
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        room = text_data_json['room']

        await self.channel_layer.group_send(
            self.room_group_name,  # Sends the message to the group
            {'type': 'send_message', 'message': message, 'username': username, 'room': room},
        )
        await self.save_message(username, message, room)

    async def send_message(self, event):
        # Code to send messages to the client
        message = event['message']
        username = event['username']
        created_str = now()

        # Context data to pass to the template
        context = {'message': message, 'username': username, 'created': created_str}

        # Render the chat message to an HTML string
        message_html = render_to_string('components/message.html', context)

        await self.send(text_data=json.dumps({'html': message_html}))

    @sync_to_async
    def save_message(self, username, message, room):
        user = User.objects.get(username=username)
        chatroom = Room.objects.get(slug=room)
        ChatMessage.objects.create(user=user, message=message, room=chatroom)

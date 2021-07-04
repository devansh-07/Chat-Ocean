import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Contact, Message, Chat
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):
    def get_our_chat(user, friend):
        for chat in user.chats.all():
            if friend in chat.members.all():
                return chat

    def fetch(self, data):
        user = User.objects.get(username=data['user']).contacts.first()

        if not data['friend']:
            return []

        friend = User.objects.get(username=data['friend']).contacts.first()
        all_messages = ChatConsumer.get_our_chat(user, friend).messages.all()

        return self.to_json(all_messages)

    def to_json(self, messages):
        result = []
        for message in messages:
            result.append(self._msg_to_json(message))

        return result

    def _msg_to_json(self, message):
        return {
            'author': message.contact.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }

    def new_message(self, data):
        author = data['from']
        receiver = data['to']
        author_user = User.objects.filter(username=author).first().contacts.first()
        receiver_user = User.objects.filter(username=receiver).first().contacts.first()

        message = Message.objects.create(
            contact = author_user,
            content = data['message']
        )

        chat = ChatConsumer.get_our_chat(author_user, receiver_user)
        chat.messages.add(message)

        content = {
            'command': 'new_message',
            'message': self._msg_to_json(message)
        }

        return self.send_message(content)

    commands = {
        'fetch': fetch,
        'message': new_message
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_' + str(self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        command = data['command']

        self.commands[command](self, data)

    def send_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['data']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'data': message
        }))

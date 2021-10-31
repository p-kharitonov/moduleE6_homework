import json
from django.utils import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Account, Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = 'chat_%s' % self.room_id
        user = self.scope["user"]
        is_permit = await self.is_permit(user, self.room_id)
        if is_permit:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_id,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]
        username = str(user)
        created_at = await self.create_message(user, self.room_id, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'created_at': created_at
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        created_at = event['created_at']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'created_at': created_at
        }))

    @database_sync_to_async
    def get_account(self, user):
        return Account.objects.get(user=user)

    @database_sync_to_async
    def is_permit(self, user, room_id):
        account = Account.objects.get(user=user)
        room = Room.objects.get(pk=room_id)
        return room.members.filter(pk=account.pk).exists()

    @database_sync_to_async
    def create_message(self, user, room_id, content):
        account = Account.objects.get(user=user)
        room = Room.objects.get(pk=room_id)
        message = Message.objects.create(author=account, room=room, content=content)

        timestamp_raw = timezone.now()  # current time, or use whatever time you have
        date_format = '%Y-%m-%d %H:%M:%S'  # time format day-month-year hour:minutes:seconds
        timestamp = timezone.datetime.strftime(timestamp_raw, date_format)
        class_date = timezone.localtime(message.created_at)

#       Поправить выбор TimeZOne
        tz = timezone.get_default_timezone()
        created_at = message.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S')
        return created_at


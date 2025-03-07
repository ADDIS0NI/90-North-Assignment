import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the chat room group
        self.room_group_name = 'chat_room'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}")
        
        # Send previous messages
        messages = await self.get_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'user_email': message['sender_email'],
                'timestamp': message['timestamp']
            }))

    async def disconnect(self, close_code):
        # Leave the chat room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} with code {close_code}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '')
            
            # Get user
            user = self.scope["user"]
            user_email = user.email if user.is_authenticated else "Anonymous"
            
            # Save message to database if user is authenticated
            if user.is_authenticated:
                await self.save_message(user, message)
            
            # Send message to the chat room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_email': user_email
                }
            )
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid message format'
            }))
        except Exception as e:
            print(f"Error in receive: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'An error occurred processing your message'
            }))
    
    # Receive message from the chat room group
    async def chat_message(self, event):
        message = event['message']
        user_email = event['user_email']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user_email': user_email
        }))
    
    @database_sync_to_async
    def save_message(self, user, message):
        return Message.objects.create(sender=user, content=message)
    
    @database_sync_to_async
    def get_messages(self):
        messages = Message.objects.all().order_by('-timestamp')[:50]
        return [
            {
                'content': message.content,
                'sender_email': message.sender.email,
                'timestamp': message.timestamp.isoformat()
            }
            for message in reversed(messages)  # Reverse to show oldest first
        ] 
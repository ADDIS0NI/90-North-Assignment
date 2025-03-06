import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Connection attempt started...")  
        try:
            self.room_group_name = 'test'
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()

            # Send previous messages
            messages = Message.objects.all().order_by('-timestamp')[:50]  # Last 50 messages
            for message in reversed(messages):
                self.send(text_data=json.dumps({
                    'message': message.content,
                    'user_email': message.sender.email,
                    'timestamp': message.timestamp.isoformat()
                }))
            print("Connection accepted successfully!")  
        except Exception as e:
            print(f"Connection error: {str(e)}")  
            raise

    def disconnect(self, close_code):
        print(f"Disconnecting with code: {close_code}")  
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
            print("Disconnected successfully")  
        except Exception as e:
            print(f"Disconnect error: {str(e)}")  

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            user_email = self.scope["user"].email

            # Save message to database
            Message.objects.create(
                sender=self.scope["user"],
                content=message
            )

            print(f"Received message: {message}")  

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user_email' : user_email
                }
            )
        except Exception as e:
            print(f"Error in receive: {str(e)}")  

    def chat_message(self, event):
        try:
            message = event['message']
            user_email = event['user_email']
            self.send(text_data=json.dumps({
                'type': 'chat',
                'message': message,
                'user_email': user_email
            }))
            print(f"Message sent: {message}")  
        except Exception as e:
            print(f"Error in chat_message: {str(e)}")  
from django.conf import settings
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests

class GoogleAuthBackend:
    def authenticate(self, request, token=None):
        try:
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID
            )

            email = idinfo['email']
            name = idinfo.get('name', '')
            
            # Get or create user
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=name.split()[0] if name else ''
                )
            return user
            
        except ValueError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
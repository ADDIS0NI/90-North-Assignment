from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth import exceptions
import os
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
import logging
import secrets

logger = logging.getLogger(__name__)

# Development setting for OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/drive.file'
]

def login_view(request):
    # Clear any existing state and ensure a fresh session
    if 'oauth_state' in request.session:
        del request.session['oauth_state']
    
    # Generate a new state parameter
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    request.session.modified = True
    
    logger.info("Login page accessed")
    return render(request, 'accounts/login.html')

def google_login(request):
    logger.info("Initiating Google login process")
    try:
        flow = Flow.from_client_config(
            settings.GOOGLE_CONFIG,
            scopes=SCOPES,
            redirect_uri=settings.GOOGLE_CONFIG['web']['redirect_uris'][0]  # Add this line
        )
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        
        request.session['google_auth_state'] = state
        return redirect(authorization_url)
    except Exception as e:
        logger.error(f"Google login error: {str(e)}")
        messages.error(request, "Failed to start Google login process")
        return redirect('login')

def google_callback(request):
    logger.info("Processing Google OAuth callback")
    try:
        state = request.session.get('google_auth_state')
        
        flow = Flow.from_client_config(
            settings.GOOGLE_CONFIG,
            scopes=SCOPES,
            state=state,
            redirect_uri=settings.GOOGLE_CONFIG['web']['redirect_uris'][0]
        )
        
        flow.fetch_token(
            authorization_response=request.build_absolute_uri()
        )
        
        credentials = flow.credentials

        # Store credentials in session
        request.session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Verify token and get user info
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10
        )
        
        email = idinfo['email']
        first_name = idinfo.get('given_name', '')
        
        # Get or create user
        try:
            user = User.objects.get(email=email)
            logger.info(f"Existing user logged in: {email}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name
            )
            logger.info(f"New user created: {email}")
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Initialize Drive connection
        request.session['drive_connected'] = True
        
        messages.success(request, f"Welcome {first_name or email}!")
        return redirect('dashboard')
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        messages.error(request, "Authentication failed. Please try again.")
        return redirect('login')

@login_required
def dashboard(request):
    logger.info(f"Dashboard accessed by user: {request.user.email}")
    return render(request, 'accounts/dashboard.html', {
        'user': request.user
    })

def logout_view(request):
    logger.info(f"Logout initiated for user: {request.user.email}")
    logout(request)
    messages.success(request, "You've been successfully logged out!")
    return redirect('home')
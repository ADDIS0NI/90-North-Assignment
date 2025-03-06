from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_drive_service(request):
    """Get Google Drive service using stored credentials"""
    try:
        creds_dict = request.session.get('google_credentials')
        if not creds_dict:
            return None
            
        credentials = Credentials(
            token=creds_dict['token'],
            refresh_token=creds_dict['refresh_token'],
            token_uri=creds_dict['token_uri'],
            client_id=creds_dict['client_id'],
            client_secret=creds_dict['client_secret'],
            scopes=creds_dict['scopes']
        )
        
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        print(f"Error getting Drive service: {str(e)}")
        return None
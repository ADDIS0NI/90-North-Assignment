from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.contrib import messages
from .utils import get_drive_service
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload, MediaIoBaseUpload
import io
import logging

logger = logging.getLogger(__name__)

def get_file_type_info(mime_type):
    """Get file type information and export format"""
    GOOGLE_MIME_TYPES = {
        'application/vnd.google-apps.document': {
            'export_type': 'application/pdf',
            'extension': '.pdf',
        },
        'application/vnd.google-apps.spreadsheet': {
            'export_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'extension': '.xlsx',
        },
        'application/vnd.google-apps.presentation': {
            'export_type': 'application/pdf',
            'extension': '.pdf',
        }
    }
    return GOOGLE_MIME_TYPES.get(mime_type, {'extension': ''})

@login_required
def drive_home(request):
    """Landing page for Google Drive integration"""
    logger.info("Accessing Drive home view")
    context = {
        'drive_connected': request.session.get('drive_connected', False)
    }
    return render(request, 'files/drive_home.html', context)

@login_required
def connect_drive(request):
    """Connect to Google Drive"""
    logger.info("Initiating Drive connection")
    try:
        service = get_drive_service(request)
        
        if not service:
            logger.warning("No Drive service available")
            messages.error(request, "Please login with Google first")
            return redirect('login')
            
        about = service.about().get(fields="user").execute()
        logger.info("Drive connection established")
        
        request.session['drive_connected'] = True
        messages.success(request, "Successfully connected to Google Drive!")
        
        return redirect('drive_home')
        
    except Exception as e:
        logger.error(f"Drive connection error: {str(e)}")
        messages.error(request, "Failed to connect to Google Drive. Please try again.")
        return redirect('drive_home')

@login_required
def upload_file(request):
    """Handle file uploads to Google Drive"""
    logger.info("Starting file upload process")
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            uploaded_file = request.FILES['file']
            logger.info(f"Processing upload: {uploaded_file.name}")

            service = get_drive_service(request)
            if not service:
                logger.error("Drive service unavailable")
                messages.error(request, "Drive service not available. Please reconnect.")
                return redirect('drive_home')

            file_metadata = {'name': uploaded_file.name}
            file_content = uploaded_file.read()
            
            fh = io.BytesIO(file_content)
            media = MediaIoBaseUpload(fh, 
                                    mimetype=uploaded_file.content_type,
                                    resumable=True)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name, webViewLink'
            ).execute()

            logger.info(f"File uploaded successfully: {file.get('name')}")
            messages.success(request, f"File '{file.get('name')}' uploaded successfully!")
            return redirect('drive_home')

        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            messages.error(request, "Upload failed. Please try again.")
            return redirect('drive_home')

    return render(request, 'files/upload.html')

@login_required
def file_list(request):
    """List files from Google Drive"""
    logger.info("Fetching file list")
    try:
        service = get_drive_service(request)
        
        if not service:
            logger.warning("Drive service not available")
            messages.error(request, "Please connect to Google Drive first")
            return redirect('drive_home')
        
        results = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType, webViewLink, createdTime, modifiedTime)",
            orderBy="modifiedTime desc"
        ).execute()
        
        files = results.get('files', [])
        logger.info(f"Retrieved {len(files)} files")

        return render(request, 'files/file_list.html', {'files': files})

    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}")
        messages.error(request, "Failed to fetch files. Please try again.")
        return redirect('drive_home')

@login_required
def download_file(request, file_id):
    """Download files from Google Drive"""
    logger.info(f"Initiating download for file: {file_id}")
    
    try:
        service = get_drive_service(request)
        
        if not service:
            logger.warning("Drive service not available")
            messages.error(request, "Please connect to Google Drive first")
            return redirect('file_list')

        file_metadata = service.files().get(fileId=file_id).execute()
        file_name = file_metadata.get('name', 'downloaded_file')
        mime_type = file_metadata.get('mimeType', 'application/octet-stream')
        
        try:
            request = service.files().get_media(fileId=file_id)
            file_buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(file_buffer, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                
            logger.info("Download completed successfully")
            file_buffer.seek(0)
            
            response = HttpResponse(file_buffer.read(), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            response['Content-Length'] = file_buffer.getbuffer().nbytes
            
            return response

        except Exception as download_error:
            logger.error(f"Download error: {str(download_error)}")
            messages.error(request, "Download failed. Please try again.")
            return redirect('file_list')

    except Exception as e:
        logger.error(f"File access error: {str(e)}")
        messages.error(request, "Failed to access file. Please try again.")
        return redirect('file_list')
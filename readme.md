# DriveConnect: Google Drive & Chat Integration 

## Overview
DriveConnect is a Django-based web application that seamlessly integrates Google OAuth 2.0, Google Drive API, and WebSockets for real-time communication. This project was developed as part of a backend developer assessment to demonstrate proficiency in API integration and real-time web technologies.

## Project Demo  
[Watch the Video](https://youtu.be/MxaneWPl-8Y)




## Key Features

### 🔐 Google Authentication
- Complete OAuth 2.0 flow implementation
- Secure user authentication and session management
- Persistent user sessions with proper token handling

### 📁 Google Drive Integration
- Connect to your Google Drive account
- Upload files directly to your Drive
- Browse and download your Drive files
- Clean UI for file management

### 💬 Real-time Chat
- WebSocket-powered messaging system
- Instant message delivery between users
- Persistent chat history
- User identification in messages

## Tech Stack
- **Backend**: Django 5.1.6
- **WebSockets**: Django Channels
- **Authentication**: Google OAuth 2.0
- **File Storage**: Google Drive API
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Deployment**: Render

## Live Demo
The application is deployed and accessible at:
[https://nine0-north-assignment-jo2o.onrender.com](https://nine0-north-assignment-jo2o.onrender.com)

> **Note**: Since this is a development application, Google OAuth is in testing mode. To access the application I have shifted to production mode for now

## Setup Instructions

### Prerequisites
- Python 3.8+
- Google Cloud Platform account with OAuth credentials
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ADDIS0NI/90-North-Assignment.git
   cd 90-North-Assignment
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**
   Create a `.env` file in the project root with:
   ```
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_PROJECT_ID=your_project_id
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to [http://localhost:8000](http://localhost:8000)

## API Endpoints

### Authentication
- `GET /accounts/login/` - Initiates Google OAuth flow
- `GET /accounts/google/callback/` - OAuth callback endpoint
- `GET /accounts/logout/` - Logs out the current user

### Google Drive
- `GET /files/` - Lists files from Google Drive
- `POST /files/upload/` - Uploads a file to Google Drive
- `GET /files/download/<file_id>/` - Downloads a specific file

### Chat
- `GET /chat/` - Accesses the chat interface
- WebSocket: `ws://<domain>/ws/chat/` - WebSocket endpoint for real-time messaging

## Testing the Application

### Authentication Flow
1. Visit the homepage and click "Login"
2. You'll be redirected to Google's authentication page
3. After successful authentication, you'll be redirected to the dashboard

### Google Drive Integration
1. Navigate to "My Files" in the navigation bar
2. Your Google Drive files will be displayed that you have uploaded from our application
3. Use the upload button to add new files (that will be uploaded in your google drive)
4. Click on any file to download it

### Real-time Chat
1. Navigate to "Chat" in the navigation bar
2. Open another browser or incognito window and log in with a different account
3. Send messages from either window to see real-time communication
4. Refresh the page to see that message history is preserved

## Implementation Details

### Google OAuth Flow
The authentication system implements the complete OAuth 2.0 flow:
- Authorization request with proper scopes
- Token exchange
- User information retrieval
- Session management with token storage

### Google Drive API
The Drive integration uses the Google Drive API v3 to:
- List files with proper pagination
- Upload files with progress tracking
- Download files with proper MIME type handling

### WebSocket Implementation
The chat feature uses Django Channels to:
- Establish persistent WebSocket connections
- Broadcast messages to all connected clients
- Store messages in the database for persistence
- Authenticate WebSocket connections

## Future Enhancements
- File sharing between users
- Group chat functionality
- Direct messaging between users
- Enhanced file management (folders, search)
- Real-time file collaboration
## Contact
For any questions or access requests, please contact me at adityasoni0950@gmail.com.

# I sincerely apologize for the delayed submission of my assignment. Due to time constraints, I prioritized the backend development while ensuring the project maintained its core design aesthetics. I have put in my best  effort to deliver a high-quality solution.
# I would greatly appreciate your feedback on my work, as I am eager to improve and contribute further. Additionally, I am highly interested in this internship with a potential job offer and look forward to any guidance on #how I can enhance my performance.

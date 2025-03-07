# Testing Endpoints with Postman

## Setup

1. Download and install Postman from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. Launch Postman

## Importing the Collection

1. Click on "Import" button in Postman
2. Select the provided `SocialConnect.postman_collection.json` file
3. The collection will be imported with all pre-configured endpoints

## Testing Endpoints

### 1. Authentication Flow

#### Initiate Google Login
- Method: GET
- Endpoint: `{{base_url}}/auth/google/login`
- No parameters required
- This will redirect to Google login page

#### OAuth Callback
- Method: GET
- Endpoint: `{{base_url}}/auth/google/callback`
- Automatically handled after Google login

#### Logout
- Method: GET
- Endpoint: `{{base_url}}/auth/logout`

### 2. Google Drive Operations

#### List Files
- Method: GET
- Endpoint: `{{base_url}}/files`
- Requires authentication
- Returns list of files from Google Drive

#### Upload File
- Method: POST
- Endpoint: `{{base_url}}/files/upload`
- Requires authentication
- Body: form-data
  - Key: `file`
  - Value: Select file to upload

#### Download File
- Method: GET
- Endpoint: `{{base_url}}/files/download/:fileId`
- Requires authentication
- Replace `:fileId` with actual Google Drive file ID

## Environment Setup

1. Create a new Environment in Postman
2. Add variable:
   - `base_url`: Your application URL (e.g., `http://localhost:3000`)

## Testing Tips

1. Always ensure you're logged in before testing protected endpoints
2. Monitor the Response section for:
   - Status code (200 OK, 401 Unauthorized, etc.)
   - Response body
   - Response time
3. Check the Headers tab for:
   - Authorization tokens
   - Content-Type
4. Use the "Tests" tab to write automated tests if needed

## Common Issues

1. 401 Unauthorized
   - Make sure you're logged in
   - Check if session/tokens are valid

2. 404 Not Found
   - Verify endpoint URL is correct
   - Check if file ID exists for download operations

3. 500 Server Error
   - Check server logs for detailed error information

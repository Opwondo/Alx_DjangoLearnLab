
# Social Media API

A Django REST Framework-based social media API with user authentication.

## Setup Instructions

1. Clone the repository
2. Install dependencies:
3. Run migrations:
4. Create a superuser:
5. Run the server:


## API Endpoints

### Registration
- **URL:** `/api/register/`
- **Method:** POST
- **Body:** 
```json
{
 "username": "your_username",
 "email": "your_email@example.com",
 "password": "your_password",
 "password2": "your_password",
 "bio": "Your bio (optional)",
 "profile_picture": "file upload (optional)"
}

Login
URL: /api/login/

Method: POST

Body:

{
  "username": "your_username",
  "password": "your_password"
}


Response: Returns user data and authentication token

Profile
URL: /api/profile/

Method: GET (view), PUT/PATCH (update)

Headers: Authorization: Token your_token_here

Response: Returns user profile information

User Model Fields
username (required)

email (required)

password (required)

bio (optional, max 500 characters)

profile_picture (optional, image upload)

followers (auto-managed, tracks followers)

following (auto-managed, tracks who user follows)


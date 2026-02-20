
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


## Posts and Comments API Endpoints

### Posts

#### List all posts
- **URL:** `/api/posts/`
- **Method:** GET
- **Query Parameters:** 
  - `search`: Search by title or content
  - `author`: Filter by author ID
  - `page`: Page number for pagination (10 items per page)
- **Response:** Paginated list of posts with comments
- **Example Request:**
  ```bash
  curl "http://127.0.0.1:8000/api/posts/?search=python&page=1"
Create a new post
URL: /api/posts/

Method: POST

Headers: Authorization: Token your_token_here

Content-Type: application/json

Body:

json
{
  "title": "My First Post",
  "content": "This is the content of my post"
}
Example Request:

bash
curl -X POST http://127.0.0.1:8000/api/posts/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Hello World", "content": "This is my first post"}'
Get a specific post
URL: /api/posts/{id}/

Method: GET

Response: Single post with all its comments

Example Request:

bash
curl http://127.0.0.1:8000/api/posts/1/
Update a post
URL: /api/posts/{id}/

Method: PUT (full update) or PATCH (partial update)

Headers: Authorization: Token your_token_here

Body: Fields to update

Note: Only the author can update the post

Example Request:

bash
curl -X PUT http://127.0.0.1:8000/api/posts/1/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Updated Title", "content": "Updated content"}'
Delete a post
URL: /api/posts/{id}/

Method: DELETE

Headers: Authorization: Token your_token_here

Note: Only the author can delete the post

Example Request:

bash
curl -X DELETE http://127.0.0.1:8000/api/posts/1/ \\
  -H "Authorization: Token YOUR_TOKEN"
Comments
List all comments
URL: /api/comments/

Method: GET

Query Parameters: post={post_id} to filter by post

Example Request:

bash
curl "http://127.0.0.1:8000/api/comments/?post=1"
Create a comment on a post
URL: /api/comments/

Method: POST

Headers: Authorization: Token your_token_here

Body:

json
{
  "post": 1,
  "content": "Great post!"
}
Example Request:

bash
curl -X POST http://127.0.0.1:8000/api/comments/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"post": 1, "content": "This is a great post!"}'
Get a specific comment
URL: /api/comments/{id}/

Method: GET

Example Request:

bash
curl http://127.0.0.1:8000/api/comments/1/
Update a comment
URL: /api/comments/{id}/

Method: PUT or PATCH

Headers: Authorization: Token your_token_here

Note: Only the author can update the comment

Example Request:

bash
curl -X PATCH http://127.0.0.1:8000/api/comments/1/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "Updated comment text"}'
Delete a comment
URL: /api/comments/{id}/

Method: DELETE

Headers: Authorization: Token your_token_here

Note: Only the author can delete the comment

Example Request:

bash
curl -X DELETE http://127.0.0.1:8000/api/comments/1/ \\
  -H "Authorization: Token YOUR_TOKEN"
Post-Specific Comment Actions
Get all comments for a specific post
URL: /api/posts/{post_id}/comments/

Method: GET

Example Request:

bash
curl http://127.0.0.1:8000/api/posts/1/comments/
Create a comment on a specific post
URL: /api/posts/{post_id}/comments/

Method: POST

Headers: Authorization: Token your_token_here

Body:

json
{
  "content": "Great post!"
}
Example Request:

bash
curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "Commenting via post endpoint"}'
Testing Examples with Complete Workflows
Complete Workflow 1: Create a post and add comments
bash
# 1. Login to get token
curl -X POST http://127.0.0.1:8000/api/login/ \\
  -H "Content-Type: application/json" \\
  -d '{"username": "testuser", "password": "testpass123"}'

# 2. Create a post (use the token from response)
curl -X POST http://127.0.0.1:8000/api/posts/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"title": "My Python Journey", "content": "Learning Django REST Framework"}'

# 3. Add a comment to the post
curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \\
  -H "Authorization: Token YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"content": "Keep it up!"}'

# 4. View post with all comments
curl http://127.0.0.1:8000/api/posts/1/
Complete Workflow 2: Search and filter
bash
# Search posts containing "python"
curl "http://127.0.0.1:8000/api/posts/?search=python"

# Filter posts by author
curl "http://127.0.0.1:8000/api/posts/?author=1"

# Combine search and pagination
curl "http://127.0.0.1:8000/api/posts/?search=django&page=2"
Pagination Information
Default page size: 10 items per page

To navigate pages: Use page query parameter

Pagination metadata included in response:

json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [...]
}
Error Responses
403 Forbidden: When trying to modify someone else's content

401 Unauthorized: When authentication token is missing or invalid

400 Bad Request: When validation fails (e.g., empty content)

404 Not Found: When post or comment doesn't exist

Permission Rules
Anyone can view posts and comments (read-only)

Only authenticated users can create posts and comments

Only authors can update or delete their own posts and comments

Authentication required for all write operations


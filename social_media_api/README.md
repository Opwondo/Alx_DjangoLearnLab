
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


## User Follows and Feed Functionality

### User Management Endpoints

#### Get User Details
- **URL:** `/api/users/{id}/`
- **Method:** GET
- **Headers:** `Authorization: Token your_token_here`
- **Response:** Detailed user information including follower/following counts
- **Example:**
  ```bash
  curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/users/1/
Follow a User
URL: /api/follow/{user_id}/

Method: POST

Headers: Authorization: Token your_token_here

Response: Success message with updated counts

Example:

bash
curl -X POST http://127.0.0.1:8000/api/follow/2/ \
  -H "Authorization: Token YOUR_TOKEN"
Unfollow a User
URL: /api/unfollow/{user_id}/

Method: POST

Headers: Authorization: Token your_token_here

Response: Success message with updated counts

Example:

bash
curl -X POST http://127.0.0.1:8000/api/unfollow/2/ \
  -H "Authorization: Token YOUR_TOKEN"
List Followers
URL: /api/followers/

Method: GET

Headers: Authorization: Token your_token_here

Response: List of users following you

Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/followers/
List Following
URL: /api/following/

Method: GET

Headers: Authorization: Token your_token_here

Response: List of users you follow

Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/following/
Feed Functionality
Get Your Feed
URL: /api/feed/

Method: GET

Headers: Authorization: Token your_token_here

Query Parameters:

page: Page number for pagination (10 items per page)

Response: Paginated list of posts from users you follow, ordered by most recent first

Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" "http://127.0.0.1:8000/api/feed/?page=1"
Complete Workflow Example
bash
# 1. Login as user1
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "password123"}'

# Save the token from response: TOKEN1

# 2. Login as user2
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user2", "password": "password123"}'

# Save the token from response: TOKEN2

# 3. User1 follows user2
curl -X POST http://127.0.0.1:8000/api/follow/2/ \
  -H "Authorization: Token TOKEN1"

# 4. User2 creates a post
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token TOKEN2" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Post", "content": "This will appear in feeds"}'

# 5. User1 views their feed (should see user2's post)
curl -H "Authorization: Token TOKEN1" http://127.0.0.1:8000/api/feed/
Model Updates
CustomUser Model Additions
Added following field: Many-to-Many relationship to self

symmetrical=False: Following is one-way relationship

related_name='followers': Access followers through this relation

New Properties
followers_count: Number of users following this user

following_count: Number of users this user follows

posts_count: Number of posts by this user

Permission Rules for Follow System
Users must be authenticated to:

View other users' details

Follow/unfollow users

View their followers/following lists

Access their feed

Users cannot follow/unfollow themselves

Users can only modify their own following list

Error Responses for Follow System
400 Bad Request:

Trying to follow/unfollow yourself

Trying to follow someone you already follow

Trying to unfollow someone you don't follow

401 Unauthorized: Missing or invalid token

404 Not Found: User doesn't exist


## Likes and Notifications Functionality

### Like System Endpoints

#### Like a Post
- **URL:** `/api/posts/{post_id}/like/`
- **Method:** POST
- **Headers:** `Authorization: Token your_token_here`
- **Response:**
  ```json
  {
    "message": "You liked post \"Post Title\"",
    "likes_count": 5
  }
Example:

bash
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
  -H "Authorization: Token YOUR_TOKEN"
Unlike a Post
URL: /api/posts/{post_id}/unlike/

Method: POST

Headers: Authorization: Token your_token_here

Response:

json
{
  "message": "You unliked post \"Post Title\"",
  "likes_count": 4
}
Example:

bash
curl -X POST http://127.0.0.1:8000/api/posts/1/unlike/ \
  -H "Authorization: Token YOUR_TOKEN"
Get Users Who Liked a Post
URL: /api/posts/{post_id}/likes/

Method: GET

Headers: Authorization: Token your_token_here

Response: List of users who liked the post

Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/posts/1/likes/
Notification System Endpoints
Get Notifications
URL: /api/notifications/

Method: GET

Headers: Authorization: Token your_token_here

Query Parameters:

show_read=true - Include read notifications (default: false)

type=like - Filter by notification type (like, comment, follow)

Response: Paginated list of notifications

Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" "http://127.0.0.1:8000/api/notifications/?show_read=false&type=like"
Get Unread Notification Count
URL: /api/notifications/unread-count/

Method: GET

Headers: Authorization: Token your_token_here

Response:

json
{
  "unread_count": 3
}
Example:

bash
curl -H "Authorization: Token YOUR_TOKEN" http://127.0.0.1:8000/api/notifications/unread-count/
Mark Notifications as Read
URL: /api/notifications/mark-read/

Method: POST

Headers: Authorization: Token your_token_here

Body Options:

json
// Mark specific notifications
{
  "notification_ids": [1, 2, 3]
}

// Mark all notifications as read
{
  "mark_all": true
}
Example:

bash
curl -X POST http://127.0.0.1:8000/api/notifications/mark-read/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mark_all": true}'
Post Serializer Updates
The Post serializer now includes:

likes_count: Total number of likes

is_liked_by_user: Boolean indicating if current user liked the post

likes: Detailed list of likes (included in response)

Complete Workflow Examples
Workflow 1: Like and Notification Flow
bash
# 1. User1 creates a post
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token USER1_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "My Awesome Post", "content": "This is content"}'

# 2. User2 likes the post
curl -X POST http://127.0.0.1:8000/api/posts/1/like/ \
  -H "Authorization: Token USER2_TOKEN"

# 3. User1 checks notifications (should see a like notification)
curl -H "Authorization: Token USER1_TOKEN" http://127.0.0.1:8000/api/notifications/

# 4. User1 marks notifications as read
curl -X POST http://127.0.0.1:8000/api/notifications/mark-read/ \
  -H "Authorization: Token USER1_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mark_all": true}'
Workflow 2: Comment and Notification Flow
bash
# 1. User2 comments on User1's post
curl -X POST http://127.0.0.1:8000/api/posts/1/comments/ \
  -H "Authorization: Token USER2_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Great post!"}'

# 2. User1 gets notification
curl -H "Authorization: Token USER1_TOKEN" http://127.0.0.1:8000/api/notifications/

# 3. User1 checks unread count
curl -H "Authorization: Token USER1_TOKEN" http://127.0.0.1:8000/api/notifications/unread-count/
Notification Types
follow: When someone follows you

like: When someone likes your post

comment: When someone comments on your post

Error Responses
400 Bad Request:

Liking a post twice

Unliking a post you haven't liked

Invalid notification IDs

401 Unauthorized: Missing or invalid token

404 Not Found: Post or notification doesn't exist

Database Schema Updates
New Models
Like Model
python
- user (ForeignKey to User)
- post (ForeignKey to Post)
- created_at (DateTime)
- unique_together: ['user', 'post']
Notification Model
python
- recipient (ForeignKey to User)
- actor (ForeignKey to User)
- verb (CharField: follow/like/comment)
- target (GenericForeignKey to any object)
- created_at (DateTime)
- is_read (Boolean)

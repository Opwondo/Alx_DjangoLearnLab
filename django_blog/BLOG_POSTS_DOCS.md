# Django Blog - Blog Post Management Documentation

## Overview
The blog post management system provides full CRUD (Create, Read, Update, Delete) functionality for blog posts. It uses Django's class-based views for efficient implementation and includes proper permission controls.

## Features

### 1. List Posts (Read)
- **URL**: `/posts/`
- **View**: `PostListView` (ListView)
- **Template**: `post_list.html`
- **Access**: Public (no authentication required)
- **Features**:
  - Displays all posts with pagination (5 posts per page)
  - Shows post title, author, date, and content excerpt
  - "Create New Post" button for authenticated users
  - Links to individual post details

### 2. View Single Post (Read)
- **URL**: `/posts/<int:pk>/`
- **View**: `PostDetailView` (DetailView)
- **Template**: `post_detail.html`
- **Access**: Public (no authentication required)
- **Features**:
  - Displays complete post with title, content, and metadata
  - Shows edit/delete buttons for post author
  - "Back to All Posts" navigation

### 3. Create Post
- **URL**: `/posts/new/`
- **View**: `PostCreateView` (CreateView)
- **Template**: `post_form.html`
- **Access**: Authenticated users only (LoginRequiredMixin)
- **Features**:
  - Form with title and content fields
  - Automatically sets author to logged-in user
  - Success message on creation
  - Redirects to post detail view

### 4. Update Post
- **URL**: `/posts/<int:pk>/edit/`
- **View**: `PostUpdateView` (UpdateView)
- **Template**: `post_form.html`
- **Access**: Post author only (UserPassesTestMixin)
- **Features**:
  - Pre-filled form with existing post data
  - Author verification before allowing edit
  - Success message on update

### 5. Delete Post
- **URL**: `/posts/<int:pk>/delete/`
- **View**: `PostDeleteView` (DeleteView)
- **Template**: `post_confirm_delete.html`
- **Access**: Post author only (UserPassesTestMixin)
- **Features**:
  - Confirmation page before deletion
  - Shows post preview for verification
  - Warning message about permanent deletion
  - Success message after deletion

## Permission System

### Permission Classes Used:
1. **LoginRequiredMixin**: Ensures user is authenticated
   - Applied to: CreateView, UpdateView, DeleteView

2. **UserPassesTestMixin**: Custom permission check
   - Applied to: UpdateView, DeleteView
   - Test: `self.request.user == post.author`

## Form Handling

### PostForm (ModelForm)
- Fields: title, content
- Custom widgets with Bootstrap-like classes
- Client-side and server-side validation
- CSRF protection enabled

## URL Patterns

| URL Pattern | View | Name | Permission |
|------------|------|------|------------|
| `/posts/` | PostListView | `post-list` | Public |
| `/posts/<int:pk>/` | PostDetailView | `post-detail` | Public |
| `/posts/new/` | PostCreateView | `post-create` | Authenticated |
| `/posts/<int:pk>/edit/` | PostUpdateView | `post-update` | Author only |
| `/posts/<int:pk>/delete/` | PostDeleteView | `post-delete` | Author only |

## Testing Instructions

### Test Post Creation
1. Login to your account
2. Navigate to `/posts/new/` or click "New Post" in navigation
3. Fill in title and content
4. Submit form
5. Verify redirect to post detail page
6. Check success message appears

### Test Post Update
1. Create a post or use existing one
2. Navigate to post detail page
3. Click "Edit Post" button
4. Modify content
5. Submit form
6. Verify changes saved and success message appears

### Test Post Deletion
1. Navigate to a post you authored
2. Click "Delete Post" button
3. Review confirmation page
4. Click "Yes, Delete Post"
5. Verify redirect to posts list
6. Confirm post no longer appears
7. Check success message

### Test Permissions
1. Logout and try to access `/posts/new/` - Should redirect to login
2. Try to edit another user's post - Should get 403 error
3. Try to delete another user's post - Should get 403 error

## Security Features

1. **CSRF Protection**: All forms include CSRF tokens
2. **Permission Checks**: Authorship verification for edit/delete
3. **Login Required**: Creation requires authentication
4. **Safe Redirects**: Using Django's redirect handling
5. **Form Validation**: Both client and server-side validation

## File Structure
## Database Schema Updates
- Added `updated_date` field to Post model
- Automatic timestamp on post updates
- Author relationship remains ForeignKey to User

## Future Enhancements
- Add post categories/tags
- Implement post search functionality
- Add post comments system
- Include post sharing options
- Add post drafts/publishing workflow

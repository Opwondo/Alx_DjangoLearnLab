# Django Blog - Comment System Documentation

## Overview
The comment system allows users to interact with blog posts by leaving comments. Authenticated users can create, edit, and delete their own comments, while all users can view comments on posts.

## Features

### 1. View Comments
- Comments are displayed on each blog post's detail page
- Comments show author, date posted, and content
- Edited comments show "(edited)" indicator
- All users (authenticated or not) can view comments

### 2. Add Comments
- **URL**: `/post/<post_id>/comments/add/`
- **Access**: Authenticated users only
- **Location**: Post detail page
- **Process**:
  1. User types comment in textarea
  2. Form submits via POST
  3. Comment saved with author and post
  4. Success message displayed
  5. Page reloads showing new comment

### 3. Edit Comments
- **URL**: `/comment/<comment_id>/edit/`
- **Access**: Comment author only
- **Template**: `comment_form.html`
- **Process**:
  1. User clicks "Edit" on their comment
  2. Pre-filled form with existing comment
  3. User modifies and submits
  4. `updated_at` timestamp updates
  5. Success message and redirect to post

### 4. Delete Comments
- **URL**: `/comment/<comment_id>/delete/`
- **Access**: Comment author only
- **Template**: `comment_confirm_delete.html`
- **Process**:
  1. User clicks "Delete" on their comment
  2. Confirmation page shows comment preview
  3. User confirms deletion
  4. Comment removed from database
  5. Success message and redirect to post

## Database Schema

### Comment Model
| Field | Type | Description |
|-------|------|-------------|
| post | ForeignKey(Post) | The post this comment belongs to |
| author | ForeignKey(User) | The user who wrote the comment |
| content | TextField | The comment text |
| created_at | DateTimeField | Auto-set when comment created |
| updated_at | DateTimeField | Auto-updated when comment edited |

### Relationships
- One Post can have many Comments (One-to-Many)
- One User can have many Comments (One-to-Many)

## URL Patterns

| URL Pattern | View | Name | Permission |
|------------|------|------|------------|
| `/post/<int:post_id>/comments/add/` | add_comment | `add-comment` | Authenticated |
| `/comment/<int:comment_id>/edit/` | edit_comment | `edit-comment` | Comment author |
| `/comment/<int:comment_id>/delete/` | delete_comment | `delete-comment` | Comment author |

## Template Structure


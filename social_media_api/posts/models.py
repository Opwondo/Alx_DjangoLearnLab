# posts/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    """
    Post model for social media posts
    Each post belongs to a user (author)
    """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text="The user who created this post"
    )
    title = models.CharField(
        max_length=255,
        help_text="Title of the post"
    )
    content = models.TextField(
        help_text="Main content of the post"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when post was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when post was last updated"
    )

    class Meta:
        ordering = ['-created_at']  # Show newest posts first

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    """
    Comment model for comments on posts
    Each comment belongs to a user (author) and a post
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The post this comment belongs to"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who created this comment"
    )
    content = models.TextField(
        help_text="The comment text"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when comment was last updated"
    )

    class Meta:
        ordering = ['created_at']  # Show oldest comments first

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
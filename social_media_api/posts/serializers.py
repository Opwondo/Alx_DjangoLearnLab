# posts/serializers.py
from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    Handles reading and writing comments
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    post_title = serializers.ReadOnlyField(source='post.title')

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'post_title', 'author', 'author_username',
            'content', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate(self, data):
        """
        Additional validation for comments
        """
        if not data.get('content', '').strip():
            raise serializers.ValidationError("Comment content cannot be empty")
        return data

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model
    Includes nested comments and author details
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_username', 'title', 'content',
            'comments', 'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def validate_title(self, value):
        """
        Validate that title is not empty
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value

    def validate_content(self, value):
        """
        Validate that content is not empty
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value
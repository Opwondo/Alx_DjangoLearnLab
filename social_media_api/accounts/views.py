# accounts/views.py

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        if request.user == user_to_follow:
            return Response(
                {"error": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)

        return Response(
            {"message": f"You are now following {user_to_follow.username}"},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), id=user_id)

        if request.user == user_to_unfollow:
            return Response(
                {"error": "You cannot unfollow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.remove(user_to_unfollow)

        return Response(
            {"message": f"You have unfollowed {user_to_unfollow.username}"},
            status=status.HTTP_200_OK
        )
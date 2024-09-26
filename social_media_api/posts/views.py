from django.shortcuts import render
from .models import Notification

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from rest_framework import filters
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise permissions.PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all() 
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Get the post or return 404
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # Create a notification for the post owner
        Notification.objects.create(
            recipient=post.user,
            actor=request.user,
            verb='liked your post',
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id
        )
        return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # Get the post or return 404
    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response({'status': 'not liked yet'}, status=status.HTTP_400_BAD_REQUEST)
    
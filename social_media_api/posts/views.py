from django.shortcuts import render
from .models import Notification

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from rest_framework import filters
from rest_framework import generics

from rest_framework import status


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

    def like_post(self,request,pk):
        post = Post.objects.get(id=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            self.create_notification(request.user, post)
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
        return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def unlike_post(self, request, pk):
        post = Post.objects.get(id=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({"message": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)

    def create_notification(self, user, post):
        notification = Notification(
            recipient=post.author, 
            actor=user, 
            verb="liked your post", 
            #target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=post.id
        )
        notification.save()
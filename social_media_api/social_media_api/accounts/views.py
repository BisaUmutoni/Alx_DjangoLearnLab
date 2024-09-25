from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework import generics
from .models import CustomUser
from .serializers import UserLoginSerializer
from rest_framework.authtoken.models import Token

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Token.objects.create(user=user)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=400)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow_user(self, request, pk=None):
        user_to_follow =  self.get.object()
        request.user.following.add(user_to_follow)
        return Response({"detail": "Now following."})
    
    @action(detail=True, methods=['post'])
    def unfollow_user(self, request, pk=None):
        user_to_unfollow = self.get_object()
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "Unfollowed."})

class FollowViewSet('', generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = CustomUser.objects.get(pk=pk)
        request.user.following.add(user_to_follow)
        return Response({"detail": "Now following."})

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_unfollow = CustomUser.objects.get(pk=pk)
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "Unfollowed."})

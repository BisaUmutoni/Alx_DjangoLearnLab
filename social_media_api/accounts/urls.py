from django.urls import path
from .views import RegisterView, LoginView
from .views import  FollowViewSet

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', FollowViewSet.as_view({'post': 'follow_user'}), name='follow_user'),
    path('unfollow/<int:user_id>/', FollowViewSet.as_view({'post': 'unfollow_user'}), name='unfollow_user'),

]

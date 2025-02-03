from django.urls import path
from .views import FollowerUserView, FollowingListView, FollowerListView

urlpatterns = [
    path('follow/<int:user_id>/', FollowerUserView.as_view(), name='follow-user'),
    path('following/', FollowingListView.as_view(), name='following-list'),
    path('followers/', FollowerListView.as_view(), name='followers-list'),
]

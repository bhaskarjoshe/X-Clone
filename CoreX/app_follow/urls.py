from django.urls import path

from .views import (
    FollowerListView,
    FollowerUserView,
    FollowingListView,
    NonFollowingUsersView,
)

app_name = "app_follow"

urlpatterns = [
    path("api/follow/<int:user_id>/", FollowerUserView.as_view(), name="follow-user"),
    path("api/following/", FollowingListView.as_view(), name="following-list"),
    path("api/followers/", FollowerListView.as_view(), name="followers-list"),
    path("non_following/", NonFollowingUsersView.as_view(), name="non-following-users"),
]

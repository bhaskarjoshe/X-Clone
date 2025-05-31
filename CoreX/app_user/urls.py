from django.urls import path

from .views import (
    AllUserListView,
    OtherUserProfileView,
    UpdateUserProfileView,
    UserProfileView,
)

app_name = "app_user"

urlpatterns = [
    path("api/profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "profile/update/", UpdateUserProfileView.as_view(), name="update-user-profile"
    ),
    path(
        "profile/<int:pk>/", OtherUserProfileView.as_view(), name="other-user-profile"
    ),
    path("api/all_users/", AllUserListView.as_view(), name="all-users-list"),
]

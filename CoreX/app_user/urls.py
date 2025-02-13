from django.urls import path
from .views import (
    UserProfileView,
    UpdateUserProfileView,
    OtherUserProfileView,
    AllUserListView,
    FetchUsersWithTweetsView
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
    path("api/fetch-users-tweets-async/", FetchUsersWithTweetsView.as_view(), name="fetch-users-tweets-async-api"),
]

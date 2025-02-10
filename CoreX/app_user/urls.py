from django.urls import path
from .views import UserProfileView, UpdateUserProfileView, OtherUserProfileView

app_name = 'app_user'

urlpatterns = [
    path("api/profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "profile/update/", UpdateUserProfileView.as_view(), name="update-user-profile"
    ),
    path(
        "profile/<int:pk>/", OtherUserProfileView.as_view(), name="other-user-profile"
    ),
]

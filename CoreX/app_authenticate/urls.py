from django.urls import path
from .views import RegisterView, LoginView, LogoutView, SearchUsersView


app_name = "app_authenticate"

urlpatterns = [
    path("api/register/", RegisterView.as_view(), name="register-api"),
    path("api/login/", LoginView.as_view(), name="login-api"),
    path("api/logout/", LogoutView.as_view(), name="logout-api"),
    path("api/search/", SearchUsersView.as_view(), name="search-users"),
]

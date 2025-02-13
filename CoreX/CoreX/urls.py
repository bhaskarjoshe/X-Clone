from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_tweets.views_frontend import landing_page, homepage
from app_user.views_frontend import profile_page

urlpatterns = [
    path("admin/", admin.site.urls),
    # normal routes
    path("", landing_page, name="landing_page"),
    path("homepage/", homepage, name="homepage"),
    path("profile/", profile_page, name="profile"),
    path("authenticate/", include("app_authenticate.urls")),
    path("tweets/", include("app_tweets.urls")),
    path("follows/", include("app_follow.urls")),
    path("user/", include("app_user.urls")),
    path("comments/", include("app_comments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

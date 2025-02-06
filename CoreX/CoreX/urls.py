from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app_tweets.views_frontend import landing_page, homepage

urlpatterns = [
    path("admin/", admin.site.urls),
    #api routes
    path("api/user/", include("app_user.urls")),
    path("api/comments/", include("app_comments.urls")),
    path("api/follows/", include("app_follow.urls")),
    # normal routes
    path('', landing_page, name='landing_page'),
    path('homepage/', homepage, name='homepage'),
    path("authenticate/", include("app_authenticate.urls")),
    path("tweets/", include("app_tweets.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

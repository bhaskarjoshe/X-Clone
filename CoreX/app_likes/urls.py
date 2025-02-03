from django.urls import path
from .views import (
    LikeTweetView,
    UnlikeTweetView,
    GetLikesView
)

urlpatterns = [
    path('tweet/<int:pk>/like/', LikeTweetView.as_view(), name='like-tweet'),
    path('tweet/<int:pk>/unlike/', UnlikeTweetView.as_view(), name='unlike-tweet'),
    path('tweet/<int:pk>/all-likes/', GetLikesView.as_view(), name='all-likes'),
]

from django.urls import path
from .views import (
    TweetListView,
    TweetDetailView,
    PinTweetView,
    LikeTweetView,
    UnlikeTweetView,
    GetLikesView,
    CommentTweetView,
)

urlpatterns = [
    path("tweet/", TweetListView.as_view(), name="tweet-list"),
    path("tweet/<int:pk>/", TweetDetailView.as_view(), name="tweet-detail"),
    path("tweet/<int:pk>/pin/", PinTweetView.as_view(), name="tweet-pin"),
    path("tweet/<int:pk>/like/", LikeTweetView.as_view(), name="tweet-like"),
    path("tweet/<int:pk>/unlike/", UnlikeTweetView.as_view(), name="tweet-unlike"),
    path("tweet/<int:pk>/likes/", GetLikesView.as_view(), name="tweet-likes"),
    path("tweet/<int:pk>/comment/", CommentTweetView.as_view(), name="tweet-comment"),
]

from django.urls import path

from .views import (
    CommentTweetView,
    FollowingTweetsView,
    GetLikesView,
    GetMediaByTweetView,
    LikeTweetView,
    PinTweetView,
    TweetDetailView,
    TweetListView,
    UnlikeTweetView,
    UploadMediaView,
    UserTweetsByIdView,
    allTweetView,
)

app_name = "app_tweets"

urlpatterns = [
    path(
        "api/tweet/user/<int:user_id>/",
        UserTweetsByIdView.as_view(),
        name="user-tweets-by-id-api",
    ),
    path("api/tweet/", TweetListView.as_view(), name="tweet-list-api"),
    path("api/tweet/all-tweets/", allTweetView.as_view(), name="all-tweets-api"),
    path(
        "api/tweet/following-tweets/",
        FollowingTweetsView.as_view(),
        name="following-tweets-api",
    ),
    path("api/tweet/<int:pk>/", TweetDetailView.as_view(), name="tweet-detail-api"),
    path("api/tweet/<int:pk>/pin/", PinTweetView.as_view(), name="tweet-pin-api"),
    path("api/tweet/<int:pk>/like/", LikeTweetView.as_view(), name="tweet-like-api"),
    path(
        "api/tweet/<int:pk>/unlike/", UnlikeTweetView.as_view(), name="tweet-unlike-api"
    ),
    path("api/tweet/<int:pk>/likes/", GetLikesView.as_view(), name="tweet-likes-api"),
    path(
        "api/tweet/<int:pk>/comment/",
        CommentTweetView.as_view(),
        name="tweet-comment-api",
    ),
    path(
        "api/tweet/<int:pk>/media/",
        GetMediaByTweetView.as_view(),
        name="get-media-by-tweet-api",
    ),
    path(
        "api/tweet/<int:pk>/media/upload/",
        UploadMediaView.as_view(),
        name="upload-media-api",
    ),
]

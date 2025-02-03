from .views import CommentListView, CreateCommentView, CommentDetailView, CommentRepliesView
from rest_framework.urls import path

urlpatterns = [
    path('comment/tweet/<int:tweet_id>/', CommentListView.as_view(), name='comment-list'),
    path('comment/tweet/<int:tweet_id>/create/', CreateCommentView.as_view(), name='create-comment'),
    path('comment/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:comment_id>/replies', CommentRepliesView.as_view(), name='comment-replies'),
]

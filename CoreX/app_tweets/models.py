from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tweet(models.Model):
    tweet_content = models.TextField(max_length=25000)
    author = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    media = models.ManyToManyField("Media", related_name="tweets", blank=True)  # Multiple media files


    def __str__(self):
        return self.tweet_content[:50]


class Like(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="liked_tweets", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("tweet", "user")

    def __str__(self):
        return f"Like by {self.user.username} on tweet {self.tweet.id}"


class Media(models.Model):
    file = models.FileField(upload_to="tweet_media/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media {self.id}"


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    comment_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author.username} on tweet {self.tweet.id}"

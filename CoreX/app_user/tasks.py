import os
import json
from celery import shared_task
from django.contrib.auth import get_user_model
from app_tweets.models import Tweet
from app_authenticate.serializers import UserProfileSerializer
from app_tweets.serializers import TweetSerializer

User = get_user_model()


@shared_task
def fetch_users_with_tweets_async():
    users = User.objects.all()
    users_with_tweets = []

    for user in users:
        tweets = Tweet.objects.filter(author=user)

        user_data = UserProfileSerializer(user).data
        tweet_data = TweetSerializer(tweets, many=True).data

        user_data["tweets"] = tweet_data
        users_with_tweets.append(user_data)

    json_data = json.dumps(users_with_tweets, indent=4)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    celery_output_dir = os.path.join(base_dir, "..", "celery_data")
    os.makedirs(celery_output_dir, exist_ok=True)
    file_path = os.path.join(celery_output_dir, f"tweets_allUsers.json")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json_data)

    return f"Data saved to {file_path}"

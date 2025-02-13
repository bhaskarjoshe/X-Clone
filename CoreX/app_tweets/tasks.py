import os
import json
from celery import shared_task
from .models import Tweet
from .serializers import TweetSerializer


@shared_task
def fetch_tweets_async(user_id):
    tweets = Tweet.objects.filter(author_id=user_id)
    serialized_tweets = TweetSerializer(tweets, many=True).data

    for tweet in serialized_tweets:
        if "author" in tweet:
            del tweet["author"]

    json_data = json.dumps(serialized_tweets, indent=4)

    username = tweets.first().author.username if tweets.exists() else "default_user"

    is_render = os.environ.get("RENDER", False)

    if is_render:
        return json_data
    
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        celery_output_dir = os.path.join(base_dir, "..", "celery_data")
        os.makedirs(celery_output_dir, exist_ok=True)
        file_path = os.path.join(celery_output_dir, f"tweets_{username}.json")

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json_data)

        return f"Tweets saved to {file_path}"

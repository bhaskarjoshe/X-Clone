# Generated by Django 5.1.5 on 2025-02-01 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_tweets", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="comment",
            old_name="content",
            new_name="comment_content",
        ),
        migrations.RenameField(
            model_name="tweet",
            old_name="content",
            new_name="tweet_content",
        ),
    ]

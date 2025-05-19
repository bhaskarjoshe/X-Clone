# X-Clone

A Twitter/X clone built with Django REST Framework, featuring real-time updates, media handling, and comprehensive social networking capabilities.

## Features

- User Authentication
- Tweet Creation and Management
- Media Upload Support (Images, GIFs, Videos)
- Comment System
- Follow/Unfollow Functionality
- Real-time Updates using Celery
- Search Functionality with Elasticsearch
- RESTful API Architecture

## Tech Stack

- Django 5.1.5
- Django REST Framework 3.15.2
- Celery 5.4.0
- PostgreSQL
- Redis
- Elasticsearch 7.10.1
- Python 3.x

## Project Structure

```
CoreX/                          # Main Django Project Directory
├── manage.py                   # Django Management Script
├── requirements.txt            # Project Dependencies
├── app_authenticate/           # Authentication App
├── app_comments/              # Comments Management App
├── app_follow/                # Follow System App
├── app_tweets/                # Tweet Management App
├── app_user/                  # User Management App
├── celery_data/              # Celery Task Data
├── CoreX/                    # Project Settings
├── media/                    # Media Files
│   └── tweet_media/         # Tweet Media Storage
├── static/                   # Static Files
└── templates/               # HTML Templates

Documentation/               # Project Documentation
```

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd X-Clone
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r CoreX/requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the CoreX directory with the following variables:
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   REDIS_URL=your_redis_url
   ELASTICSEARCH_DSL_HOST=your_elasticsearch_host
   ```

5. Set up the database:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Start Elasticsearch service (make sure it's installed)

8. Start Redis server (make sure it's installed)

9. Start Celery worker:
   ```bash
   celery -A CoreX worker -l info
   ```

10. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

The application provides several RESTful API endpoints:

- Authentication: `/api/auth/`
- Tweets: `/api/tweets/`
- Comments: `/api/comments/`
- User Profiles: `/api/users/`
- Follow System: `/api/follow/`


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


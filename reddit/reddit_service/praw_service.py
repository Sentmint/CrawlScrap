import praw
import os
from dotenv import load_dotenv


def praw_connection():
    load_dotenv()
    return praw.Reddit(
        client_id=os.environ.get('REDDIT_CLIENT_ID'),
        client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
        user_agent=os.environ.get('REDDIT_USER_AGENT')
    )

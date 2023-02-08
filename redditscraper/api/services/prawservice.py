import praw
from redditscraper.api.services import secrets


def prawConnection():
    return praw.Reddit(
        client_id=secrets.creds.get('CLIENT_ID'),
        client_secret=secrets.creds.get('CLIENT_SECRET'),
        user_agent=secrets.creds.get('USER_AGENT')
    )
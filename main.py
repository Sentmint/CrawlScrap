import praw
from praw.models import MoreComments
import secrets

reddit = praw.Reddit(
    client_id=secrets.creds.get('CLIENT_ID'),
    client_secret=secrets.creds.get('CLIENT_SECRET'),
    user_agent=secrets.creds.get('USER_AGENT')
)

hot_posts = reddit.subreddit('WallStreetBets').hot(limit=20)
# for x in hot_posts:
#     print(x.title)
#     print(x)

submissionTest = reddit.submission(id="10nnswb")

for x in submissionTest.comments:
    if isinstance(x, MoreComments or x.parent_id != "10nnswb"):
        continue
    print(x.author, ":", x.body, x.score)

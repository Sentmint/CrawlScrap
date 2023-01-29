import praw
from praw.models import MoreComments
import secrets
import datetime

reddit = praw.Reddit(
    client_id=secrets.creds.get('CLIENT_ID'),
    client_secret=secrets.creds.get('CLIENT_SECRET'),
    user_agent=secrets.creds.get('USER_AGENT')
)

## TODO: find a way to get to the bottom of every comment, or find a function that does it for us.
## TODO: think of a way to exclude duplicates in the final product. Ignore already stored comments, only rescan when size has changed.


# def threadScrape(thread):

# Each page is 25 entries on reddit. Only checking the front page of the subreddit.
note01 = reddit.subreddit("wallstreetbets").hot(limit=25)
note00 = reddit.submission("10nozyf")

# for x in note01:
#     if x.stickied:
#         continue
#     print(x.name, ", ", x.author, ": ", x.title, x.selftext)

testList = []

print(len(testList))

start = datetime.datetime.now()

for x in note01:
    if x.stickied:
        continue
    curr = reddit.submission(x.id)  # Grabs the front page ids to be scanned for comments
    curr.comments.replace_more(limit=None)
    for y in curr.comments.list():
        testList.append(y.body)

end = datetime.datetime.now()

totalRun = end - start

print(len(testList))
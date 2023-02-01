import Services.prawservice as praw
import datetime
from praw.models import MoreComments


reddit = praw.prawConnection()

# TODO: find a way to get to the bottom of every comment, or find a function that does it for us.
# ANSWER: comments.replace_more(limit=None) to scan entire comment tree; .list() to iterate tree.
# TODO: Add a prelim check to make sure that we do not keep duplicate comments.
# TODO: Do we want to scan the same thread multiple times and fetch new comments?
# TODO: Make an external list of subreddits to scrape; reference that here.


# def threadScrape(thread):

# Each page is 25 entries on reddit. Only checking the front page of the subreddit.
note01 = reddit.subreddit("personalfinancecanada").hot(limit=25)

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
print(totalRun)

import Services.prawservice as praw
import Resources.subreddits as subs
import datetime
from praw.models import MoreComments

reddit = praw.prawConnection()


# TODO: find a way to get to the bottom of every comment, or find a function that does it for us.
# ANSWER: comments.replace_more(limit=None) to scan entire comment tree; .list() to iterate tree.
# TODO: Add a prelim check to make sure that we do not keep duplicate comments.
# ANSWER: We created a list of all comments; hierarchy no longer exists.
# Can do a simple check on created_utc to see if we want to keep the comment
# TODO: Do we want to scan the same thread multiple times and fetch new comments?
# Sure. Done above.
# TODO: Make an external list of subreddits to scrape; reference that here.
# Done: resources folder
# TODO: Find an algorithm that will make it so that we fetch all comments in a reddit thread.
# TODO: Find an algorithm to ensure no duplicates with a faster runtime than our solution (checking for duplicates || only scanning if the comment is newer than our previously newest comment scanned).
# Potential Answer: First scan will be done on BEST. Second scan will be done on NEW. (not correct, may end up losing new comments due to janky logic)


# def threadScrape(thread):

# Each page is 25 entries on reddit. Only checking the front page of the subreddit.

start = datetime.datetime.now()

testList = []

testThread = reddit.submission("10rs0tf")
testThread.comments.replace_more(limit=None, threshold=0)
testThread.comment_sort = "new"
for comment in testThread.comments.list():
    testList.append(comment.body)
testComment = reddit.comment("j6zxty2")

# for subreddit in subs.subredditList():
#     redditTop25 = reddit.subreddit("All").hot(limit=25)
#     for thread in redditTop25:
#         if thread.stickied:
#             continue
#         curr = reddit.submission(thread.id)  # Grabs the front page ids to be scanned for comments
#         curr.comment_sort = "new"  # Sort comments by new to fetch only new comments
#         curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children, rather than just top level
#         for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
#             # if comment.created_utc < 1675368630.0:
#             #     continue
#             testList.append(comment.body)


end = datetime.datetime.now()

totalRun = end - start

print(len(testList))
print(totalRun)

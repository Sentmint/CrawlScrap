<<<<<<< HEAD
<<<<<<< HEAD
from api.services import prawservice as praw
from api.resources import subreddits as subs
from pathlib import Path
import logging
<<<<<<< HEAD
import json
import time
import os
=======
import Services.prawservice as praw
import Resources.subreddits as subs
=======
from api.services import prawservice as praw
from api.resources import subreddits as subs
<<<<<<< HEAD
from api.dtos import redditdto as dto
from pathlib import Path
>>>>>>> 0af83de (restructure; scraper now outputting JSON properly. Need to fix file dumping)
import datetime
import json
import time
import os

reddit = praw.prawConnection()
<<<<<<< HEAD
>>>>>>> 4a098b5 (restructured a bit, abstracted out praw credentials)
=======
started = str(time.time())
Path("/Reddit-Scraper/api/output/" + started).mkdir(parents=True, exist_ok=True)
>>>>>>> 0af83de (restructure; scraper now outputting JSON properly. Need to fix file dumping)
=======
import json
import time
import os
from pathlib import Path
>>>>>>> c2a3682 (refactored code & returning larger json rather than 1 json per thread)

=======
import json
import time
import os
>>>>>>> c982382 (release)

# TODO: find a way to get to the bottom of every comment, or find a function that does it for us.
# ANSWER: comments.replace_more(limit=None) to scan entire comment tree; .list() to iterate tree.
# TODO: Add a prelim check to make sure that we do not keep duplicate comments.
<<<<<<< HEAD
<<<<<<< HEAD
# ANSWER: We created a list of all comments; hierarchy no longer exists.
# Can do a simple check on created_utc to see if we want to keep the comment
# TODO: Do we want to scan the same thread multiple times and fetch new comments?
# Sure. Done above.
# TODO: Make an external list of subreddits to scrape; reference that here.
# Done: resources folder
# TODO: Find an algorithm that will make it so that we fetch all comments in a reddit thread.
# TODO: Find an algorithm to ensure no duplicates with a faster runtime than our solution (checking for duplicates || only scanning if the comment is newer than our previously newest comment scanned).
# Potential Answer: First scan will be done on BEST. Second scan will be done on NEW. (not correct, may end up losing new comments due to janky logic)


logging.basicConfig(level=logging.DEBUG)


def top25scanner():
    reddit = praw.prawConnection()
    for subreddit in subs.subredditList():
        top25 = reddit.subreddit(subreddit).hot(limit=25)
        top25Submissions = []
        for submission in top25:
            if submission.stickied:
                continue
            comments = []
            curr = reddit.submission(submission)  # Grabs the front page ids to be scanned for comments

            # TODO: Move this to ETL if quick way to filter out old comments is needed
            # curr.comment_sort = "new"  # Sort comments by new to fetch only new comments
            # if comment.created_utc < valueToScan:
            #     continue

            curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children
            for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
                comments.append({
                    "commentAuthor": comment.author_fullname if hasattr(comment, 'author_fullname') else "null",
                    # Note: Shadowbanned redditors do not have any of these fields available.
                    # "commentAuthor": [{
                    #     "id": comment.author.id,
                    #     "name": comment.author.name,
                    #     "commentKarma": comment.author.comment_karma,
                    #     "submissionKarma": comment.author.link_karma,
                    #     "accountCreated": comment.author.created_utc
                    #   } if comment.author is not None and not hasattr(comment.author, 'is_suspended') else "null"],
                    "body": comment.body,
                    "created_utc": comment.created_utc,
                    "edited": comment.edited,
                    "id": comment.id,
                    "is_root": comment.is_root,
                    "is_submitter": comment.is_submitter,
                    "permalink": comment.permalink,
                    "score": comment.score,
                    "ups": comment.ups
                })
            top25Submissions.append({
                "id": submission.id,
                "title": submission.title,
                "flair": submission.link_flair_text,
                "subreddit": submission.subreddit_name_prefixed,
                "created_utc": submission.created_utc,
                "upvote": submission.ups,
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "selfText": submission.selftext,
                "selfUrl": submission.url,
                "permalink": submission.permalink,
                "shortlink": submission.shortlink,
                "author": submission.author_fullname if hasattr(submission, 'author_fullname') else "null",
                # "author": [{
                #     "id": submission.author.id,
                #     "name": submission.author.name,
                #     "commentKarma": submission.author.comment_karma,
                #     "submissionKarma": submission.author.link_karma,
                #     "accountCreated": submission.author.created_utc,
                #     } if submission.author is not None and not hasattr(submission.author, 'is_suspended') else "null"],
                "commentCount": submission.num_comments,
                "comments": comments
            })
        create_submission_json(top25Submissions, subreddit)


def create_submission_json(submissions: list, subreddit):
    path = "output/" + subreddit
    file = str(time.time()) + ".json"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(path, file), "w") as f:
        json.dump(submissions, f)


top25scanner()
=======
=======
# ANSWER: We created a list of all comments; hierarchy no longer exists.
# Can do a simple check on created_utc to see if we want to keep the comment
>>>>>>> 1c4fc0b (updated todos + algo progress)
# TODO: Do we want to scan the same thread multiple times and fetch new comments?
# Sure. Done above.
# TODO: Make an external list of subreddits to scrape; reference that here.
# Done: resources folder
# TODO: Find an algorithm that will make it so that we fetch all comments in a reddit thread.
# TODO: Find an algorithm to ensure no duplicates with a faster runtime than our solution (checking for duplicates || only scanning if the comment is newer than our previously newest comment scanned).
# Potential Answer: First scan will be done on BEST. Second scan will be done on NEW. (not correct, may end up losing new comments due to janky logic)


logging.basicConfig(level=logging.DEBUG)


def top25scanner():
    reddit = praw.prawConnection()
    for subreddit in subs.subredditList():
        top25 = reddit.subreddit(subreddit).hot(limit=25)
        top25Submissions = []
        for submission in top25:
            if submission.stickied:
                continue
            comments = []
            curr = reddit.submission(submission)  # Grabs the front page ids to be scanned for comments

            # TODO: Move this to ETL if quick way to filter out old comments is needed
            # curr.comment_sort = "new"  # Sort comments by new to fetch only new comments
            # if comment.created_utc < valueToScan:
            #     continue

            curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children
            for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
                comments.append({
                    "commentAuthor": comment.author_fullname if hasattr(comment, 'author_fullname') else "null",
                    # Note: Shadowbanned redditors do not have any of these fields available.
                    # "commentAuthor": [{
                    #     "id": comment.author.id,
                    #     "name": comment.author.name,
                    #     "commentKarma": comment.author.comment_karma,
                    #     "submissionKarma": comment.author.link_karma,
                    #     "accountCreated": comment.author.created_utc
                    #   } if comment.author is not None and not hasattr(comment.author, 'is_suspended') else "null"],
                    "body": comment.body,
                    "created_utc": comment.created_utc,
                    "edited": comment.edited,
                    "id": comment.id,
                    "is_root": comment.is_root,
                    "is_submitter": comment.is_submitter,
                    "permalink": comment.permalink,
                    "score": comment.score,
                    "ups": comment.ups
                })
            top25Submissions.append({
                "id": submission.id,
                "title": submission.title,
                "flair": submission.link_flair_text,
                "subreddit": submission.subreddit_name_prefixed,
                "created_utc": submission.created_utc,
                "upvote": submission.ups,
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "selfText": submission.selftext,
                "selfUrl": submission.url,
                "permalink": submission.permalink,
                "shortlink": submission.shortlink,
                "author": submission.author_fullname if hasattr(submission, 'author_fullname') else "null",
                # "author": [{
                #     "id": submission.author.id,
                #     "name": submission.author.name,
                #     "commentKarma": submission.author.comment_karma,
                #     "submissionKarma": submission.author.link_karma,
                #     "accountCreated": submission.author.created_utc,
                #     } if submission.author is not None and not hasattr(submission.author, 'is_suspended') else "null"],
                "commentCount": submission.num_comments,
                "comments": comments
            })
        create_submission_json(top25Submissions, subreddit)


def create_submission_json(submissions: list, subreddit):
    path = "output/" + subreddit
    file = str(time.time()) + ".json"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(path, file), "w") as f:
        json.dump(submissions, f)


top25scanner()
<<<<<<< HEAD
end = datetime.datetime.now()
totalRun = end - start
print(totalRun)
>>>>>>> 4a098b5 (restructured a bit, abstracted out praw credentials)
=======
>>>>>>> c2a3682 (refactored code & returning larger json rather than 1 json per thread)

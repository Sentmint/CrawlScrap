from api.services import prawservice as praw
from api.resources import subreddits as subs
import json
import time
import os
from pathlib import Path


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


def top25scanner():
    reddit = praw.prawConnection()
    for subreddit in subs.subredditList():
        top25 = reddit.subreddit(subreddit).hot(limit=25)
        top25Submissions = []
        for submission in top25:
            if submission.stickied:
                continue
            comments = []
            curr = reddit.submission(submission.id)  # Grabs the front page ids to be scanned for comments

            # TODO: Move this to ETL if quick way to filter out old comments is needed
            # curr.comment_sort = "new"  # Sort comments by new to fetch only new comments
            # if comment.created_utc < valueToScan:
            #     continue

            curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children
            for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
                if comment.author is None:  # Handles cases of comment being deleted by user or removed by Reddit
                    continue
                comments.append({
                    "commentAuthor": [{
                        "id": comment.author.id,
                        "name": comment.author.name,
                        "commentKarma": comment.author.comment_karma,
                        "submissionKarma": comment.author.link_karma,
                        "accountCreated": comment.author.created_utc
                    }],
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
                "author": [
                    {"id": submission.author.id,
                     "name": submission.author.name,
                     "commentKarma": submission.author.comment_karma,
                     "submissionKarma": submission.author.link_karma,
                     "accountCreated": submission.author.created_utc,
                     }],
                "commentCount": submission.num_comments,
                "comments": comments
            })
        create_submission_json(top25Submissions, subreddit)


def create_submission_json(submissions: list, subreddit):
    testing = json.dumps(submissions)
    print(testing)
    path = "Reddit-Scraper/api/output/" + subreddit
    Path(path).mkdir(parents=True, exist_ok=True)

    with open("PersonalFinanceCanada.json", "w") as f:
        json.dump(submissions, f)

    # path = 'Reddit-Scraper/api/output/' + subreddit
    # file = 'subreddit.json'
    # test = os.path.join(path, file)
    # with open(test, 'w') as file:
    #     json.dump(submissions, file)


top25scanner()

from pathlib import Path
from reddit_service import praw_service as praw
from reddit_resource import subreddits as subs
import logging
import json
import time
import os


logging.basicConfig(level=logging.DEBUG)


def top_25_scanner():
    reddit = praw.praw_connection()
    for subreddit in subs.subreddit_list():
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
    path = "../data_collected/reddit/" + subreddit
    file = str(time.time()) + ".json"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(path, file), "w") as f:
        json.dump(submissions, f)


top_25_scanner()

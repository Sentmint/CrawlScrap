from pathlib import Path
from reddit_service import praw_service as praw
from reddit_resource import subreddits as subs
import logging
import json
import time
import os
from producer import publish_stock

logging.basicConfig(level=logging.DEBUG)

def test_1_scan():
    reddit = praw.praw_connection()
    subreddit = subs.subreddit_list()[0]
    top25Submissions = []
    top25 = reddit.subreddit(subreddit).hot(limit=25)
    for submission in top25:
        if submission.stickied:
            continue
        comments = []
        curr = reddit.submission(submission)
        curr.comments.replace_more(limit=1, threshold=0)
        for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
            comments.append({
                "comment_author": comment.author_fullname if hasattr(comment, 'author_fullname') else "null",
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
            "self_text": submission.selftext,
            "self_url": submission.url,
            "permalink": submission.permalink,
            "shortlink": submission.shortlink,
            "author": submission.author_fullname if hasattr(submission, 'author_fullname') else "null",
            "comment_count": submission.num_comments,
            "comments": comments
        })
        publish_stock(top25Submissions)
        create_submission_json(top25Submissions, subreddit)
        break


def create_submission_json(submissions: list, subreddit):
    path = "../data_collected/reddit/" + subreddit
    file = str(time.time()) + ".json"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(path, file), "w") as f:
        json.dump(submissions, f)

    os.remove(path + "/" + file)

test_1_scan()

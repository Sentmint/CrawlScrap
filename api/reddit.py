from api.services import prawservice as praw
from api.resources import subreddits as subs
from api.dtos import redditdto as dto
from pathlib import Path
import datetime
import json
import time
import os

reddit = praw.prawConnection()
started = str(time.time())
Path("/Reddit-Scraper/api/output/" + started).mkdir(parents=True, exist_ok=True)


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

def build_submission_json(submission: dto.SubmissionDto, comments: list):
    commentsCollection = []
    for comment in comments:
        if comment.body == "[deleted]":
            continue
        curr = {
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
        }
        commentsCollection.append(curr)
    return {
        "id": submission.id,
        "title": submission.title,
        "subreddit": submission.subreddit_name_prefixed,
        "created_utc": submission.created_utc,
        "upvote": submission.ups,
        "upvote_ratio": submission.upvote_ratio,
        "score": submission.score,
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
        "comments": commentsCollection
    }


def create_submission_json(thread: dict):
    path = '/Reddit-Scraper/api/output/' + started + '.JSON'
    file = str(time.time())
    with open(os.path.join(path, file), 'w') as file:
        json.dump(thread, file)


def top25scanner():
    for subreddit in subs.subredditList():
        top25 = reddit.subreddit(subreddit).hot(limit=25)
        for thread in top25:
            if thread.stickied:
                continue
            submission = dto.SubmissionDto(
                thread.author,
                thread.created_utc,
                thread.id,
                thread.num_comments,
                thread.permalink,
                thread.score,
                thread.selftext,
                thread.shortlink,
                thread.subreddit_name_prefixed,
                thread.title,
                thread.ups,
                thread.upvote_ratio,
                thread.url
            )
            comments = []
            curr = reddit.submission(thread.id)  # Grabs the front page ids to be scanned for comments
            curr.comment_sort = "new"  # Sort comments by new to fetch only new comments
            curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children
            for comment in curr.comments.list():  # Create a list of all comments to eliminate hierarchy
                # if comment.created_utc < valueToScan:
                #     continue
                comments.append(dto.CommentDto(
                    comment.author,
                    comment.body,
                    comment.created_utc,
                    comment.edited,
                    comment.id,
                    comment.is_root,
                    comment.is_submitter,
                    comment.permalink,
                    comment.score,
                    comment.ups
                ))
            create_submission_json(build_submission_json(submission, comments))


start = datetime.datetime.now()
top25scanner()
end = datetime.datetime.now()
totalRun = end - start
print(totalRun)

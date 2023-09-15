import json
import logging
import os
import sys
import time
import re
from pathlib import Path
import praw.models
from reddit_resource import subreddits as subs
from reddit_service import praw_service as p
script_dir = os.path.dirname(os.path.abspath(__file__))
crawl_scrape_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(crawl_scrape_dir)
from stock.stock_search import find_stock
from producer import publish_stock

logging.basicConfig(level=logging.DEBUG)

cli_arguments = sys.argv[1:]

def top_25_scanner():
    reddit = p.praw_connection()
    for subreddit in subs.subreddit_list():
        top25 = reddit.subreddit(subreddit).hot(limit=25)
        top25Submissions = []
        for submission in top25:
            if submission.stickied:
                continue
            comments = []
            curr = reddit.submission(submission)  # Grabs the front page ids to be scanned for comments
            curr.comments.replace_more(limit=None, threshold=0)  # Fetch all comments and their children
            for comment in curr.comments.list():  # Creates a list of all comments to eliminate hierarchy
                if not isinstance(comment, praw.models.Comment):
                    continue
                comments.append({
                    "comment_author": comment.author_fullname if hasattr(comment, 'author_fullname') else "null",
                    ### This was removed because it requires additional API calls
                    ### Slows down the scraper as we only have 60 API calls available per minute.
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
                "self_text": submission.selftext,
                "self_url": submission.url,
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
                "comment_count": submission.num_comments,
                "comments": comments
            })
        publish_stock(top25Submissions)
        create_submission_json(top25Submissions, subreddit)


def create_submission_json(submissions: list, subreddit):
    path = "../data_collected/reddit/" + subreddit
    file = str(time.time()) + ".json"
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(path, file), "w") as f:
        json.dump(submissions, f)

    if cli_arguments:
        # TODO: Has to be modified for "STM-114:dynamic output directories" later on
        with open("../data_collected/reddit/" + subreddit + "/" + file) as f:
            data = json.load(f)
            stuff = find_stock(sys.argv[1:])
            for key, value in stuff.items():
                filtered_json = []
                for submission in data:
                    relevant_comments = [
                        # Will look for a complete ticker match within the comment body, or
                        # Will look for a word match within the body.
                        # For example, "Tesla Inc. Common Stock" and "I love stocks" will return a match,
                        # whereas "Tesla Inc. Common Stock" and "I love Tes" (should) not.

                        # TODO: Potentially look into removing common words such as "stock" from nasdaq.csv and only keep company name
                        comment for comment in submission['comments'] if key.lower() in comment['body'].lower() or
                                                                         any(re.search(r"\b" + re.escape(word.lower()) +
                                                                                       r"\b", comment['body'].lower())
                                                                             for word in value.split())
                    ]
                    # If we find any matches, replace the old list in the submission object with the new filtered list
                    # We build a new JSON using the old one with only filtered comments as a result
                    if relevant_comments:
                        filtered_submission = submission.copy()
                        filtered_submission['comments'] = relevant_comments
                        filtered_json.append(filtered_submission)

                #TODO: As is, we will most likely have duplicate comments since a new sub-directory is being made for every
                # cli arg. Could just do one output for all args, but then it would be difficult to tell which cli arg
                # comment had a match for. Discuss with team later.

                filter_path = "../data_collected/reddit/" + subreddit + "/" + key
                Path(filter_path).mkdir(parents=True, exist_ok=True)
                file = str(time.time()) + ".json"
                with open(os.path.join(filter_path, file), "w") as filtered:
                    json.dump(filtered_json, filtered)


top_25_scanner()

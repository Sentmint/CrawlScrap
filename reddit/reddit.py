import json
import logging
import os
import time
import praw.models
from datetime import datetime
from pathlib import Path
from reddit_resources import reddit_config as config
from reddit_service import praw_service as p
from reddit_service import logger as log
from reddit_service.producer import publish_stock

def subreddit_scanner():
    reddit = p.praw_connection()
    reddit_config = config.getConfig()
    log.formatter()
    logging.info("config: ", reddit_config)
    for config_data in reddit_config["Subreddits"]:
        subreddit = config_data["Name"]
        if not subreddit:
            continue

        logging.info("Scanning subreddit: " + subreddit)
        collected_comments = []
        try:
            thread_limit = int(os.environ.get('REDDIT_THREAD_LIMIT', "25"))
            threads = reddit.subreddit(subreddit).hot(limit = thread_limit)
            logging.info("Successfully collected the front page submissions of " + subreddit)
        except:
            logging.error("Error encountered when collecting the front page submissions on the subreddit: " + subreddit)
            continue
        
        for submission in threads:
            # For now we're skipping mod-related posts since they're not relevant to our project
            if submission.stickied:
                continue
            logging.info("Scanning submission: " + submission.title)
            comments = []

            # TODO: There is a bug in the Reddit API limitation logic. It's been reported but no fix yet.
            # As a result, we may sometimes miss comments. Changing our threshold limit here may not fix the issue entirely.
            try:
                 # Fetch all comments and their children
                submission.comments.replace_more(limit=None, threshold=0) 
                logging.info("Successfully collected " + str(len(submission.comments.list())) + " comments")
            except:
                logging.error("API returned a non-ok response. Likely due to API Limit bug. Skipping submission: " + submission.title)
                continue

            # Creates a list of all comments to eliminate hierarchy
            # Hierarchy can be inferred if it has a use-case (which comment belongs to which parent)
            for comment in submission.comments.list():  
                if not isinstance(comment, praw.models.Comment):
                    continue

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
            collected_comments.append({
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
        
        logging.info("Attempting to create JSON for scanned subreddit: " + subreddit)
        if "Filter" in config_data: 
            filtered_comments = filter_submission_json(collected_comments, config_data["Filter"])
            publish_stock(filtered_comments, '','reddit-in', logging)
            create_submission_json(filtered_comments, subreddit)
        else:
            publish_stock(collected_comments, '','reddit-in', logging)
            create_submission_json(collected_comments, subreddit)


def filter_submission_json(submissions: list, filter: dict):
    filtered_submissions = []

    if "Keyword" in filter:
        keyword = filter["Keyword"]
    else:
        keyword = None 

    if "StartTimeUTC" in filter:
        utc = datetime.strptime(filter["StartTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
        unix = utc.timestamp()
    else:
        unix = None

    for submission in submissions:
        filtered_comments = [
            comment for comment in submission["comments"]
            if
            (
                (not keyword or any(word in comment["body"].lower() for word in [k.lower() for k in keyword])) and
                (not unix or comment["created_utc"] >= unix)
            )
        ]

        if filtered_comments:
            submission["comments"] = filtered_comments
            filtered_submissions.append(submission)

    return filtered_submissions


def create_submission_json(submissions: list, subreddit):
    try:
        init_path = os.environ.get('REDDIT_OUTPUT_PATH', "../data_collected/reddit/") 
        final_path = os.path.join(init_path, subreddit)
        file = str(time.time()) + ".json"
        Path(final_path).mkdir(parents=True, exist_ok=True)

        with open(os.path.join(final_path, file), "w") as f:
            json.dump(submissions, f)
            logging.info("Successfully created JSON for subreddit: " + subreddit)
    except:
        logging.error("Error encountered when creating JSON for subreddit: " + subreddit)


subreddit_scanner()

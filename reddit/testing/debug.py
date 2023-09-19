from pathlib import Path
from reddit_service import praw_service as praw
from reddit_resource import subreddits as subs
import logging
import json
import time
import os


logging.basicConfig(level=logging.DEBUG)

def debug():
    reddit = praw.praw_connection()
    test00 = reddit.comment("g7y99tq")
    test01 = reddit.comment("i1s9pb8")
    test02 = reddit.submission("j6gabx")

debug()
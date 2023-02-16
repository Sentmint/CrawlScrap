from praw.models import Redditor


class SubmissionDto:

    def __init__(self, author: Redditor, created_utc: float, id: str, flair: str, num_comments: str, permalink: str,
                 score: int, self_text: str, shortlink: str, subreddit_name_prefixed: str, title: str, ups: int,
                 upvote_ratio: float, url: str) -> None:
        self.author = author
        self.created_utc = created_utc
        self.id = id
        self.flair = flair
        self.num_comments = num_comments
        self.permalink = permalink
        self.score = score
        self.self_text = self_text
        self.shortlink = shortlink
        self.subreddit_name_prefixed = subreddit_name_prefixed
        self.title = title
        self.ups = ups
        self.upvote_ratio = upvote_ratio
        self.url = url


class CommentDto:

    def __init__(self, author: str, body: str, created_utc: float, edited: bool, id: str,
                 is_root: bool, is_submitter: bool, permalink: str, score: int, ups: int) -> None:
        self.author = author
        self.body = body
        self.created_utc = created_utc
        self.edited = edited
        self.id = id
        self.is_root = is_root
        self.is_submitter = is_submitter
        self.permalink = permalink
        self.score = score
        self.ups = ups

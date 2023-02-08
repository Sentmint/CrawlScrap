Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)

When this application is run, it will scan and fetch comments from the front page of the given subreddits <br>
Folders corresponding to the scanned subreddit will be created [here](api/output) (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 

When this application is run, it will scan and fetch comments from the front page of the given subreddits <br>
Folders corresponding to the scanned subreddit will be created here (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 

Requires a Reddit account with a script application defined. Quick guide available [here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768)

The credentials are currently stored within the services folder [here](api/services) using a `secrets.py` folder with a `CLIENT_ID` , `CLIENT_SECRET` , and `USER_AGENT` field which are populated with the given credentials from the Reddit application we create.

`Note: This should probably be changed to use ENV later`


## API Limitations & API Definitions

There are 60 API calls available to us per minute. To avoid bad requests or potentially getting banned off of Reddit, the PRAW wrapper will enforce this restriction on its own.

Attributes available for each of these return Objects can be seen here

| API | Range | Description |
| --- | --- | --- |
| GET Subreddit Submissions | 0-60 | Fetches number of desired submissions. A reddit "page" has 25 submissions; we can also specify how we want the page to be sorted before fetching, i.e. "BEST, TOP, CONTROVERSIAL", etc.
| Get Comments | 0-2048 | Fetches number of desired comments. We can specify how we want the comments to be sorted before fetching here as well.
| Get Author | 1 | Gets all information about the given author

## Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)

When this application is run, it will scan and fetch comments from the front page of the given subreddits <br>
Folders corresponding to the scanned subreddit will be created [here](data_collected/reddit) (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 

## Connecting

Requires a Reddit account with a script application defined. Quick guide available [here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768)

The credentials for the PRAW connection are fetched from an env file that has to be created and populated manually when running this application for the first time. There is a `.env.template` available [here](.env.template); the three credentials needed for the Reddit application are `CLIENT_ID`, `CLIENT_SECRET`, and `USER_AGENT`.

<br>

## API Limitations & API Definitions

There are 60 API calls available to us per minute. To avoid bad requests or potentially getting banned off of Reddit, the PRAW wrapper will enforce this restriction on its own.

Attributes available for each of these return Objects can be seen here

| API | Limit | Description |
| --- | --- | --- |
| GET Subreddit Submissions | 60 | Fetches number of desired submissions. A reddit "page" has 25 submissions; we can also specify how we want the page to be sorted before fetching, i.e. "BEST, TOP, CONTROVERSIAL", etc.
| Get Comments | 2048 | Fetches number of desired comments. We can specify how we want the comments to be sorted before fetching here as well.
| Get Author | 1 | Gets all information about the given author

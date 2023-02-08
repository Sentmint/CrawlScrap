<<<<<<< HEAD
Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)

When this application is run, it will scan and fetch comments from the front page of the given subreddits <br>
Folders corresponding to the scanned subreddit will be created [here](api/output) (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 
=======
## Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)
>>>>>>> 0668ebe (Final README update)

When this application is run, it will scan and fetch comments from the front page of the given subreddits <br>
Folders corresponding to the scanned subreddit will be created here (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 

Requires a Reddit account with a script application defined. Quick guide available [here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768)

<<<<<<< HEAD
The credentials are currently stored within the services folder [here](api/services) using a `secrets.py` folder with a `CLIENT_ID` , `CLIENT_SECRET` , and `USER_AGENT` field which are populated with the given credentials from the Reddit application we create.
=======
The credentials are currently stored within the services folder [here](api/services/) using a `secrets.py` folder with a `CLIENT_ID` , `CLIENT_SECRET` , and `USER_AGENT` field which are populated with the given credentials from the Reddit application we create.
>>>>>>> 0668ebe (Final README update)

`Note: This should probably be changed to use ENV later`


<<<<<<< HEAD
## API Limitations & API Definitions

There are 60 API calls available to us per minute. To avoid bad requests or potentially getting banned off of Reddit, the PRAW wrapper will enforce this restriction on its own.

Attributes available for each of these return Objects can be seen here

| API | Range | Description |
| --- | --- | --- |
| GET Subreddit Submissions | 0-60 | Fetches number of desired submissions. A reddit "page" has 25 submissions; we can also specify how we want the page to be sorted before fetching, i.e. "BEST, TOP, CONTROVERSIAL", etc.
| Get Comments | 0-2048 | Fetches number of desired comments. We can specify how we want the comments to be sorted before fetching here as well.
| Get Author | 1 | Gets all information about the given author
=======
| JSON Prefix | Description | 
| - | - |
| t1_ | Comment chain (?) | 
| t2_ | Account; author of a comment or thread | 
| t3_ | Specific comment within a thread; this is how child comments reference a parent comment/thread. <br> For example: A comment will be given id "j654l1g", comments replying to it will have tag "parent_id": "t3_j654l1g". <br> This chain begins at a lone comment in a thread whose parent_id will reference the thread itself. 
| t4_ | Message(?) | 
| t5_ | Subreddit(?) | 
| t6_ | Award | 
>>>>>>> 0668ebe (Final README update)

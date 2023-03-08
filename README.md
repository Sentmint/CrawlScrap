<details>
<summary>Testing</summary>

</details>

# Data Collection

The collection of data scraped from various online website sources:
| Source:                           | Summary: |
|---------                          |----------|
| 1. Twitter (w/o API usage)        | Twitter Cards Scraper Python using Selenium                                       |
| 2. Reddit (w/ API usage)          |  User can provide a list of subreddits to scan. For each subreddit, the top 25 submissions (front page) of the subreddit will be scanned and the body of each comment within those 25 submissions will be stored with additional data such as upvote ratio or submission time     |
| 3. Yahoo (w/ API usage)       |   TBD. Alpha Vantage.    |
|                                   |          |





<summary><font size="5"> Twitter </font></summary>


## Objective
User Tweet Cards Content Scraper on Twitter

## Overview Workflow
    1. (Navigation) Log into Twitter --> Searches inputted keyword query ('ie: #TSLA') --> Select tab option (ie: 'Latest')

    2. (Collection) EXTRACTS & COLLECTS Tweet Cards seen on page --> Scrolls --> REPEAT until condition met to stop... (View "scroll_to_bottom" function)

    3. (Storage) --> STORE all Tweet Cards extracted & collected in specified file format

## Important Details

### Tools and Technologies Used
    - Python
    - Selenium

### Performance (Runtime)
    Note: Depends on the type of user content posted at the time of application execution
   
   <u>  <b> Archived Milestone Iterations (Rough Estimates)  </b> </u>
   
    Runtime: O(n^2) 

    | (End of Page) | (Minutes) |
    | Scroll Count  | Time      |
    |---------------|-----------|
    | ~110          | ~7.5      |
    |               | ~10-15    |
    | ~55           | ~7-8      |
    | ~73           | ~4.5      |
    | ~             | ~         |
    |               |           |

### Notes

    (In General: SETUP)
 - Runs on Chrome web browser driver
 - Includes ability to handle unexpected lost/failure connection status to webpage: saves and overwrites extracted/collected data up to that point of failed connection
 - Forces fullscreen for best/foolproof results (Certain elements only appear with certain resolutions)
 - Uses dummy Twitter account (Creds in .env variable file)

        (COLLECTION)
 
 - Filters DURING collection of tweet cards: view docstrings of <i> EXTRACT </i> and <i> COLLECT </i> functions (1 scroll collects about ~10 tweet cards)
 - Condition to stop infinite scrolling: (MATCHING Y scroll pos of current VS new scroll height pos   OR   scroll counter limit) 

        (STORING)
 
 - Currently written to CSV and Binary file
 - Send written data for further transformation/cleaning of data within ETL pipeline



<details>

<summary><font size="5"> Reddit </font></summary>

# 

## Built using the Python Reddit API Wrapper [PRAW](https://praw.readthedocs.io/en/latest/index.html)

When this application is run, it will scan and fetch comments from the front page of the given subreddits. <br>
Folders corresponding to the scanned subreddit will be created [here](data_collected/reddit) (if needed) and populated with a JSON; the JSON's filename will be when the JSON was produced. 

## Connecting

Requires a Reddit account with a script application defined. Quick guide available [here](https://towardsdatascience.com/scraping-reddit-data-1c0af3040768)

The credentials for the PRAW connection are fetched from an env file that has to be created and populated manually when running this application for the first time. There is a `.env.template` available [here](.env.template); the three credentials needed for the Reddit application are `CLIENT_ID`, `CLIENT_SECRET`, and `USER_AGENT`.



## Setup & Running 

### Version requirements
``python --version`` <br>
``Python 3.10.10`` <br> <br>
``pip show praw`` <br>
``Name: praw`` <br>
``Version: 7.6.1`` <br>

### Setting up desired subreddits to be scanned
The reddit scraper will evaluate a given array of subreddit strings defined in ``..\CrawlScrape\reddit\reddit_resource\subreddits.py`` which can be found [here](reddit/reddit_resource/subreddits.py)

### Execution
Enter the directory containing the reddit.py file: ``..\CrawlScrape\reddit\reddit.py`` <br>
Application will start running once the command ``python reddit.py`` is entered
Debugging is enabled by default, so the user will see each API call and it's response. <br>
![prawDebugResponse](reddit/readme_resources/prawDebugResponse.png)


## API Limitations & API Definitions

There are 60 API calls available to us per minute. To avoid bad requests or potentially getting banned off of Reddit, the PRAW wrapper will enforce this restriction on its own.

Attributes available for each of these return Objects can be seen here

| API | Limit | Description |
| --- | --- | --- |
| GET Subreddit Submissions | 60 | Fetches number of desired submissions. A reddit "page" has 25 submissions; we can also specify how we want the page to be sorted before fetching, i.e. "BEST, TOP, CONTROVERSIAL", etc.
| Get Comments | 2048 | Fetches number of desired comments. We can specify how we want the comments to be sorted before fetching here as well.
| Get Author | 1 | Gets all information about the given author



</details>

<details>
<summary><font size="5"> Yahoo </font></summary>

# 

## TBD

</details>
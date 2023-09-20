""" Twitter Cards Scraper Python using Selenium
TODO NOTE: OPTIONAL Addons below
- Discuss additional addon options to main functionality:
    - Re-write this program but using Twitter API (IGNORED due to recent news that Twitter API no longer free: Feb 2023)
    - Failed connection data storage: Maybe give user OPTION on how to store data upon connection failure (Overwrite? Store separately?) [Currently: Overwrites data collected file up to point of failure]
    - Setup other web browsers and give user OPTION to choose? [Currently: Chrome]
    - More efficient performance/runtime (Ex: Clearing search box)
(NAVIGATION)
 - Setup which TAB to select and view  [Currently: 'Latest' Tab)
(COLLECTION)
 - DOESNT support certain elements: (Needed or useful to collect and store?)
    - 'tweetTextAddon' = Person referencing tweet below
    - Images/gifs/videos/media text 
    - Look into ignoring all media tags to improve runtime?
 - Edge/Outlier case may exist where user posts content that the webpage css does not exist so crash application?
"""

import time, requests, random, csv, pickle, os, sys
from search_query import search_query_list
from dotenv import load_dotenv #For envrionment variables
from selenium.webdriver import Chrome #Firefox Browser: "Firefox" | Edge Browser: "from msedge.selenium_tools import Edge, EdgeOptions"
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
script_dir = os.path.dirname(os.path.abspath(__file__))
crawl_scrape_dir = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(crawl_scrape_dir)
from stock.stock_search import find_stock
from producer import publish_stock
from log_format import setup_logger

####################### FUNCTIONS ##########################
def valid_connection_status():
    """ Function checks connection status before interacting with webpage
        Returns True if valid connection to webpage; False if not
    """
    try:
        currentURL = driver.current_url
        logger.debug(currentURL)
        response = requests.head(currentURL) # Send HEAD request to the webpage
        logger.debug(response)
        return (True) if (response.status_code == 200) else (False) # Ternary operator to check connection status
    except Exception as eMsg:
        logger.debug("<< Connection to Webpage FAILED/LOST >> \n \
            Function 'valid_connection_status' failed exception: << " + str(eMsg) + " >>")
        return False


def scroll_to_bottom():
    """ Function handles infinite scrolling; scrolls bottom of page until no more tweets are loaded (or scroll counter limit condition satisfied) using Selenium
        - Includes flexible way to TEST with sample size (Within while loop break condition):  MATCHING Y scroll pos   OR   manually set scroll counter limit
        - Includes handling of checking connection status to webpage (Function)
        - Includes EXTRACT and COLLECT of tweet cards shown on page (Function)
        If bottom of page reached/condition satisifed, BREAKS out of while loop and function; ELSE continously scrolls/loops
    """
    tweetIdList = set() # Handle omitting duplicates during collection of tweet cards
    scrollCount = 0 # For TESTING with sample size purposes

    # Get CURRENT scroll height
    currentScrollHeightPos = driver.execute_script("return Math.max( \
        document.body.scrollHeight, document.body.offsetHeight, \
        document.documentElement.clientHeight, \
        document.documentElement.scrollHeight, \
        document.documentElement.offsetHeight );")

    while True:
        #-- Function: Check connection status before interacting with webpage
        if valid_connection_status():
            #-- Function: SCRAPE and COLLECT all the tweets loaded on entire page using Selenium
            collect_tweet_data_payload(tweetIdList)

            # Scroll to bottom of page
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(30) # To allow enough load time for webpage (May need more due to varying sizes/dependent on tweet card content loaded)
            scrollCount += 1
            logger.debug("-- Scroll Count: " + str(scrollCount) + " --")

            #-- Condition to EXIT loop (1. MATCHING Y scroll pos   OR   2. Scroll counter limit)
            ######## START ########
            ## <<  1. >>> Have we reached bottom of the page/Is there no more new tweets to load?
            # Get NEW scroll height once scrolled
            newScrollHeightPos = driver.execute_script("return Math.max( \
                document.body.scrollHeight, document.body.offsetHeight, \
                document.documentElement.clientHeight, \
                document.documentElement.scrollHeight, \
                document.documentElement.offsetHeight );")

            # Bottom of the page reached if CURRENT Y scroll height pos MATCHES with NEW Y scroll height pos (No more scrolling/change in Y scroll height pos)
            if newScrollHeightPos == currentScrollHeightPos:
                logger.info("-- [All Tweets on Page LOADED in] --")
                break
            currentScrollHeightPos = newScrollHeightPos # Otherwise update the last scroll height (currentScrollHeightPos) with newly scrolled Y position
            ####### END #########

            #-- [OR] --

            # ####### START ########
            # ## <<  2. >>>
            # # Mainly just for TESTING with sample size (Change # to set scroll limit)
            # testWithSampleSize = 3
            # if scrollCount == testWithSampleSize: break
            # ###### END #########

        else: # Invalid connection status
            logger.debug("INVALID connection status")
            break


def extract_tweet_data_payload(tweet):
    """ Function EXTRACTS specific data details/content from EACH Tweet Card using Selenium 
        - Arguement 'tweet' is a single tweet card shown on the webpage 
        - Extracts and Stores: username, twitterHandle, datePosted, replyCount, retweetCount, LikeCount, tweetText
        - Data filtering: 
            - OMIT ads/sponsors/non-users by checking for no date timestamps        
        Returns: A Tuple Object containing specific extracted info from a specific tweet card
    """
    username = tweet.find_element("xpath", './/span').text # Get Username  (Elements identified earlier are removed from DOM due to page refresh)
    twitterHandle = tweet.find_element("xpath", './/span[contains(text(), "@")]').text # Get Twitter Handle
    try:
        datePosted = tweet.find_element("xpath", './/time').get_attribute('datetime') # Get Timestamp string
    except NoSuchElementException as eMsg:
        logger.info("Tweet Card Content Exception: << " + str(eMsg) + " >> \n \t [It was likely not a user! Filtered Out and Omitted tweet]") # If no date found, NOT a user (Ex: Ad/sponsor)
        return

    # Get Tweet DATA Content paylod (TEXT + addons)
    tweetText = tweet.find_element("xpath", './/div[@data-testid="tweetText"]').text  # Tweet itself
    if args_provided:
        norm_tweet = tweetText.lower()
        #TODO: Study domain of this. A lot of posts have $TICKER, especially the TSX ones. Fix for later when querying of TSX is fixed.
        if not (query.lower() in norm_tweet or ("#"+query.lower() in norm_tweet) or chosen_search[query].lower() in norm_tweet):
            logger.info("Tweet does not contain text relating to the searched stock. It will be skipped.")
            return None


    # tweetTextAddon = tweet.find_element("xpath", '//div[@class="css-1dbjc4n r-1ssbvtb r-1s2bzr4"]')  # Tweet person is referring to (Image, Reply, Article, Link, etc.)
    # textContent = tweetText + " \t " + tweetTextAddon

    # Get COUNTERS (Comment/Retweets/Likes)  
    replyCount = tweet.find_element("xpath", './/div[@data-testid="reply"]').text # Reply Count
    retweetCount = tweet.find_element("xpath", './/div[@data-testid="retweet"]').text # Retweet Count
    LikeCount = tweet.find_element("xpath", './/div[@data-testid="like"]').text # Likes Count

    # Combine into Tuple: Tweet data
    tweetData = (username, twitterHandle, datePosted, replyCount, retweetCount, LikeCount, tweetText)
    return tweetData


def collect_tweet_data_payload(tweetIdList):
    """ Function COLLECTS list of Tweets payload extracted using Selenium 
        - Arguement 'tweetIdList' is the list of UNIQUE tweet cards identified/determined by custom made ID condition upon collection
        - 1 scroll, collects/recognizes ~10 tweet cards at a time in FOR loop
        - Includes EXTRACT of tweet cards shown on page (Function)
        - Includes OMITTING duplicates collected by creating unique ID for each item
        Returns: Finalized list of Tuple Objects which are all the tweet cards extracted and collected
    """
    driver.implicitly_wait(10) # To allow enough load time for webpage
    tweetCardList = driver.find_elements("xpath", '//article[@data-testid="tweet"]') # Get entire Tweet Card Payload element
    for tweet in tweetCardList: #Commented out "[-15:]" range on list which views LAST 15 items (Supposedly removes need to recheck every tweet in list & reduces duplicates) [Unsure if useful with this implementation anymore]
        data = extract_tweet_data_payload(tweet) #-- Function: extracts info from EACH Tweet Card using Selenium
        if data: # If tweet card content extracted is NOT null
            #-- Check for duplicates collected (Make our OWN tweet ID)
            tweetId = ''.join(data) # Create UNIQUE ID by concat elements of tweet into 1 string
            if tweetId not in tweetIdList:
                tweetIdList.add(tweetId)
                payloadCollected.append(data) # Finalized extracted & collected tweet cards list contents to be store
    logger.info("-- Extracted and Collected Tweets Payload --")


def store_tweet_data_payload(searchQuery, dataPayload):
    """ Function STORES list of Tweets payload extracted and collected in desired format using Selenium.
        Containing the Extracted & Collected tweet cards, write to a:
        - CSV file
        or/and
        - BINARY file
    """
    # print(os.getcwd()) # Show current dirc (Test)
    # print(os.listdir("../")) # Show files (Test)

    #-- Check for invalid character in directory. Currently this is only ":" for the case of :TSX
    searchQuery = searchQuery.replace(":", "_")

    #-- Create dir path if not already exist
    if not os.path.exists('../data_collected/twitter/' + searchQuery + "/"):
        os.makedirs('../data_collected/twitter/' + searchQuery + "/")

    directoryPath = '../data_collected/twitter/' + searchQuery + "/"
    createdfileName = str(time.time()) + "_" + searchQuery 

    #-- TO CSV Format
    csvFile = os.path.join(directoryPath, createdfileName + ".csv")
    with open(csvFile, 'w', newline='', encoding='utf-8') as fileCSV: # Writing to file
        header = ['Username', 'Twitter Handle', 'Timestamp',
                  "Comments", "Retweets", "Likes", 'Text']
        writer = csv.writer(fileCSV)
        writer.writerow(header)
        writer.writerows(dataPayload)

    #-- To Binary Format
    binaryFile = os.path.join(directoryPath, createdfileName + ".bin")
    with open(binaryFile, 'wb') as fileBin:
        header = ['Username', 'Twitter Handle', 'Timestamp',
                "Comments", "Retweets", "Likes", 'Text']
        data = [header] + dataPayload
        pickle.dump(data, fileBin)

    logger.info("<< STORED Tweets Payload >>")

    #-- Send collected Twitter data payload to RabbitMQ Queue
    publish_stock(binaryFile,'','scraped_data', logger)


# ----------------------------------------------------- (DIVIDER) -----------------------------------------------------


####################### LOGIC ##########################
startTime = time.time() # Time Keeper
logger = setup_logger() # Logging Messages
load_dotenv() # Load environment variables from .env file

#-- Create Instance of Webdriver
user_agents_list = [ # NOTE: NEED to randomize user agent every time run to NOT get flagged by Twitter that we are bot scraping and they blacklist (ie: 403 forbidden us access)
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36', #'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]
options = ChromeOptions()
# (In order to run CI agent account on Ubuntu server (within Jenkins Build Environment)
options.add_argument("--no-sandbox") # Bypass OS security model (Has to be first option)
options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
options.add_argument(f'user-agent={random.choice(user_agents_list)}') # Needed for headless mode
options.add_argument('--headless') # Runs Chrome Driver without actual browser [NOTE: Comment out to debug WITH browser]

# (IF needed JIC for headless mode not working)
options.add_argument("--proxy-server='direct://'") # Proxy arguments fix the error of headless not launching fast enough, resulting in the "cannot find element" error.
options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--disable-gpu") # [Unnecesary if have --headless flag] Applicable to windows os only 
# options.add_argument('--ignore-certificate-errors') #Fix possible invalid SSL certificate
# options.add_argument('--allow-running-insecure-content') #Fix possible invalid SSL certificate
# options.add_argument("--allow-insecure-localhost")
# options.add_argument('--user-data-dir=~/.config/google-chrome') # Supposed fix to permission issue with CI agent account on Ubuntu server
options.add_argument("--disable-extensions") # disabling extensions
options.add_argument("--disable-infobars") # disabling infobars (Info text sometimes given by browser)
options.add_argument("--window-size=1920,1080") # JIC if screen too small (Fix bug in headless mode)
options.add_argument("--start-maximized") # Double JIC: open Browser in maximized mode [Some elements only found on bigger screen resolution]

options.add_experimental_option('excludeSwitches', ['enable-logging']) # This IGNORES unfixable chrome web driver logs
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options) #Firefox: "Firefox" | Edge: "options = EdgeOptions(); options.use_chromium = True; driver = Edge(options=options)"
logger.debug("--- Created Chrome driver ---  ")

driver.implicitly_wait(20) # Better Practice to use this than time.sleep() (Unlike 'time.sleep()', 'driver.implicitly_wait()' is NOT a FIXED wait time) [Gives more time to load webpage to find elements]

#-- Go to first landing page [TRAVERSING Thru Twitter]
driver.get("https://www.twitter.com/login")

#-- Login to Twitter --
username = driver.find_element("xpath", '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]') #@type="text"
username.send_keys(os.environ.get("TWITTER_USERNAME"))
username.send_keys(Keys.RETURN) #-- Same as user clicking "NEXT" Button

#-- (FIRST) If unusal activity confirmation page appears (User Confirmation via Twitter USERNAME handle!)
try:
    userConfirmation = driver.find_element("xpath", '//input[@data-testid="ocfEnterTextTextInput"]') # User Confirmation screen
    userConfirmation.send_keys(os.environ.get("TWITTER_USER_CONFIRMATION"))
    userConfirmation.send_keys(Keys.RETURN)
except NoSuchElementException:
    logger.info("No Extra User Confirmation Needed (Twitter USERNAME handle)")

driver.implicitly_wait(10) # To allow enough load time for webpage

#-- Enter PSWD Page
pswd = driver.find_element("xpath", '//input[@type="password"]')
pswd.send_keys(os.environ.get("TWITTER_PSWD"))
pswd.send_keys(Keys.RETURN)

#-- (SECOND) If unusal activity confirmation page appears (User Confirmation via EMAIL confirmation code sent!)
try:
    driver.find_element("xpath", '//input[@data-testid="ocfEnterTextTextInput"]') # User Confirmation Code screen/alert appears
    logger.warn("Oopsie! Ran Twitter Scraper consecutively too many times: Requires user confirmation code sent to email or else account temporarily blocked (NOT HANDLED in Code)")
except NoSuchElementException:
    logger.info("No Extra User Confirmation Code Needed (EMAIL confirmation code)")

#-- Check whether any arguments were provided. If they were, call stock_search.py and use the found tickers.
args_provided = False
chosen_search = {}

if sys.argv[1:]:
    try:
        chosen_search = find_stock(sys.argv[1:])
    except Exception as eMsg:
        logger.info("Error while running stock_search function find_stock using cli arguments" + str(eMsg))

if not chosen_search:
    chosen_search_symbols = search_query_list()
else:
    chosen_search_symbols = list(chosen_search.keys())
    args_provided = True


#TODO: Scraper cannot collect :TSX stock posts. Figure out later and fix. scroll_to_bottom causes it.
#-- Iterate through all custom search queries set
for query in chosen_search_symbols:
    if "#" not in query:
        query = "#"+query
    logger.info(query)
    driver.implicitly_wait(20) # To allow enough load time for webpage

    #-- Find search box --
    searchInput = driver.find_element("xpath", '//input[@data-testid="SearchBox_Search_Input"]')

    # (For future iterations): Clear search input box to ensure on next iteration its cleared
    searchInput.send_keys(Keys.BACKSPACE * len(searchInput.get_attribute('value'))) # Slowest solution but only one that works!? (Using Backspaces to clear)

    #-- Search the keyword
    searchInput.send_keys(query)
    searchInput.send_keys(Keys.RETURN)

    #-- Pull historical data -- ## TAB Viewing Options TODO: Select which TAB option to view?
    driver.find_element("xpath", "//span[text()='Latest']").click()

    try:
        payloadCollected = [] # Finalized extracted & collected tweet cards to be stored used in COLLECTION process (NOTE: Initalized here to still be able to store data if failure occurs)

        #-- Scroll to get entire PAGE of Tweets (Either bottom of the page or set limit condition reached) --
        scroll_to_bottom()

    except Exception as eMsg: # Possible Edge case: Element reference lost from DOM due to dynamic loading of page (".click()" or ".text" ref on element may get lost if load too fast)
        logger.debug("Function 'scroll_to_bottom' while loop exception occurred: << " + str(eMsg) + " >>")

    #-- STORE Data Collected
    store_tweet_data_payload(query, payloadCollected)
    logger.info("--- %s Minutes for search query [ %s ] ---" % ( ((time.time() - startTime) / 60) , query))  # Reference for time keeping sake

#-- CLOSE browser to save resources (Good practice)
# driver.close() # Closes focused opened browser window
driver.quit() # Close all (if any) multiple opened browser windows (Better to END program and prevent memory leak errors)
""" Twitter Cards Scraper Python using Selenium
NOTE:
 Overview Objective WorkFlow: 
 1. (Navigation) Log into Twitter --> Searches inputted keyword query ('ie: #TSLA') --> Select tab option (ie: 'Latest')
 2. (Collection) EXTRACTS & COLLECTS Tweet Cards seen on page --> Scrolls --> REPEAT until condition met to stop... (View "scroll_to_bottom" function) 
 3. (Storage) --> STORE all Tweet Cards extracted & collected in specified file format
 Runtime: O(n^2)   ~7.5 min long to complete with Scroll Count ~110 until reach end of page (Milestone Archive: ~10-15min/end of page; ~7-8min/~55 scrolls; ~4.5min/~73 scrolls; )
 - Runs on Chrome web browser driver
 - Includes ability to handle unexpected lost/failure connection status to webpage: saves and overwrites extracted/collected data up to that point of failed connection
 (Setup)
 - Forces fullscreen for best/foolproof results (Certain elements only appear with certain resolutions)
 - Uses dummy Twitter account (Creds in .env variable file)
 (Collection)
 - Filters DURING collection of tweet cards: view docstrings of EXTRACT and COLLECT functions (1 scroll collects about ~10 tweet cards)
 - Condition to stop infinite scrolling: (MATCHING Y scroll pos of current VS new scroll height pos   OR   scroll counter limit) 
 (Storing)
 - Currently written to CSV or/and Binary file
 - Send written data for further transformation/cleaning of data within ETL pipeline
TODO: (OPTIONAL Addons)
- Discuss additional addon options to main functionality:
    - Re-write this program but using Twitter API (IGNORE due to recent news that Twitter API no longer free: Feb 2023)
    - Failed connection data storage: Maybe give user OPTION on how to store data upon connection failure (Overwrite? Store separately?) [Currently: Overwrites data collected file up to point of failure]
    - Setup other web browsers and give user OPTION to choose? [Currently: Chrome]
(Navigation)
 - Setup custom search query navigation OPTIONS: 
    - Search query box [Currently: '#TSLA']
    - Select which TAB to view  [Currently: 'Latest' Tab)
(Collection)
 - DOESNT support certain elements:
    - 'tweetTextAddon' = Person referencing tweet below (Needed or useful to collect and store?)
    - Images/gifs/videos/media text (Needed or useful to collect and store?)
    - Look into ignore all media tags to improve runtime?
"""


import time, requests, logging, getpass, csv, pickle, os
from dotenv import load_dotenv #For envrionment variables
from selenium.webdriver import Chrome #Firefox Browser: "Firefox" | Edge Browser: "from msedge.selenium_tools import Edge, EdgeOptions"
from selenium.webdriver import ChromeOptions 
from selenium.webdriver.chrome.service import Service  
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


####################### FUNCTIONS ##########################
def setup_logger():
    """ Function sets up logger and logging capabilities: organize messages
        - Logger log levels: Debug, Info, Warn, Error, Critial, Fatal
        Returns logger object with custom template to print logs/msgs to devs in console
    """
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG) # SET log level

    # Create log handler and formatter
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter) # Add formatter to handler
    logger.addHandler(handler) # Add handler to logger
    return logger


def valid_connection_status():
    """ Function checks connection status before interacting with webpage
        Returns True if valid connection to webpage; False if not
    """
    try:
        currentURL = driver.current_url
        response = requests.head(currentURL) # Send HEAD request to the webpage
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

            ######## START ########
            # ## <<  2. >>>
            # # Mainly just for TESTING with sample size (Change # to set scroll limit)
            # testWithSampleSize = 3
            # if scrollCount == testWithSampleSize: break
            ####### END #########

        else: # Invalid connection status
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


def store_tweet_data_payload(dataPayload):
    """ Function STORES list of Tweets payload extracted and collected in desired format using Selenium.
        Containing the Extracted & Collected tweet cards, write to a:
        - CSV file
        or/and
        - BINARY file
    """
    # print(os.getcwd()) # Show current dirc (Test)
    # print(os.listdir("../")) # Show files (Test)
    directoryPath = '../data_collected/twitter/'
    createdfileName = 'TwitterPayloadScraped'
    
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


# --------------------------------------------------------------- (DIVIDER) ----------------------------------------------------------------
    

####################### LOGIC ##########################
startTime = time.time() # Time Keeper
logger = setup_logger() # Logging Messages
load_dotenv() # Load environment variables from .env file

#-- Create Instance of Webdriver 
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # This IGNORES unfixable chrome web driver logs
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
#Firefox: "Firefox" | Edge: "options = EdgeOptions(); options.use_chromium = True; driver = Edge(options=options)"

#-- Gives more time to load webpage to find elements
driver.maximize_window() # Some elements only found on bigger screen resolution
driver.implicitly_wait(20) # Better Practice to use this than time.sleep() (Unlike 'time.sleep()', 'driver.implicitly_wait()' is NOT a FIXED wait time)

#-- Go to first landing page [TRAVERSING Thru Twitter]
driver.get("https://www.twitter.com/login")

#-- Login to Twitter --
username = driver.find_element("xpath", '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]') #@type="text"
username.send_keys(os.environ.get("TWITTER_USERNAME"))
username.send_keys(Keys.RETURN) #-- Same as user clicking "NEXT" Button

#-- If unusal activity confirmation page appears
try:
    userConfirmation = driver.find_element("xpath", '//input[@data-testid="ocfEnterTextTextInput"]') # User Confirmation screen
    userConfirmation.send_keys(os.environ.get("TWITTER_USER_CONFIRMATION"))
    userConfirmation.send_keys(Keys.RETURN)
except NoSuchElementException:
    logger.info("No Extra User Confirmation Needed")

driver.implicitly_wait(10) # To allow enough load time for webpage

#-- Enter PSWD Page
pswd = driver.find_element("xpath", '//input[@type="password"]')
pswd.send_keys(os.environ.get("TWITTER_PSWD")) # (SETUP to manually type into console each time due to security)
pswd.send_keys(Keys.RETURN)
driver.implicitly_wait(10) # To allow enough load time for webpage

#-- Go to search box and type keyword to search --
searchInput = driver.find_element("xpath", '//input[@data-testid="SearchBox_Search_Input"]')
searchInput.send_keys('#TSLA')  ## SEARCH TERM TODO: Select custom search query to look up?
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
store_tweet_data_payload(payloadCollected)

logger.info("--- %s Minutes ---" % ((time.time() - startTime) / 60))  # Reference for time keeping sake 

#-- CLOSE browser to save resources (Good practice)
# driver.close() # Closes focused opened browser window
driver.quit() # Close all (if any) multiple opened browser windows (Better to END program and prevent memory leak errors)
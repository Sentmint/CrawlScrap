"""
Twitter Cards Scraper Python using Selenium
NOTE:
 Overview Objective WorkFlow: 
 1. (Navigation) Log into Twitter --> Searches inputted keyword query --> Select "LATEST" tab
 2. (Collection) EXTRACTS & COLLECTS Tweet Cards seen on page --> Scrolls --> REPEAT until condition met to stop... --> STORE all Tweet Cards extracted & collected
 (Setup)
 - Forces fullscreen for best/foolproof results (Certain elements only appear with certain resolutions)
 - Uses dummy Twitter account
 (Collection)
 - Filters DURING collection of tweet cards: (view docstrings of EXTRACT and COLLECT functions)
 - Condition used to stop infinite scrolling: (If current scroll position >= total scrollable height of page) OR (scroll count) 
 - Runtime WITHOUT set scroll Count limit/condition: ~10-15 min runtime (Request overload maybe?)
 (Storing)
 - 
TODO: 
- Setup ENV variables in file for login credentials + other miscellaneous items? (Good code practice)
(Navigation)
 - With user input, dynamically setup custom navigation on Twitter?: 
    - Enter keyword for search query box (ie: '#TSLA')
    - Switch case to see various tab options to select (ie: 'Latest' tab)
(Collection)
 - DOESNT support certain elements:
    - 'tweetTextAddon' = Person referencing tweet below (Needed or useful to collect and store?)
    - Images/gifs/videos/media text (Needed or useful to collect and store?)
 - Filter further DURING collection of tweet cards? (ie: Only english?)
 - Filter further AFTER storing the extracted & collected data? (Ie: Better data handling if continue to create own file, otherwise store in DATABASE)
 - More efficient runtime? (Better handling of infinite scrolling!)
"""

import time, csv, os
from time import sleep

from selenium.webdriver import Chrome #Firefox Browser: "Firefox" | Edge Browser: "from msedge.selenium_tools import Edge, EdgeOptions"
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver import ChromeOptions 
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


####################### FUNCTIONS ##########################
def scroll_to_bottom(scrollCount):
    """ Function handles infinite scrolling: scrolls all the way to bottom of page: using Selenium
        - Includes EXTRACT and COLLECT of tweet cards shown on page
        Returns: TRUE if (bottom of page/condition) REACHED (No more tweets are loaded)
    """
    #-- SCRAPE and COLLECT all the tweets loaded on entire page using Selenium
    collect_tweet_data_payload()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll to bottom of page
    time.sleep(2) # Wait for the page to load

    print("-- Scroll Count: " + str(scrollCount) + " --")

    #TODO: EXIT FUNCTION (2 Ways with: scroll pos >= total height of page   OR   scroll counter)
    # # Get NEW scroll height
    # newScrollHeightPos = driver.execute_script("return Math.max( \
    #     document.body.scrollHeight, document.body.offsetHeight, \
    #     document.documentElement.clientHeight, \
    #     document.documentElement.scrollHeight, \
    #     document.documentElement.offsetHeight );")

    # #-- Have we reached bottom of the page? Is there no more new tweets to load?
    # if newScrollHeightPos != currentScrollHeightPos: # Update the last scroll height to set the new CURRENT Y scroll height pos
    #     currentScrollHeightPos = newScrollHeightPos  
    #     return False 
    # elif newScrollHeightPos == currentScrollHeightPos: # Bottom of the page reached if CURRENT Y scroll height pos MATCHES with NEW Y scroll height pos (No more scrolling/change in Y scroll height pos)
    #     return True
    # return newScrollHeightPos == currentScrollHeightPos #JIC failsafe

#######
    # if newScrollHeightPos == currentScrollHeightPos: # If the new scroll height is the same as the last scroll height, it means we have reached the bottom of the page
    #     break

    # # Update the last scroll height
    # currentScrollHeightPos = newScrollHeightPos
##########

    # return driver.execute_script("return {currentScrollHeightPos} >= document.body.scrollHeight;") # (Compare If current scroll position is MORE/EQUAL than the total scrollable height of the page) [DOESNT WORK??]
    #-- [OR] --
    #-- Change # of scrolls to set Limit/Condition to stop
    return scrollCount == 10


def extract_tweet_data_payload(tweet):
    """ Function EXTRACTS data details from EACH Tweet Card: using Selenium 
        - Extracts and Stores: username, twitterHandle, datePosted, replyCount, retweetCount, LikeCount, tweetText
        - Data filtering: 
            - OMIT ads/sponsors/non-users by checking for no timestamps        
        Returns: Tuple Object of specific tweet card 
    """

    username = tweet.find_element("xpath", './/span').text # Get Username  (Elements identified earlier are removed from DOM due to page refresh)
    twitterHandle = tweet.find_element("xpath", './/span[contains(text(), "@")]').text # Get Twitter Handle
    try:
        datePosted = tweet.find_element("xpath", './/time').get_attribute('datetime') # Get Timestamp string 
    except NoSuchElementException:
        print("Likely Not a User. Filter Out and Omit tweet") # If no date found, NOT a user (Ex: Ad/sponsor)
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


def collect_tweet_data_payload():
    """ Function COLLECTS list of Tweets payload extracted: using Selenium 
        Returns: Finalized list of Tuple Objects which are all the tweet cards extracted and collected
    """
    tweetCardList = driver.find_elements("xpath", '//article[@data-testid="tweet"]') # Get entire Tweet Card Payload element
    for tweet in tweetCardList: # [-15:]:  # View LAST 15 items (Removes need to recheck every tweet in list & reduces duplicates)
        data = extract_tweet_data_payload(tweet)
        if data:
            #-- Check for duplicates collected (Make our OWN tweet ID)
            tweetId = ''.join(data) # Create UNIQUE ID by concat elements of tweet into 1 string
            if tweetId not in tweetIdList:
                tweetIdList.add(tweetId)
                payloadCollected.append(data) # Original Scrapped Data
    
    print("-- Extracted and Collected Tweets Payload --")
    return payloadCollected


def store_tweet_data_payload(dataPayload):
    """ Function STORES list of Tweets payload extracted and collected in desired format: using Selenium """

    # TO CSV
    directoryPath = 'CrawlScrap/asset_scrapper/api/database/data_storage'
    createdfileName = 'TwitterPayloadScrapped.csv'
    csvFile = os.path.join(directoryPath, createdfileName)

    with open(csvFile, 'w', newline='', encoding='utf-8') as file: # Writing to file
        header = ['Username', 'Twitter Handle', 'Timestamp',
                  "Comments", "Retweets", "Likes", 'Text']
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(dataPayload)

    print("<< STORED Tweets Payload >>")


# --------------------------------------------------------------- (DIVIDER) ----------------------------------------------------------------
    

####################### LOGIC ##########################
startTime = time.time() #Time Keeper

#-- Create Instance of Webdriver 
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) # This IGNORES unfixable chrome web driver logs
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)
#Firefox: "Firefox" | Edge: "options = EdgeOptions(); options.use_chromium = True; driver = Edge(options=options)"

#-- Gives more time to load webpage to find elements
driver.maximize_window() # Some elements only found on bigger screen resolution
driver.implicitly_wait(20)

#-- Go to first landing page [TRAVERSING Thru Twitter]
driver.get("https://www.twitter.com/login")

#-- Login to Twitter --
username = driver.find_element("xpath", '//input[@class="r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu"]') #@type="text"
username.send_keys('marco_cen2001@hotmail.com')
username.send_keys(Keys.RETURN) #-- Same as user clicking "NEXT" Button

#-- If unusal activity confirmation page appears
try:
    userConfirmation = driver.find_element("xpath", '//input[@data-testid="ocfEnterTextTextInput"]') # User Confirmation screen
    userConfirmation.send_keys('ProudMC2')
    userConfirmation.send_keys(Keys.RETURN)
except NoSuchElementException:
    print("No Extra User Confirmation Needed")

sleep(1) # To allow enough load time

#-- Enter PSWD Page
pswd = driver.find_element("xpath", '//input[@type="password"]')
pswd.send_keys("Testing1") # Pswd for this acc TODO!
pswd.send_keys(Keys.RETURN)
sleep(1) # To allow enough load time

#-- Go to search box and type keyword to search --
searchInput = driver.find_element("xpath", '//input[@data-testid="SearchBox_Search_Input"]')
searchInput.send_keys('#TSLA')  ## SEARCH TERM TODO!
searchInput.send_keys(Keys.RETURN) 

#-- Pull historical data (Ex: "LATEST" tab) TODO!
driver.find_element("xpath", '//div[@class="css-901oao r-1awozwy r-14j79pv r-6koalj r-18u37iz r-37j5jr r-a023e6 r-majxgm r-1pi2tsx r-1777fci r-rjixqe r-bcqeeo r-1l7z4oj r-95jzfe r-bnwqim r-qvutc0"]').click() #Just above span tag bc cant interact with span tag





#-- Scroll to get entire PAGE of Tweets (Either bottom of the page or set limit condition reached) --
scrollCount = 0
payloadCollected = []
tweetIdList = set()
# Get CURRENT scroll height
currentScrollHeightPos = driver.execute_script("return Math.max( \
    document.body.scrollHeight, document.body.offsetHeight, \
    document.documentElement.clientHeight, \
    document.documentElement.scrollHeight, \
    document.documentElement.offsetHeight );")

while True:
    try:
        # Reached End of Page or Limit Condition Reached
        scrollCount += 1
        if scroll_to_bottom(scrollCount): # Reminder: in Python function is called here as well in condition statement!
            print("-- [All Tweets on Page LOADED in] --")            
            break # EXIT while loop 
    except:
        continue

# [Uncomment below ONLY if want to scrap stuff AFTER reach bottom of page, other than scrap as it scrolls]
# #-- SCRAPE and COLLECT all the tweets loaded on entire page using Selenium 
# payloadCollected = collect_tweet_data_payload()

#-- STORE Data Collected
store_tweet_data_payload(payloadCollected)

print("--- %s Minutes ---" % ((time.time() - startTime) / 60))  # Reference for time keeping sake 

#-- CLOSE browser to save resources (Good practice)
driver.close() 
# driver.quit() # Close Multiple Windows 












# Code Commit Msg
"""
Subject: Its ALIVE. NEW stockup LORE dropped 
- cleanup code/file structure
- alternative cleaner method: Ease of modification and readability/traceability of code
"""
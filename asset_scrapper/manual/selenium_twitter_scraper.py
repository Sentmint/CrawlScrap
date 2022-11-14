# Twitter Scraper Python using Selenium
#NOTE:
# - Uses dummy Twitter account
# - Runs UNTIL load request reached? (Due to infinite scrolling)
# - Fullscreen for best results (Certain elements only appear with certain resolutions)
# - ~10-15 min runtime
#TODO: 
# - When collect data, remove new line in TWEET TEXT for better data handling during collection?
# - More efficient runtime?
# - Dynamic 'Search Query', 'Latest' tab?
# - Dynamically setup SEARCH TERM?
# - DOESNT support 'tweetTextAddon' (Person referencing tweet below. How to store that data in database so useful?)
# - Setup ENV variables? (Replace username, pswd, etc... from file)
# - Put time limit on how long extract data?

import time, csv
from time import sleep

from selenium.webdriver import Chrome #Firefox Browser: "Firefox" | Edge Browser: "from msedge.selenium_tools import Edge, EdgeOptions"
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver import ChromeOptions 
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


startTime = time.time() #Time Keeper
#-- Function to Automate Collecting Tweet Cards List and their information --
def get_tweet_data_payload(tweet):
    """ Extract Data from each Tweet Card Payload"""
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
# sleep(1) # To allow enough load time

#-- Go to search box and type keyword to search --
searchInput = driver.find_element("xpath", '//input[@data-testid="SearchBox_Search_Input"]')
searchInput.send_keys('#TSLA')  ## SEARCH TERM TODO!
searchInput.send_keys(Keys.RETURN) 

#-- Pull historical data (Ex: "LATEST" tab) TODO!
driver.find_element("xpath", '//div[@class="css-901oao r-1awozwy r-14j79pv r-6koalj r-18u37iz r-37j5jr r-a023e6 r-majxgm r-1pi2tsx r-1777fci r-rjixqe r-bcqeeo r-1l7z4oj r-95jzfe r-bnwqim r-qvutc0"]').click() #Just above span tag bc cant interact with span tag

#-- Apply Function to ALL Cards if any data returns --
tweetDataPayloadList = []
tweetIdList = set()
lastPosOfScroll = driver.execute_script("return window.pageYOffset;") # Keep track of y position of scroll bar (Know when we reached end of pagination)
scrolling = True # Fixes pagination bug where diff y Offset of scroll pos not correctly recognized (Due to load times)

#-- Scrolling to Get New Tweet Data Loaded --
while scrolling: 

##################
    print("-- Collecting Tweet Data --")
    tweetCardList = driver.find_elements("xpath", '//article[@data-testid="tweet"]') # Get entire Tweet Card Payload element
    for tweet in tweetCardList [-15:]:  # View LAST 15 items (Removes need to recheck every tweet in list & reduces duplicates)
        data = get_tweet_data_payload(tweet)
        if data:
            #-- Check for duplicates collected (Make our OWN tweet ID)
            tweetId = ''.join(data) # Create UNIQUE ID by concat elements of tweet into 1 string
            if tweetId not in tweetIdList:
                tweetIdList.add(tweetId)
                tweetDataPayloadList.append(data) # Original Scrapped Data
##################

    scrollAttempt = 0
    while True:
        # -- Continuously scroll down page (Pagination on Twitter: unlimited scrolling)
        print("<< Scrolling Down the Page for More Tweets... >>")
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') 
        sleep(2) # To allow enough load time

        #-- Keep track of y pos of scroll bar: Handle pagination and different contents
        currPosOfScroll = driver.execute_script("return window.pageYOffset;")
        if currPosOfScroll == lastPosOfScroll:  # If same, break OUT of loop 
            scrollAttempt += 1

            #-- END scroll region
            if scrollAttempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) # Attempt to scoll again
        else:
            lastPosOfScroll = currPosOfScroll 
            break


#-- Saving Twitter Payload data collected --
# (TO CSV)
with open('pythonSeleniumTweetPayloadData.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['Username', 'Twitter Handle', 'Timestamp', "Comments", "Retweets", "Likes", 'Text']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(tweetDataPayloadList)
    print("<< COLLECTED TWEET DATA NOTED. >>")
    print("--- %s Minutes ---" % ((time.time() - startTime) / 60))

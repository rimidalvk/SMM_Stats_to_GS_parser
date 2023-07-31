import requests
import time
from connectors import google_sheets

from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# from pyvirtualdisplay import Display

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException


from utils.logger import Logger

# from pyshadow.main import Shadow


class RedditScraper:
    DEFAULT_HEADERS = {}

    DEFAULT_URL = ''  # https://www.reddit.com/r/StupidFood/comments/...
    BROWSER_EXE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    DRIVER_EXE_PATH = ""
    PROFILE_DIR_NAME = "--profile-directory=Profile 2"

    # For Mac /Users/max/Library/Application Support/Google/Chrome
    # For Windows C:\Users\User3\AppData\Local\Google\Chrome\User Data
    USER_DATA_DIR = r'--user-data-dir=C:\Users\User3\AppData\Local\Google\Chrome\User Data'

    def __int__(self):
        self.service = 'reddit'

    def get_scraping_data(self, link):
        # Need profile directory name and user data directory

        options = Options()
        # browser_executable_path=self.BROWSER_EXE_PATH,
        # use_subprocess=False,
        # driver_executable_path=self.DRIVER_EXE_PATH
        # options.add_argument(self.PROFILE_DIR_NAME)

        options.add_argument(self.USER_DATA_DIR)
        options.add_argument("--headless")

        driver = uc.Chrome(options=options)

        # "https://www.reddit.com/r/analytics/comments/14vx5yt/comment/jrjy387/?context=3"

        driver.get(link)

        '''
            Check type of the post: Personal post or Comment for the post
            profile_name = ""
            Depends on that try to locate desired elements
            For Post:

            For Comment:

        '''

        profile_name = "Competitive_Speech36"

        # Post selectors
        posted_by_selector = 'div[data-test-id="post-content"] div[data-adclicklocation="top_bar"]'
        post_selectors = ['div[data-test-id="post-content"] div[id^="vote-arrows"]',
                          'div[data-test-id="post-content"] > div:last-child > div > div:first-child']

        # Comment selectors
        comment_header_element_selector = 'div[data-testid="post-comment-header"]'
        comment_selector = 'div[class^="Comment"]'

        upvotes = 'div[id^="vote-arrows"]'
        comment_selectors = [upvotes]

        # # Check whether Post or Comment should be parsed
        try:
            post_header = driver.find_element(
                By.CSS_SELECTOR, posted_by_selector)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Post header element was not found on the page!")
            print(f"There is an error: {e}")

        try:
            # comments_group = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, comment_element_selector)))
            comments_group = driver.find_elements(
                By.CSS_SELECTOR, comment_selector)

            # Use XPath to find the element with the specific text within the group of elements
            element_xpath = f'//*[text()="{profile_name}"]'
            comment_with_text = next((element for element in comments_group if element.find_elements(
                By.XPATH, element_xpath)), None)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Comment elements were not found on the page!")
            print(f"There is an error: {e}")

        results = []
        # "/comment/" in link - is not reliable option to use
        if profile_name not in post_header.text:
            print("Comment should be scraped, Follow comment rules!")
            for selector in comment_selectors:
                print(f'Find element with selector {selector}')
                try:
                    # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    element = comment_with_text.find_element(
                        By.CSS_SELECTOR, selector)

                    # upvotes_count
                    data = int(element.text)
                    results.append(data)
                    # Can not count commnents for now

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging

                    print(f"No data for the element {selector}!")
                    results.append('no data')
        elif profile_name in post_header.text:
            print("Post should be scraped, Follow post rules!")
            for selector in post_selectors:
                print('check each element and use try and catch block')
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)

                    # votes_count
                    if post_selectors.index(selector) == 0:
                        data = int(element.text)
                        results.append(data)
                    else:
                        # comments_count
                        # reposts_count (shares) - is not used
                        data = int((element.text).split(" ")[0])
                        results.append(data)

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging

                    print(f"No data for the element {selector}!")
                    results.append(0)
        else:
            print(
                "Profile name is not found in the Post Header and in Comments! Please check the link!")
        driver.quit()
        return results

    def get_analytics_content(self, links: list = None):

        # Algorithm #
        # Open Link
        # Check the link is opened correctly

        # Get Upvotes(Likes) using this Selector: 'span[data-post-click-location="vote"] span faceplate-number'
        # Get Comments using this Selecutr: 'button[name="comments-action-button"] span span:last-of-type faceplate-number'
        # Need some other data?

        # Return Data for Upvotes, Comments
        final_results = []

        ["Datetime", "Link", "Impressions/Views/Upvotes", "Likes",
            "Number of Comments", "Number of shares/reposts"]
        # reddit_links = [x for x in links if "https://www.reddit.com/" in x]
        # print(reddit_links)

        for link in ["https://www.reddit.com/r/dataengineering/comments/144en5h/data_architecture_best_practices_how_to_build_a/?context=3", "https://www.reddit.com/r/startup_resources/comments/14914tj/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/datascience/comments/148gv5d/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/dataengineering/comments/146yzed/how_cios_approach_automation/?context=3", "https://www.reddit.com/r/DigitalMarketing/comments/14mcrn6/struggling_with_posting_blog_posts_in_linkedin/", "https://www.reddit.com/r/Entrepreneur/comments/15b4ag0/7_lesson_i_learned_as_a_solopreneur/", "https://www.reddit.com/r/ChatGPT/comments/1470xlf/how_cios_approach_automation/?context=3", "https://www.reddit.com/r/Entrepreneur/comments/148hnh7/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/learnmachinelearning/comments/14zqsio/the_next_generation_of_ai_platforms/", "https://www.reddit.com/r/Entrepreneur/comments/14yityj/comment/jrst5rz/?context=3", "https://www.reddit.com/r/dataengineering/comments/14xwkrp/comment/jrsspvs/?context=3"]:
            print("THIS IS THE LINK FOR PARSING: ", link)
            data = self.get_scraping_data(link)
            test_list = [datetime.now().strftime(
                "%m/%d/%Y %H:%M:%S"), link, "not used"]

            test_list.extend(data)
            final_results.append(test_list)

        return final_results

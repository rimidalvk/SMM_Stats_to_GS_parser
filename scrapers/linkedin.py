import requests
import time

from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# from pyvirtualdisplay import Display

import undetected_chromedriver as uc
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException


from utils.logger import Logger


class LinkedinScraper:
    DEFAULT_HEADERS = {}
    PROFILE_NAME = "Vladímir Kúbikov Smulski"
    DEFAULT_URL = ""  # https://www.linkedin.com/feed/update/urn:li:activity:
    BROWSER_EXE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    DRIVER_EXE_PATH = ""
    PROFILE_DIR_NAME = "--profile-directory=Profile 2"

    # For Mac /Users/max/Library/Application Support/Google/Chrome
    # For Windows C:\Users\User3\AppData\Local\Google\Chrome\User Data
    USER_DATA_DIR = r'--user-data-dir=C:\Users\User3\AppData\Local\Google\Chrome\User Data'

    def __int__(self):
        self.service = 'linkedin'

    def get_scraping_data(self, link):
        # Need profile directory name and user data directory

        options = Options()
        # browser_executable_path=self.BROWSER_EXE_PATH
        # use_subprocess=False
        # driver_executable_path=self.DRIVER_EXE_PATH
        # options.add_argument(self.PROFILE_DIR_NAME)

        options.add_argument(self.USER_DATA_DIR)
        options.add_argument("--headless")

        driver = uc.Chrome(options=options)
        # driver.get("https://www.linkedin.com/")

        driver.get(link)
        # "https://www.linkedin.com/feed/update/urn:li:activity:7084130557613252608/"

        # class="artdeco-modal__header - modal header
        # data-js-reaction-tab="ALL" - all reactions in  modal
        # data-js-reaction-tab="LIKE" - likes button in modal
        # data-js-reaction-tab="EMPATHY" - empathy button in modal

        '''
            Check type of the post: Personal post or Comment for the post
            profile_name = "Vladímir Kúbikov Smulski"
            Depends on that try to locate desired elements

            For post: 
            post_element = 'div[class^="feed-shared-update"] div[class*="update-components-actor--with-control-menu"]'

            For comment:
            comment_element = 'article[class^="comments-comment-item"]'  + find text  {profile_name}
        '''

        # Post selectors
        post_header_element_selector = 'div[class^="feed-shared-update"] div[class*="update-components-actor--with-control-menu"]'
        post_selectors = ['li[class*="social-details-social-counts__reactions"]',
                          'li[class*="social-details-social-counts__comments"]', 'button[aria-label*="repost"]']

        # Comment selectors #
        comment_element_selector = 'article[class^="comments-comment-item"]'

        comment_reactions_count_selector = 'div[class^="social-details-social-activity"] div[class^="comments-comment-item__social-actions"] div div:first-child button[class^="comments-comment-social-bar__reactions-count"]'
        replies_count_selector = 'div[class^="social-details-social-activity"] div[class^="comments-comment-item__social-actions"] div div:last-child span[class="comments-comment-social-bar__replies-count"]'
        comment_selectors = [
            comment_reactions_count_selector, replies_count_selector]
        # # #
        # # Check whether Post or Comment should be parsed
        # try:
        #     post_header = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #         (By.CSS_SELECTOR, post_header_element_selector)))
        # except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
        #     print(f"Post header element was not found on the page!")
        #     print(f"There is an error: {e}")

        try:
            # comments_group = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, comment_element_selector)))
            comments_group = driver.find_elements(
                By.CSS_SELECTOR, comment_element_selector)

            # Use XPath to find the element with the specific text within the group of elements
            element_xpath = f'//*[text()="{self.PROFILE_NAME}"]'
            comment_with_text = next((element for element in comments_group if element.find_elements(
                By.XPATH, element_xpath)), None)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Comment elements were not found on the page!")
            print(f"There is an error: {e}")

        # if profile_name in post_header.text:
        #     print("POST IS ON THE PAGE!")
        # elif comment_with_text:
        #     print(comment_with_text.text)

        results = []
        if "?commentUrn" in link:
            print("Comment should be scraped, Follow comment rules!")
            for selector in comment_selectors:
                print(f'Find element with selector {selector}')
                try:
                    # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    element = comment_with_text.find_element(
                        By.CSS_SELECTOR, selector)

                    if comment_selectors.index(selector) == 0:
                        # reactions_count
                        data = int(element.text)
                        results.append(data)
                    else:
                        # replies_count
                        data = int((element.text).split(" ")[0])
                        results.append(data)

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging

                    print(f"No data for the element {selector}!")
                    results.append(0)
        else:
            print("Post should be scraped, Follow post rules!")
            for selector in post_selectors:
                print(f'Find element with selector {selector}')
                try:
                    # element = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    element = driver.find_element(By.CSS_SELECTOR, selector)

                    if post_selectors.index(selector) == 0:
                        # reactions_count
                        data = int((element.text).replace(',', ''))
                        results.append(data)
                    else:
                        # comments_count / reposts_count
                        data = int((element.text).split(" ")[0])
                        results.append(data)

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging

                    print(f"No data for the element {selector}!")
                    results.append(0)

        driver.quit()
        return results

    def get_analytics_content(self, links: list = None):

        # Algorithm #
        # Open Link
        # Check the link is opened correctly
        # There is Element with this selector 'div.social-details-social-activity' visible on the page

        # Get Reactions using this Selector: 'li.social-details-social-counts__reactions'
        # Get Comments using this Selecutr: 'li.social-details-social-counts__comments'
        # Get Reposts using this Selecutr: 'ul.social-details-social-counts li:last-of-type '
        # Return Data for Likes, Comments, Reposts
        final_results = []

        ["Datetime", "Link", "Impressions/Views/Upvotes", "Likes",
            "Number of Comments", "Number of shares/reposts"]
        # linkedin_links = [x for x in links if "https://www.linkedin.com/" in x]
        # print(linkedin_links)
        # list for testing - ["https://www.linkedin.com/feed/update/urn:li:activity:7086592897440980994/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7086592897440980994%2C7086706052330586114%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287086706052330586114%2Curn%3Ali%3Aactivity%3A7086592897440980994%29", "https://www.linkedin.com/posts/vladimirks_top-10-data-sync-integration-systems-activity-7075422145861816320-Saw0/", "https://www.linkedin.com/feed/update/urn:li:ugcPost:7080593974758887424/?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7080593974758887424%2C7081640219942297601%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287081640219942297601%2Curn%3Ali%3AugcPost%3A7080593974758887424%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:37988-7090070935386435584/", "https://www.linkedin.com/feed/update/urn:li:share:7090706962111193088/", "https://www.linkedin.com/feed/update/urn:li:activity:7087174399446966273/", "https://www.linkedin.com/feed/update/urn:li:activity:7087171864300597248/", "https://www.linkedin.com/feed/update/urn:li:groupPost:99434-7089758320944717824/", "https://www.linkedin.com/feed/update/urn:li:activity:7089741686423089152/", "https://www.linkedin.com/feed/update/urn:li:groupPost:37988-7090070935386435584/", "https://www.linkedin.com/feed/update/urn:li:activity:7084420489074331648/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084420489074331648%2C7084912047955546112%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084912047955546112%2Curn%3Ali%3Aactivity%3A7084420489074331648%29", "https://www.linkedin.com/feed/update/urn:li:activity:7085217288982810624/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7085217288982810624%2C7085257880924282881%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085257880924282881%2Curn%3Ali%3Aactivity%3A7085217288982810624%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:2351870-7085150705132474369/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A2351870-7085150705132474369%2C7085261941279010816%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085261941279010816%2Curn%3Ali%3AgroupPost%3A2351870-7085150705132474369%29", "https://www.linkedin.com/feed/update/urn:li:activity:7084940087871901697/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084940087871901697%2C7085259837231501312%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085259837231501312%2Curn%3Ali%3Aactivity%3A7084940087871901697%29", "https://www.linkedin.com/feed/update/urn:li:activity:7085217288982810624/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7085217288982810624%2C7085257880924282881%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085257880924282881%2Curn%3Ali%3Aactivity%3A7085217288982810624%29", "https://www.linkedin.com/feed/update/urn:li:activity:7084420489074331648/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084420489074331648%2C7084912047955546112%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084912047955546112%2Curn%3Ali%3Aactivity%3A7084420489074331648%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:3990648-7084620562202796032/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A3990648-7084620562202796032%2C7084916178036359168%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084916178036359168%2Curn%3Ali%3AgroupPost%3A3990648-7084620562202796032%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:3990648-7084428329281323008/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A3990648-7084428329281323008%2C7084916777708584960%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084916777708584960%2Curn%3Ali%3AgroupPost%3A3990648-7084428329281323008%29", "https://www.linkedin.com/feed/update/urn:li:ugcPost:7079894316139053056/?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7079894316139053056%2C7084575472537190400%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084575472537190400%2Curn%3Ali%3AugcPost%3A7079894316139053056%29"]

        for link in links:
            print("THIS IS THE LINK FOR PARSING: ", link)
            data = self.get_scraping_data(link)
            test_list = [datetime.now().strftime(
                "%m/%d/%Y %H:%M:%S"), link, "not used"]

            test_list.extend(data)
            final_results.append(test_list)

        return final_results

import time
import json

from datetime import datetime

import undetected_chromedriver as uc

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

from utils.logger import Logger
import utils.user_config as config


class LinkedinScraper:
    # DEFAULT_HEADERS = {}
    # DEFAULT_URL = ""  # https://www.linkedin.com/feed/update/urn:li:activity:
    # BROWSER_EXE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # DRIVER_EXE_PATH = ""
    # PROFILE_DIR_NAME = "--profile-directory=Profile 2"
    LINKEDIN_PROFILE_NAME = config.linkedin_profile_name

    # For Mac /Users/max/Library/Application Support/Google/Chrome
    # For Windows C:\Users\User3\AppData\Local\Google\Chrome\User Data
    USER_CHROME_DIR = r'C:\Users\User3\AppData\Local\Google\Chrome\User Data'
    USER_DATA_DIR = f'--user-data-dir={config.user_chrome_directory}'

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
        driver.get("https://www.linkedin.com/")

        time.sleep(5)

        # Scroll and wait Random number of seconds

        driver.get(link)

        # Analytics selectors
        analytics_section_selector = '.content-analytics-entry-point a'
        metrics_elements_selector = '.member-analytics-addon__cta-list-item-text'
        impressions_selector = ' div > div'

        # Post selectors
        post_header_element_selector = 'div[class^="feed-shared-update"] div[class*="update-components-actor--with-control-menu"]'
        post_selectors = ['li[class*="social-details-social-counts__reactions"]',
                          'li[class*="social-details-social-counts__comments"]', 'button[aria-label*="repost"]']

        # Post element names mapping based on selectors
        post_element_names = {
            post_selectors[0]: "reactions", post_selectors[1]: "comments", post_selectors[2]: "reposts"}

        # Comment selectors
        comment_element_selector = 'article[class^="comments-comment-item"]'
        comment_reactions_count_selector = 'div[class^="social-details-social-activity"] div[class^="comments-comment-item__social-actions"] div div:first-child button[class^="comments-comment-social-bar__reactions-count"]'
        replies_count_selector = 'div[class^="social-details-social-activity"] div[class^="comments-comment-item__social-actions"] div div:last-child span[class="comments-comment-social-bar__replies-count"]'
        comment_selectors = [
            comment_reactions_count_selector, replies_count_selector]

        # Comment element names mapping based on selectors
        comment_element_names = {
            comment_selectors[0]: "reactions", comment_selectors[1]: "comments"}

        # # # Check if post has Analytics Section
        analytics_section = None
        try:
            analytics_section = driver.find_element(
                By.CSS_SELECTOR, analytics_section_selector)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Impressions element was not found on the page!")
            print(f"There is an error: {e}")

        # FIND COMMENTS GROUP ELEMENTS (ALL COMMNETS FOR POST)
        try:
            comments_group = driver.find_elements(
                By.CSS_SELECTOR, comment_element_selector)

            # Use XPath to find the element with the specific text within the group of elements
            element_xpath = f'//*[text()="{self.LINKEDIN_PROFILE_NAME}"]'
            comment_with_text = next((element for element in comments_group if element.find_elements(
                By.XPATH, element_xpath)), None)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Comment elements were not found on the page!")
            print(f"There is an error: {e}")

        # # # #
        # ALTERNATIVE APROACH OF CHOOSING BETWEEN POST AND COMMENT
        # # Check whether Post or Comment should be parsed
        # try:
        #     post_header = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
        #         (By.CSS_SELECTOR, post_header_element_selector)))
        # except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
        #     print(f"Post header element was not found on the page!")
        #     print(f"There is an error: {e}")

        # if profile_name in post_header.text:
        #     print("POST IS ON THE PAGE!")
        # elif comment_with_text:
        #     print(comment_with_text.text)
        # # # #

        # Dict for result data for link
        results_dict = {"impressions": 0,  "upvote_rate": 0,
                        "reactions": 0, "comments": 0, "reposts": 0}

        # There is no upvote rate for LinkeIn links
        results_dict['upvote_rate'] = 0

        # If URL is for comment --> Parse comment
        if "?commentUrn" in link:
            print("Comment should be scraped, Follow comment rules!")

            results_dict['impressions'], results_dict['reposts'] = 0, 0

            for selector in comment_selectors:
                print(f'Find {comment_element_names[selector]} element!')

                try:
                    # element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
                    element = comment_with_text.find_element(
                        By.CSS_SELECTOR, selector)
                    if comment_selectors.index(selector) == 0:
                        # reactions_count
                        data = int(element.text)
                        results_dict['reactions'] = data
                    else:
                        # replies_count
                        data = int((element.text).split(" ")[0])
                        results_dict['comments'] = data

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging

                    print(
                        f"No data for the element {comment_element_names[selector]}!")

                    # Add 0 for the data
                    results_dict[comment_element_names[selector]] == 0

        # If URL is not for comment --> Parse Post
        else:
            print("Post should be scraped, Follow the Post rules!")
            # If Anaytics Section exists for the post --> Go to Analytics Page and get data

            if analytics_section:
                # .is_displayed()
                print("Work with post's Analytics Section!")

                impressions_element = analytics_section.find_element(
                    By.CSS_SELECTOR, impressions_selector)

                # Add Impressions count
                results_dict["impressions"] = int(
                    (impressions_element.text).split(' ')[0])

                time.sleep(3)  # wait before click to Analytics Page

                analytics_section.click()  # click on the element
                time.sleep(3)  # wait for page loads

                # Find elements on Analytics Page
                try:
                    metrics_elements = driver.find_elements(
                        By.CSS_SELECTOR, metrics_elements_selector)

                    # Add  reactions_count / comments_count / reposts_count
                    results_dict["reactions"] = int(metrics_elements[0].text)
                    results_dict["comments"] = int(metrics_elements[1].text)
                    results_dict["reposts"] = int(metrics_elements[2].text)

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"Metrics elements were not found on the page!")
                    print(f"There is an error: {e}")

            # If No Analytics Page exists get data for post from current page
            else:
                # CHECK IF THIS CASE NEED FOR HANDLE:  WHEN REACTIONS IS PERSONS' NAME AND NUMBER
                print("Work with post's elements on the page!")

                # Add 0 for Impressions
                results_dict['impressions'] = 0

                for selector in post_selectors:
                    print(
                        f"Find post's {post_element_names[selector]} element!")
                    try:
                        element = driver.find_element(
                            By.CSS_SELECTOR, selector)

                        if post_selectors.index(selector) == 0:
                            # Add reactions_count
                            data = int((element.text).replace(',', ''))
                            results_dict["reactions"] = data
                        elif post_selectors.index(selector) == 1:
                            # Add comments_count
                            data = int((element.text).split(" ")[0])
                            results_dict["comments"] = data
                        else:
                            # reposts_count
                            data = int((element.text).split(" ")[0])
                            results_dict["reposts"] = data

                    except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                        print(f"There is an error: {e}")
                        # Save the error for logging

                        print(
                            f"No data for the post's {post_element_names[selector]} element!")
                        results_dict[post_element_names[selector]] == 0

        driver.quit()
        return results_dict

    def get_analytics_content(self, links: list):
        # list = None - was removed temporarily
        # Algorithm #

        # Final Result list with data for each link
        final_results = []

        # linkedin_links = [x for x in links if "https://www.linkedin.com/" in x]
        # print(linkedin_links)
        test_linkedin_links = ["https://www.linkedin.com/feed/update/urn:li:activity:7086592897440980994/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7086592897440980994%2C7086706052330586114%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287086706052330586114%2Curn%3Ali%3Aactivity%3A7086592897440980994%29", "https://www.linkedin.com/posts/vladimirks_top-10-data-sync-integration-systems-activity-7075422145861816320-Saw0/", "https://www.linkedin.com/feed/update/urn:li:ugcPost:7080593974758887424/?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7080593974758887424%2C7081640219942297601%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287081640219942297601%2Curn%3Ali%3AugcPost%3A7080593974758887424%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:37988-7090070935386435584/", "https://www.linkedin.com/feed/update/urn:li:share:7090706962111193088/", "https://www.linkedin.com/feed/update/urn:li:activity:7087174399446966273/", "https://www.linkedin.com/feed/update/urn:li:activity:7087171864300597248/", "https://www.linkedin.com/feed/update/urn:li:groupPost:99434-7089758320944717824/", "https://www.linkedin.com/feed/update/urn:li:activity:7089741686423089152/", "https://www.linkedin.com/feed/update/urn:li:groupPost:37988-7090070935386435584/", "https://www.linkedin.com/feed/update/urn:li:activity:7084420489074331648/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084420489074331648%2C7084912047955546112%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084912047955546112%2Curn%3Ali%3Aactivity%3A7084420489074331648%29", "https://www.linkedin.com/feed/update/urn:li:activity:7085217288982810624/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7085217288982810624%2C7085257880924282881%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085257880924282881%2Curn%3Ali%3Aactivity%3A7085217288982810624%29",
                               "https://www.linkedin.com/feed/update/urn:li:groupPost:2351870-7085150705132474369/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A2351870-7085150705132474369%2C7085261941279010816%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085261941279010816%2Curn%3Ali%3AgroupPost%3A2351870-7085150705132474369%29", "https://www.linkedin.com/feed/update/urn:li:activity:7084940087871901697/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084940087871901697%2C7085259837231501312%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085259837231501312%2Curn%3Ali%3Aactivity%3A7084940087871901697%29", "https://www.linkedin.com/feed/update/urn:li:activity:7085217288982810624/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7085217288982810624%2C7085257880924282881%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287085257880924282881%2Curn%3Ali%3Aactivity%3A7085217288982810624%29", "https://www.linkedin.com/feed/update/urn:li:activity:7084420489074331648/?commentUrn=urn%3Ali%3Acomment%3A%28activity%3A7084420489074331648%2C7084912047955546112%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084912047955546112%2Curn%3Ali%3Aactivity%3A7084420489074331648%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:3990648-7084620562202796032/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A3990648-7084620562202796032%2C7084916178036359168%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084916178036359168%2Curn%3Ali%3AgroupPost%3A3990648-7084620562202796032%29", "https://www.linkedin.com/feed/update/urn:li:groupPost:3990648-7084428329281323008/?commentUrn=urn%3Ali%3Acomment%3A%28groupPost%3A3990648-7084428329281323008%2C7084916777708584960%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084916777708584960%2Curn%3Ali%3AgroupPost%3A3990648-7084428329281323008%29", "https://www.linkedin.com/feed/update/urn:li:ugcPost:7079894316139053056/?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7079894316139053056%2C7084575472537190400%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287084575472537190400%2Curn%3Ali%3AugcPost%3A7079894316139053056%29"]

        for link in links:
            print("THIS IS THE LINK FOR PARSING: ", link)
            data = self.get_scraping_data(link)

            # Declare dict with results
            data_dict = {"datetime": datetime.now().strftime(
                "%m/%d/%Y %H:%M:%S"), "link": link}
            # Add scraped data to dict
            data_dict.update(data)

            # Updata dict with JSON data
            data_dict.update({"json": json.dumps(data)})
            print('THIS IS DATA IN DICT: ', data_dict)

            final_results.append(data_dict)
            print('--------------------------------------------------------')

        return final_results

import json

from datetime import datetime
# from pyvirtualdisplay import Displayxw

import undetected_chromedriver as uc

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

from utils.logger import Logger
import utils.user_config as config


class RedditScraper:
    # DEFAULT_HEADERS = {}
    # DEFAULT_URL = ''  # https://www.reddit.com/r/StupidFood/comments/...
    # BROWSER_EXE_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    # DRIVER_EXE_PATH = ""
    # PROFILE_DIR_NAME = "--profile-directory=Profile 2"
    REDDIT_PROFILE_NAME = config.reddit_profile_name

    # For Mac /Users/max/Library/Application Support/Google/Chrome
    # For Windows C:\Users\User3\AppData\Local\Google\Chrome\User Data
    # USER_CHROME_DIR = r'C:\Users\User3\AppData\Local\Google\Chrome\User Data'
    USER_DATA_DIR = f'--user-data-dir={config.user_chrome_directory}'

    def __int__(self):
        self.service = 'reddit'

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
        # driver.get("https://www.reddit.com/")

        # Scroll and wait Random number of seconds

        driver.get(link)

        # Post selectors
        posted_by_selector = 'div[data-test-id="post-content"] div[data-adclicklocation="top_bar"]'
        post_selectors = ['div[data-test-id="post-content"] div[id^="vote-arrows"]',
                          'div[data-test-id="post-content"] > div:last-child > div > div:first-child']
        upvote_rate_number_selector = 'div[data-test-id="post-content"] div[id^="vote-arrows"] > div'
        upvote_rate_selector = upvote_rate_number_selector + ' > div'
        analytics_section_selector = ''
        post_container_element = 'div[data-testid="post-container"]'

        # Post Element names mapping based on selectors
        post_element_names = {
            post_selectors[0]: "reactions", post_selectors[1]: "comments"}

        # Comment selectors
        comment_header_element_selector = 'div[data-testid="post-comment-header"]'
        comment_selector = 'div[class^="Comment"]'

        upvotes = 'div[id^="vote-arrows"]'
        comment_selectors = [upvotes]

        # # Check whether Post or Comment should be parsed

        # Find Post Header
        try:
            # post_header = driver.find_element(By.CSS_SELECTOR, posted_by_selector)
            post_header = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, posted_by_selector)))
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Post header element was not found on the page!")
            print(f"There is an error: {e}")

        # POSTS #
        # # # Check if post has Analytics Section
        analytics_section_element = None
        try:
            # Find the parent element using the specified CSS selector
            # child_element = driver.find_element(By.CSS_SELECTOR, post_container_element)
            child_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, post_container_element)))

            # Get parent of child element
            parent_element = child_element.find_element(By.XPATH, '..')

            # # Find Analytics Section
            children = parent_element.find_elements(By.XPATH, '*')
            analytics_section_element = children[1].find_elements(
                By.XPATH, '*')[1]

        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Impressions element was not found on the page!")
            print(f"There is an error: {e}")

        # COMMMENTS #
        # Find comment with Profile Name
        try:
            # comments_group = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, comment_selector)))
            comments_group = driver.find_elements(
                By.CSS_SELECTOR, comment_selector)

            # Use XPath to find the element with the specific text within the group of elements
            element_xpath = f'//*[text()="{self.REDDIT_PROFILE_NAME}"]'
            comment_with_text = next((element for element in comments_group if element.find_elements(
                By.XPATH, element_xpath)), None)
        except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
            print(f"Comment elements were not found on the page!")
            print(f"There is an error: {e}")

        # Dict for result data for link
        results_dict = {"impressions": 0,  "upvote_rate": 0,
                        "reactions": 0, "comments": 0, "reposts": 0}

        # "/comment/" in link - is not reliable option to use

        # If Profile Name IS NOT in Post Header --> Follow the Comment Scraping rules
        if self.REDDIT_PROFILE_NAME not in post_header.text:
            print("This is the comment, so comment scraping rules are applied!")

            # For Impressions and Upvotes Rate
            results_dict['impressions'], results_dict['upvote_rate'] = 0, 0

            for selector in comment_selectors:
                print(f'Find element with selector {selector}')
                try:
                    element = comment_with_text.find_element(
                        By.CSS_SELECTOR, selector)

                    # reactions count (upvotes)
                    data = int(element.text)
                    results_dict['reactions'] = data

                    # UPDATE: NEED TO COUNT COMMENT (not possible for now)
                    results_dict['comments'] = 0

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging
                    print(f"No data for the element {selector}!")
                    results_dict['reactions'] = 0

            # No reposts for comments
            results_dict['reposts'] = 0

        # If Profile Name is in Post Header --> Follow the Post Scraping rules
        elif self.REDDIT_PROFILE_NAME in post_header.text:
            print("This is the post, so post scraping rules are applied!")

            if analytics_section_element:
                if "Total Views" in analytics_section_element.text:
                    print("Analytics Section is Visible")

                    analytics_section_child_ellements = analytics_section_element.find_elements(
                        By.XPATH, '*')

                    total_views = analytics_section_child_ellements[0].text.split("\n")[
                        0]
                    upvote_rate = analytics_section_child_ellements[1].text.split("\n")[
                        0]
                    total_shares = int(
                        analytics_section_child_ellements[3].text.split("\n")[0])

                    results_dict['impressions'], results_dict['upvote_rate'], results_dict['reposts'] = total_views, upvote_rate, total_shares

                else:
                    # Impressions and Upvotes Rate are 0
                    results_dict['impressions'], results_dict['reposts'] = 0, 0

                    # Get upvote rate from the hover element
                    print("Get Upvote Rate from the hover element")
                    try:
                        actions = ActionChains(driver)
                        upvote_rate_number_element = driver.find_element(
                            By.CSS_SELECTOR, upvote_rate_number_selector)

                        hover = actions.move_to_element(
                            upvote_rate_number_element)
                        hover.perform()
                        upvote_rate_element = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, upvote_rate_selector)))

                        print(upvote_rate_element.text)
                        results_dict['upvote_rate'] = (
                            upvote_rate_element.text).split(" ")[0]
                    except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                        print(
                            f"Upvote Rate percent element was not found on the page!")
                        print(f"There is an error: {e}")

            for selector in post_selectors:
                print('check each element and use try and catch block')
                try:
                    element = driver.find_element(
                        By.CSS_SELECTOR, selector)

                    # votes_count (reactions)
                    if post_selectors.index(selector) == 0:
                        data = int(element.text)
                        results_dict["reactions"] = data

                    else:
                        # comments_count
                        data = int((element.text).split(" ")[0])
                        results_dict["comments"] = data

                except (NoSuchElementException, Exception, WebDriverException, TimeoutException) as e:
                    print(f"There is an error: {e}")
                    # Save the error for logging
                    print(
                        f"No data for the element {post_element_names[selector]}!")
                    results_dict[post_element_names[selector]] = 0

        else:
            print(
                "Profile name is not found in the Post Header and in Comments! Please check the link!")
        driver.quit()
        return results_dict

    def get_analytics_content(self, links: list):
        # list = None - was removed temporarily
        # Algorithm #

        # Final Result list with data for each link
        final_results = []

        # reddit_links = [x for x in links if "https://www.reddit.com/" in x]
        test_reddit_links = ["https://www.reddit.com/r/dataengineering/comments/144en5h/data_architecture_best_practices_how_to_build_a/?context=3", "https://www.reddit.com/r/startup_resources/comments/14914tj/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/datascience/comments/148gv5d/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/dataengineering/comments/146yzed/how_cios_approach_automation/?context=3", "https://www.reddit.com/r/DigitalMarketing/comments/14mcrn6/struggling_with_posting_blog_posts_in_linkedin/", "https://www.reddit.com/r/Entrepreneur/comments/15b4ag0/7_lesson_i_learned_as_a_solopreneur/", "https://www.reddit.com/r/ChatGPT/comments/1470xlf/how_cios_approach_automation/?context=3", "https://www.reddit.com/r/Entrepreneur/comments/148hnh7/data_management_challenges_in_ma/?context=3", "https://www.reddit.com/r/learnmachinelearning/comments/14zqsio/the_next_generation_of_ai_platforms/", "https://www.reddit.com/r/Entrepreneur/comments/14yityj/comment/jrst5rz/?context=3", "https://www.reddit.com/r/dataengineering/comments/14xwkrp/comment/jrsspvs/?context=3",
                             "https://www.reddit.com/r/exchangeserver/comments/14zrsb8/the_next_generation_of_ai_platforms/", "https://www.reddit.com/r/learnmachinelearning/comments/14zqsio/the_next_generation_of_ai_platforms/", "https://www.reddit.com/r/startup_resources/comments/14wmhlx/comment/jsbd5si/?context=3", "https://www.reddit.com/r/dataengineering/comments/1539422/data_management_challenges_in_ma/?sort=new", "https://www.reddit.com/r/ITManagers/comments/153a3bx/data_management_challenges_in_ma/", "https://www.reddit.com/r/productivity/comments/158c049/comment/jt993sp/?context=3", "https://www.reddit.com/r/BusinessIntelligence/comments/15gfv8d/are_ai_agents_the_future_of_content_writing/ ", "https://www.reddit.com/r/dataengineering/comments/15g63rd/comment/jugv0ff/?context=3", "https://www.reddit.com/r/dataengineering/comments/15gi2tr/are_ai_agents_the_future_of_content_writing/", "https://www.reddit.com/r/Entrepreneur/comments/14lmfra/how_to_approach_tearing_down_monoliths_in_favor/", "https://www.reddit.com/r/dataengineering/comments/144en5h/data_architecture_best_practices_how_to_build_a/?utm_source=share&utm_medium=web2x&context=3"]

        for link in links:
            print("THIS IS THE LINK FOR PARSING: ", link)
            # Get Parsed Data
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

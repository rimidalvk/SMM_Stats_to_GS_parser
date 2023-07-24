import requests
import time

from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
# from pyvirtualdisplay import Display

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import Logger


class LinkedinScraper:
    DEFAULT_HEADERS = {

    }
    DEFAULT_URL = ''

    # https://www.linkedin.com/feed/update/urn:li:activity:

    def __int__(self):
        self.service = 'linkedin'

    def login_linkedin_selenium(self):
        # Need profile directory name
        profile_dir_name = '--profile-directory=Profile 2'
        user_data_dir = '--user-data-dir=/Users/max/Library/Application Support/Google/Chrome'
        exe_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        # Need user data directory
        options = Options()
        options.add_argument(profile_dir_name)
        options.add_argument(user_data_dir)
        driver = uc.Chrome(executable_path=exe_path, options=options)
        driver.get("https://www.linkedin.com/")

        time.sleep(5)
        driver.get(
            "https://www.linkedin.com/feed/update/urn:li:activity:7084130557613252608/")
        # https://www.linkedin.com/feed/update/urn:li:activity:7072270080629194752/

        # ul class="social-details-social-counts
        # li class*=social-details-social-counts__reactions]
        # li [class*=social-details-social-counts__comments]
        # class="social-details-social-counts__item - reposts

        # class="artdeco-modal__header - modal header
        # data-js-reaction-tab="ALL" - all reactions in  modal
        # data-js-reaction-tab="LIKE" - likes button in modal
        # data-js-reaction-tab="EMPATHY" - empathy button in modal

        reactions_count_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'li[class*="social-details-social-counts__reactions"]')))
        print(reactions_count_element)

        try:
            # Wait until the reactions, comments, and reposts elements are loaded.
            reactions_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[class*="social-details-social-counts__reactions"]'))
            )

            comments_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[class*="social-details-social-counts__comments"]'))
            )

            reposts_count_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[class^="social-details-social-counts__item"]:last-child'))
            )

            # Get the counts of reactions, comments, and reposts.
            reactions_count = int(reactions_count_element.text.split()[0])
            comments_count = int(comments_count_element.text.split()[0])
            reposts_count = int(reposts_count_element.text.split()[0])

            # Output the results.
            print(f"Reactions: {reactions_count}")
            print(f"Comments: {comments_count}")
            print(f"Reposts: {reposts_count}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            driver.quit()

    def login_linkedin_playwright(self, email, password):
        with sync_playwright() as p:
            # args=["--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"]
            # args=['--profile-directory=Profile 2']
            user_data_dir = '/Users/max/Library/Application Support/Google/Chrome'
            exe_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            browser_type = p.chromium

            browser = browser_type.launch_persistent_context(headless=False,
                                                             executable_path=exe_path, user_data_dir=user_data_dir, args=['--profile-directory=Profile 2', "--disable-blink-features=AutomationControlled", "--disable-dev-shm-usage"])

            # context = browser.new_context()
            page = browser.new_page()
            page.goto("https://www.linkedin.com/")

            # page.fill('input[name="session_key"]', email)
            # page.fill('input[name="session_password"]', password)
            # page.click('button[type="submit"]')

            time.sleep(20)
            # You can add some delay here or use wait functions to ensure the login is complete before proceeding further
            # For example, you can use `page.wait_for_timeout(timeout)` to add some delay.

            # Check if the login was successful
            if "feed" in page.url:
                print("Login successful.")
                # Add your code to perform actions after successful login here.
            else:
                print("Login failed.")

            # Don't forget to close the browser when done.
            browser.close()

    def run_check(self):
        # self.login_linkedin_playwright(email, password)
        self.login_linkedin_selenium()

    def get_analytics_content(self, links: list = None):

        # Algorithm #
        # Open Link
        # Check the link is opened correctly
        # There is Element with this selector 'div.social-details-social-activity' visible on the page

        # Get Reactions using this Selector: 'li.social-details-social-counts__reactions'
        # Get Comments using this Selecutr: 'li.social-details-social-counts__comments'
        # Get Reposts using this Selecutr: 'ul.social-details-social-counts li:last-of-type '

        # Return Data for Likes, Comments, Reposts
        return

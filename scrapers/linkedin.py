import requests
import time

from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
#from pyvirtualdisplay import Display

from utils.logger import Logger


class LinkedinScraper:
    DEFAULT_HEADERS = {

    }
    DEFAULT_URL = ''

    # https://www.linkedin.com/feed/update/urn:li:activity:

    def __int__(self):
        self.service = 'linkedin'

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

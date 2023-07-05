import requests
import time

from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
#from pyvirtualdisplay import Display

from utils.logger import Logger


class RedditScraper:
    DEFAULT_HEADERS = {

    }
    DEFAULT_URL = ''

    #  https://www.reddit.com/r/StupidFood/comments/...


    def __int__(self):
        self.service = 'reddit'

    def get_analytics_content(self, links: list = None):

        # Algorithm #
        # Open Link 
        # Check the link is opened correctly

        # Get Upvotes(Likes) using this Selector: 'span[data-post-click-location="vote"] span faceplate-number'
        # Get Comments using this Selecutr: 'button[name="comments-action-button"] span span:last-of-type faceplate-number'
        # Need some other data?
        
        # Return Data for Likes, Comments
        return

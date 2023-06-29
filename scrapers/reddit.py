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

    def __int__(self):
        self.service = 'reddit'

    def get_analytics_content(self, links: list = None):
        return

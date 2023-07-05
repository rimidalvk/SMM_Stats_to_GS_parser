import time
import threading

from scrapers import linkedin, reddit
from connectors import google_sheets
from utils.logger import Logger

from config import link_table


# Sart Parsing LinkedIn Posts
def start_parse_linkedin(linkedin, google, linkedin_links):
    Logger.get_log('Собираем статистику по linkedin')

    content = linkedin.get_analytics_content(linkedin_links)
    google.add_result_analytics(content, link_table)

# Sart Parsing Reddit Posts
def start_parse_reddit(reddit, google, reddit_links):
    Logger.get_log('Собираем статистику по reddit')

    content = reddit.get_analytics_content(reddit_links)
    google.add_result_analytics(content, )

if __name__ == '__main__':
    Logger.get_log('Начали сбор информации')

    # Declare parameters for threads
    google_sheet = google_sheets.GoogleSheet()
    linkedin_posts = linkedin.LinkedinScraper()
    reddit_posts = reddit.RedditScraper()

    Logger.get_log('Получаем ссылки с таблицы')

    # Get Links for Parsing
    links_post = google_sheet.get_links_post(link_table)

    # Run process in Threads for faster completetion
    t1 = threading.Thread(target=start_parse_linkedin, args=(linkedin_posts, google_sheet, links_post['linkedin_links'],))
    t2 = threading.Thread(target=start_parse_reddit, args=(reddit_posts, google_sheet, links_post['reddit_links'],))

    t1.start()
    t2.start()

    # Finish threads
    t1.join()
    t2.join()

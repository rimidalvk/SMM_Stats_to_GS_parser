import time
import threading

from scrapers import linkedin, reddit
from connectors import google_sheets
from utils.logger import Logger

from utils.config import table_id


# Start Parsing LinkedIn Posts
def start_parse_linkedin(linkedin, google, linkedin_links):
    Logger.get_log('Собираем статистику по linkedin')

    content = linkedin.get_analytics_content(linkedin_links)
    google.add_result_analytics(content, table_id)

# Start Parsing Reddit Posts


def start_parse_reddit(reddit, google, reddit_links):
    Logger.get_log('Собираем статистику по reddit')

    content = reddit.get_analytics_content(reddit_links)
    google.add_result_analytics(content, table_id)


if __name__ == '__main__':
    Logger.get_log('Начали сбор информации')

    # Declare parameters for threads for Google Sheets and different types of posts
    google_sheet = google_sheets.GoogleSheet()
    linkedin_posts = linkedin.LinkedinScraper()
    reddit_posts = reddit.RedditScraper()

    Logger.get_log('Получаем ссылки с таблицы')

    # PRINT DATA
    # TESTING
    # print(google_sheet.get_all_links_from_sheet())
    # print(google_sheet.get_configuration_data())
    # google_sheet.filter_posts()
    linkedin_posts.run_check()
    #

    # Get Links for Parsing
    links_post = google_sheet.get_links_post(table_id)

    # Run process in Threads for faster completetion for different Link types
    t1 = threading.Thread(target=start_parse_linkedin, args=(
        linkedin_posts, google_sheet, links_post))
    # links_post['linkedin_links']
    t2 = threading.Thread(target=start_parse_reddit, args=(
        reddit_posts, google_sheet, links_post))
    # links_post['reddit_links'

    t1.start()
    t2.start()

    # Finish threads
    t1.join()
    t2.join()

import time
import threading

from scrapers import linkedin, reddit
from connectors import google_sheets
from utils.logger import Logger

from config import link_table


def start_parse_linkedin(linkedin, google, linkedin_links):
    Logger.get_log('Собираем статистику по linkedin')

    content = linkedin.get_analytics_content(linkedin_links)
    google.add_result_analytics(content)


def start_parse_reddit(reddit, google, reddit_links):
    Logger.get_log('Собираем статистику по reddit')

    content = reddit.get_analytics_content(reddit_links)
    google.add_result_analytics(content)


if __name__ == '__main__':
    Logger.get_log('Начали сбор информации')

    google = google_sheets.GoogleSheet()
    linkedin = linkedin.LinkedinScraper()
    reddit = reddit.RedditScraper()

    Logger.get_log('Получаем ссылки с таблицы')
    links_post = google.get_links_post(link_table)

    t1 = threading.Thread(target=start_parse_linkedin, args=(linkedin, google, links_post['linkedin_links'],))
    t2 = threading.Thread(target=start_parse_reddit, args=(reddit, google, links_post['reddit_links'],))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

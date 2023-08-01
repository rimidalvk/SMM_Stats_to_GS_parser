import time
from datetime import datetime
import threading

from scrapers import linkedin, reddit
from connectors import google_sheets
from utils.logger import Logger

from utils.config import table_id


# Start Parsing LinkedIn Posts
def start_parse_linkedin(linkedin, google, linkedin_links):
    Logger.get_log('Собираем статистику по linkedin')

    # Filter links only if link contains base URL
    linkedin_links_upd = [
        x for x in linkedin_links if "https://www.linkedin.com/" in x]

    # Store data for loging: LinkedIn Posts and Comments
    google_sheet.store_data("Linkedin links", len(linkedin_links_upd))
    google_sheet.store_data("Linkedin posts", len(
        [item for item in linkedin_links_upd if "?commentUrn" not in item]))
    google_sheet.store_data("Linkedin comments", len(
        [item for item in linkedin_links_upd if "?commentUrn" in item]))

    content = linkedin.get_analytics_content(linkedin_links_upd)
    google.add_result_analytics(content)  # table_id


# Start Parsing Reddit Posts
def start_parse_reddit(reddit, google, reddit_links):
    Logger.get_log('Собираем статистику по reddit')

    reddit_links_upd = [
        x for x in reddit_links if "https://www.reddit.com/" in x]

    # Store data for loging
    google_sheet.store_data("Reddit links", len(reddit_links_upd))
    google_sheet.store_data("Reddit posts", len(
        [item for item in reddit_links_upd if "/comment/" not in item]))
    google_sheet.store_data("Reddit comments", len(
        [item for item in reddit_links_upd if "/comment/" in item]))

    content = reddit.get_analytics_content(reddit_links_upd)
    google.add_result_analytics(content)  # table_id


if __name__ == '__main__':

    Logger.get_log('Начали сбор информации')
    # Declare parameters for threads for Google Sheets and different types of posts
    google_sheet = google_sheets.GoogleSheet()
    linkedin_posts = linkedin.LinkedinScraper()
    reddit_posts = reddit.RedditScraper()

    # Start the script - get the log data
    google_sheet.store_data(
        "Cycle start", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

    Logger.get_log('Получаем ссылки с таблицы')

    # PRINT DATA
    # TESTING
    # print(google_sheet.get_all_links_from_sheet())
    # print(google_sheet.get_configuration_data())
    # google_sheet.filter_posts()
    # linkedin_posts.get_scraping_data("https://www.linkedin.com/feed/update/urn:li:ugcPost:7080593974758887424/?commentUrn=urn%3Ali%3Acomment%3A%28ugcPost%3A7080593974758887424%2C7081640219942297601%29&dashCommentUrn=urn%3Ali%3Afsd_comment%3A%287081640219942297601%2Curn%3Ali%3AugcPost%3A7080593974758887424%29")
    # reddit_posts.get_scraping_data()
    #

    # Get Links for Parsing
    links_post = google_sheet.get_links_post()  # table_id

    # Run process in Threads for faster completetion for different Link types
    t1 = threading.Thread(target=start_parse_linkedin, args=(
        linkedin_posts, google_sheet, links_post))
    # links_post['linkedin_links']
    t2 = threading.Thread(target=start_parse_reddit, args=(
        reddit_posts, google_sheet, links_post))
    # links_post['reddit_links']

    # Start threads
    t1.start()
    t1.join()

    # Finish threads
    t2.start()
    t2.join()

    # End script run - save the log data
    google_sheet.store_data(
        "Cycle end", datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

    # Save to Google Sheets all log data about script run
    google_sheet.add_scraper_run_result()
    print("Scraping is finished")

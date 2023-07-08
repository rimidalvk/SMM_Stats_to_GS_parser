import requests
import gspread
import config
from google.oauth2.service_account import Credentials


from utils.logger import Logger


class GoogleSheet:
    def __int__(self):
        self.service = 'google_sheets'

    # Function the Authorizes and connects to Google Sheets
    def connect_to_the_sheeet(link_table):
        # Path to the service account JSON file
        service_account_file = config.link_table

        # ID of the Google Sheet
        spreadsheet_id = link_table

        # Create credentials using the service account file
        credentials = Credentials.from_service_account_file(
            service_account_file)
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/spreadsheets'])

        # Authenticate using the scoped credentials
        client = gspread.authorize(scoped_credentials)

        # Open the Google Sheet
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Output Google Sheet Object
        return spreadsheet

    # Main function that provides final links for parsing
    def get_links_post(self, connect_to_the_sheeet):

        # Get the resulting lists of link for Main Action
        result_links = self.filter_posts(
            self.get_all_links_from_sheet, self.get_configuration_data)
        return result_links

    def get_all_links_from_sheet(connect_to_the_sheeet):
        # Fetch posts links from Google Sheets

        all_links_data = []
        # Output the the combination of Link and Time of Publication
        return all_links_data

    def filter_posts(links, config_data):
        # Input Links_data and Config_data

        # # Detailed Algorithm # #
        '''
        Sort the posts for the last 10 days? - Move this setting to the Config File?
        Filter data basing on the Config Data and Current Date (Calculate the difference)

        CONFIGURATION FORMAT SHOULD BE DEFINED IN ADVANCE!
        IT SHOULD BE MODIFIABLE IN THE GOOGLE SHEETS WITH THE APPROPRIATE VALUES!

        # Rule example:
        During 24 hours  ---> check posts each 60 mintes
        Between 24 - 48 hours  ---> check posts each 120 mintes
        Between 48 - 72 hours  ---> check posts each 180 mintes
        Between 72 - 96 hours  ---> check posts each 1440 mintes
        Between 96 - 120 hours  ---> check posts each 1440 mintes
        And so on...

        The configuration rules are separated for a few layers:
        1. Get Post for scraping
        2. Get Likes/Upvotes from the Post
        2. Get Comments from the Post
        3. Get Reposts/Shares from the Post 

        '''

        # Data structure for Links Data
        links_data = [{'link': 'https://www.linkedin.com/feed/update/urn:li:activity:...', 'link_type': 'linkedin', 'date': '05.07.2023'},
                      {'link': 'https://www.reddit.com/r/therewasanattempt/comments/...', 'link_type': 'reddit', 'date': '04.07.2023'}]
        links_data = [['https://www.linkedin.com/feed/update/urn:li:activity:', '05.07.2023'],
                      ['https://www.reddit.com/r/therewasanattempt/comments/...', '04.07.2023']]

        # Output final Links Data for scraping
        final_links_result = []
        return final_links_result

    def get_configuration_data(connect_to_the_sheeet):
        # Read Config Table in Google Sheets

        # Output the Config Data
        config_data = []
        return config_data

    def add_result_analytics(self, info, connect_to_the_sheeet):
        # Get Tab in the Google Sheet by name
        # Get the Content Info from parsing

        # Write the info into the Google Shet row
        print("Data has been added")

    def log_srapper_run(self):
        # Saving errors for each process (functions) that can meet some problems

        # Errors for Reading from the Google Sheets
        # Errors for Writing to the Google Sheet
        # Errors Scraping Data
        # Errors for data manipulation

        log_data = []
        print("Logs has been saved")
        return log_data

    def add_srapper_run_result(self, connect_to_the_sheeet):
        # Get Tab in the Google Sheet by name
        ''' Save the following data:
            - Start Time of the Scrapper Cycle
            - End Time of the Scrapper Cycle
            - Number of Links processed
            - Errors & comments (will be saved into the separte txt file)
            - LinkedIn Posts processes
            - LinkedIn Comments in total ?
            - Reddit Posts precessed
            - Reddit Comments in total ?
        '''

        # Errors that can be found during the script run
        errors = self.log_srapper_run()

        # Comments depeneding on the type of error
        comments = ''

        # Write the above logging info into the row
        '''
            Need to consider loging approach
            Could be the text file that contains all logs and saved in the repository or HTML report.
        '''
        print("Data has been added")

import requests
import gspread
from gspread import utils
import utils.config as config
from google.oauth2.service_account import Credentials
from datetime import datetime

from utils.logger import Logger


class GoogleSheet:
    def __int__(self):
        self.service = 'google_sheets'

    # Function the Authorizes and connects to Google Sheets
    def connect_to_the_sheeet(self):
        # Path to the service account JSON file
        service_account_file = config.service_account_credentials

        # ID of the Google Sheet
        spreadsheet_id = config.table_id

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
        # result_links = self.filter_posts(self.get_all_links_from_sheet, self.get_configuration_data)
        return ""

    def get_all_links_from_sheet(self):
        # Fetch posts links from Google Sheets

        worksheet = self.connect_to_the_sheeet().worksheet("SMM Journal")

        # Reading all column values for "M" and "Q" columns
        values_links_list = worksheet.col_values(
            utils.column_letter_to_index("M"))
        values_dates_list = worksheet.col_values(
            utils.column_letter_to_index("Q"))

        '''
            Iteration approach of getting data from GSheet - Doesn't work and Above the limit

            values_time_list = []
            for link in values_links_list:
                if values_links_list.index(link) >= 2:
                    value = worksheet.acell(
                        'Q' + f'{values_links_list.index(link)}').value
                    values_time_list.append(value)
        '''

        all_links = values_links_list[2:]
        all_publication_times = values_dates_list[2:]

        combined_list = list(zip(all_links, all_publication_times))

        # Output the the combination of Link and Time of Publication
        return combined_list

    def filter_posts(self):
        # Input Links_data and Config_data

        links_data = self.get_all_links_from_sheet()

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

        config_data = self.get_configuration_data()

        # FIRST LAYER: If (current date & time - date & time of post publication) <=  24 --> Add post fo Scraping
        for item in links_data[:5]:
            if item[0] != '':
                from_time = 0
                for time_period in config_data['Period']:
                    # check if Time of Publication in Time Period
                    print(from_time)
                    print(int(time_period))
                    print('-----------------------')
                    if self.time_diff_to_hours(item[1]) in range(int(from_time), int(time_period)):
                        print(f'Post is added for Sraping: {item}')
                        print('----------------------------------')
                        break
                    from_time = time_period
            else:
                print('No link in this row!')

        # SECOND LAYER: If the post has been choosen on the previuos step --> Check comments rule:
        #  If (current date & time - date & time of post publication) <= 60 --> Scrape comments from the post

        # Data structure for Links Data
        # links_data = [{'link': 'https://www.linkedin.com/feed/update/urn:li:activity:...', 'link_type': 'linkedin', 'date': '05.07.2023'},
        #               {'link': 'https://www.reddit.com/r/therewasanattempt/comments/...', 'link_type': 'reddit', 'date': '04.07.2023'}]
        # links_data = [['https://www.linkedin.com/feed/update/urn:li:activity:', '05.07.2023'],
        #               ['https://www.reddit.com/r/therewasanattempt/comments/...', '04.07.2023']]

        # Output final Links Data for scraping
        final_links_result = []
        return final_links_result

    def get_configuration_data(self):
        # Read Config Table in Google Sheets

        worksheet = self.connect_to_the_sheeet().worksheet(
            "SMM stats parsing setup & log")

        # Define the list of cell ranges to retrieve values from (e.g., ['A1:A15', 'B1:B15'])
        ranges = ['A1:A15', 'B1:B15', 'C1:C15']

        # Get the cell values within the ranges
        cell_values = worksheet.batch_get(ranges)

        # Declare config data List and Dict
        config_data = []
        config_data_dict = {}

        # Reformat the data to list of lists
        for list in cell_values:
            unpacked_list = [item for sublist in list for item in sublist]
            print(unpacked_list)
            print('----------------------')
            config_data.append(unpacked_list)

        config_data_dict.update(
            {"Period": config_data[0][1:], "LinkedIn posts": config_data[1][1:], 'LinkedIn comments': config_data[2][1:]})
        # Output the Config Data
        return config_data_dict

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

    def time_diff_to_hours(self, datetime_string):
        time_delta_result = datetime.now() - datetime.strptime(datetime_string,
                                                               "%m/%d/%Y %H:%M:%S")

        total_seconds = time_delta_result.total_seconds()
        hours = int(total_seconds // 3600)
        # minutes = int((total_seconds % 3600) // 60)
        # seconds = int(total_seconds % 60)
        # time_delta_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        print(hours)
        return hours

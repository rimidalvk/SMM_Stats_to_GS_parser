import gspread
from gspread import utils
import utils.config as config
from google.oauth2.service_account import Credentials
from datetime import datetime, time

from utils.logger import Logger


class GoogleSheet:
    def __int__(self):
        self.service = 'google_sheets'

    # Function the Authorizes and connects to Google Sheets
    def connect_to_the_sheeet(self):
        # Path to the service account JSON file
        service_account_file = config.service_account_credentials

        # Get ID of the Google Sheet
        spreadsheet_id = config.table_id

        # Create credentials using the service account file
        credentials = Credentials.from_service_account_file(
            service_account_file)
        scoped_credentials = credentials.with_scopes(
            ['https://www.googleapis.com/auth/spreadsheets'])

        # Authenticate using the scoped credentials
        client = gspread.authorize(scoped_credentials)

        # Open the Google Sheet by ID
        spreadsheet = client.open_by_key(spreadsheet_id)

        # Output Google Sheet Object
        return spreadsheet

    # Main function that provides final links for parsing
    def get_links_post(self):

        # Get the resulting lists of links for Main Action
        return self.filter_posts()

    # Get all links from the sheet basing on collumns
    # UPDATE: CAN BE PUT INTO THE SETTINGS text FIE LATER
    def get_all_links_from_sheet(self):
        # Fetch posts links from Google Sheets

        worksheet = self.connect_to_the_sheeet().worksheet("SMM Journal")

        # Reading all column values for "M" and "Q" columns
        values_links_list = worksheet.col_values(
            utils.column_letter_to_index("M"))
        values_dates_list = worksheet.col_values(
            utils.column_letter_to_index("Q"))

        all_links = values_links_list[2:]
        all_publication_times = values_dates_list[2:]

        combined_list = list(zip(all_links, all_publication_times))

        # Output the the combination of Link and Time of Publication
        return combined_list

    # Filter post based on the configuration data
    def filter_posts(self):
        # Input Links_data and Config_data

        # Save all links from the sheet
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

        # Save configuration data
        config_data = self.get_configuration_data()

        # Declare final links list for scraping
        final_links_result = []

        # FIRST LAYER: If (current date & time - date & time of post publication) <=  24 --> Add post fo Scraping
        for item in links_data:
            if item[0] != '' and item[1] != '':  # If link is present and date is specified
                from_time = 0  # Declare period time as 0 for first iteration
                for time_period in config_data['Period']:
                    # check if Time of Publication in Time Period
                    print('This is the time period:',
                          from_time, int(time_period))
                    '''
                        If the time difference in the range of Hours from A column
                        0-24, 24-48 and so on
                    '''
                    if self.time_diff_to_hours(item[1]) in range(int(from_time), int(time_period)):

                        # If Comment:  "?commentUrn" in item[0] or "/comment/" in item[0]: --> Parse tne Comment
                        if "https://www.linkedin.com/" in item[0] and "?commentUrn" in item[0]:
                            parse_every_time = config_data['LinkedIn comments'][config_data['Period'].index(
                                time_period)]
                            print(
                                f'LinkedIn Comment is added for Sсraping: {item} for this time period {from_time, int(time_period)} every {parse_every_time} minutes')

                        elif "https://www.reddit.com/" in item[0] and "/comment/" in item[0]:
                            parse_every_time = config_data['Reddit comments'][config_data['Period'].index(
                                time_period)]
                            print(
                                f'Reddit comment is added for Sсraping: {item} for this time period {from_time, int(time_period)} every {parse_every_time} minutes')

                        # If post:  if "?commentUrn" not in item[0] or "/comment/" not in item[0]: --> Parse tne Post
                        elif "https://www.linkedin.com/" in item[0] and "?commentUrn" not in item[0]:
                            parse_every_time = config_data['LinkedIn posts'][config_data['Period'].index(
                                time_period)]
                            print(
                                f'LinkedIn post is added for Sсraping: {item} for this time period {from_time, int(time_period)} every {parse_every_time} minutes')

                        elif "https://www.reddit.com/" in item[0] and "/comment/" not in item[0]:
                            parse_every_time = config_data['Reddit posts'][config_data['Period'].index(
                                time_period)]
                            print(
                                f'Reddit post is added for Sсraping: {item} for this time period {from_time, int(time_period)} every {parse_every_time} minutes')

                        else:
                            print(f"Chcek the link {item[0]}!")

                        if self.will_be_scraped(parse_every_time, item[1]):
                            print(f'Post will be Sсraped: {item[0]}')

                            final_links_result.append(item[0])

                        print('---------------------------------')
                        break
                    from_time = time_period
            else:
                print('No link in this row!')
            print("-----------------------")

        print(final_links_result)

        # Output final Links Data for scraping
        return final_links_result

    # Get configuration data from the Google Sheet
    def get_configuration_data(self):
        # Read Config Table in Google Sheets

        worksheet = self.connect_to_the_sheeet().worksheet(
            "SMM stats parsing setup & log")

        # Define the list of cell ranges to retrieve values from (e.g., ['A1:A15', 'B1:B15'])
        ranges = ['A1:A15', 'B1:B15', 'C1:C15', 'D1:D15', 'E1:E15']

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
            {"Period": config_data[0][1:], "LinkedIn posts": config_data[1][1:], "LinkedIn comments": config_data[2][1:], "Reddit posts": config_data[3][1:], "Reddit comments": config_data[4][1:]})
        # Output the Config Data
        return config_data_dict

    # Save sraped data into Google Sheet
    def add_result_analytics(self, data):
        # Get Tab in the Google Sheet by name
        worksheet = self.connect_to_the_sheeet().worksheet("Scraping results")

        # Get the Content data from parsing
        # data = [["Datetime", "Link", "Impressions/Views/Upvotes", "Likes", "Number of Comments", "Number of shares/reposts"]]

        # # Get the header row of the Google Sheet
        # header_row = worksheet.row_values(2)

        # # Get the column indices for each column header using the mapping
        # col_indices = [header_row.index(
        #     col_header) + 1 for col_header in column_mapping.keys()]

        # # Write data to rows based on column headers using the mapping and column indices
        # for data_dict in data:
        #     for col_header, col_key in column_mapping.items():
        #         if col_header in header_row:
        #             col_index = col_indices[list(
        #                 column_mapping.keys()).index(col_header)]
        #             # Assuming header is in row 1, so data starts from row 2
        #             row_index = data.index(data_dict) + \
        #                 self.get_last_row_index(worksheet)+1
        #             value = data_dict.get(col_key, "")
        #             worksheet.update_cell(row_index, col_index, str(value))

        # Create a mapping between column headers and dictionary keys
        column_mapping = {
            "Date&Time": "datetime",
            "Link": "link",
            "Impressions/Views": "impressions",
            "Upvote Rate": "upvote_rate",
            "Reactions/Likes": "reactions",
            "Comments": "comments",
            "Shares/Reposts": "reposts",
            "JSON": "json"
        }

        # Get the header row of the Google Sheet
        header_row = worksheet.row_values(2)

        # Prepare the data to update in the Google Sheet
        data_to_update = []
        for data_dict in data:
            row_data = []
            for col_header in column_mapping.keys():
                if col_header in header_row:
                    col_key = column_mapping[col_header]
                    value = data_dict.get(col_key, "")
                    row_data.append(str(value))
            data_to_update.append(row_data)

        # Update the range of cells in one API call
        # Assuming header is in row 2, so data starts from row 3
        start_row = self.get_last_row_index(worksheet)+1
        start_col = 1  # Start from the first column
        end_row = start_row + len(data_to_update) - 1
        end_col = start_col + len(data_to_update[0]) - 1
        # e.g., A2:E3
        range_to_update = f'A{start_row}:{chr(ord("A") + end_col)}{end_row}'
        worksheet.update(range_to_update, data_to_update)

        # worksheet.update(f"A{self.get_last_row_index(worksheet)+1}", data)

        # Write the data into the Google Shet row
        print("Data has been added")

    # Log the worlflow of the script to txt file
    # SHOULD BE UPDATED
    def log_srapper_run(self):
        # Saving errors for each process (functions) that can meet some problems

        # Errors for Reading from the Google Sheets
        # Errors for Writing to the Google Sheet
        # Errors Scraping Data
        # Errors for data manipulation

        log_data = "No errors"
        print("Logs has been saved")
        return log_data

    # Save scraper run result to Google Sheets
    def add_scraper_run_result(self):

        worksheet = self.connect_to_the_sheeet().worksheet(
            "SMM stats parsing setup & log")

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
        # Access the stored data
        cycle_start = self.data_store.get("Cycle start", None)
        cycle_end = self.data_store.get("Cycle end", None)
        total_links_processed = self.data_store.get(
            "Linkedin links", None) + self.data_store.get("Reddit links", None)

        # Errors that can be found during the script run
        errors = self.log_srapper_run()
        # Comments depeneding on the type of error
        comments = ''

        linkedin_posts = self.data_store.get("Linkedin posts", None)
        linkedin_comments = self.data_store.get("Linkedin comments", None)
        reddit_posts = self.data_store.get("Reddit posts", None)
        reddit_comments = self.data_store.get("Reddit comments", None)

        # Write the above logging info into the row
        '''
            Need to consider loging approach
            Could be the text file that contains all logs and saved in the repository or HTML report.
        '''
        worksheet.update(f"A{self.get_last_row_index(worksheet)+1}", [
                         [cycle_start, cycle_end, total_links_processed, errors, linkedin_posts, linkedin_comments, reddit_posts, reddit_comments]])
        print("Data has been added")

    # Convert time difference between post publication and current time to hours
    def time_diff_to_hours(self, datetime_string):
        time_delta_result = datetime.now() - datetime.strptime(datetime_string,
                                                               "%m/%d/%Y %H:%M:%S")

        total_seconds = time_delta_result.total_seconds()
        hours = int(total_seconds // 3600)
        # minutes = int((total_seconds % 3600) // 60)
        # seconds = int(total_seconds % 60)
        # time_delta_str = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        # print('Hours passed after publication time:', hours)
        return hours

    # Funcation that decides if post should be scraped
    def will_be_scraped(self, time_period, publish_date):
        time_period = int(time_period)

        # Main checks whether Post will be scraped
        one_hour_check = datetime.now().minute in range(0, 10)
        other_hours_check = datetime.now().hour % (time_period//60)
        one_day_check = int(self.get_minutes_of_day()) in range(1380, 1440)

        time_frame = int(self.get_minutes_after_publish(publish_date)) / 7200
        decimal_part = round(time_frame % 1, 4)
        five_days_check = 0.9917 <= decimal_part or decimal_part <= 0.0083

        result = True

        ''' Logic Description:
            For 60 minutes --> every 60 minutes from the day start
            For 120/180/240/480 minutes --> if the current hour is devided by time_period without remainder
            For 1440 minutes --> when the current minute in the timeframe between 1400 - 1440 minutes (last hour of day)
            For 7200 minutes --> The decimal part of the division minutes passed from the publication by time_period is +- 0.0083
        '''
        if time_period == 60 and one_hour_check:
            print("For 60 minutes/1 hour")
        elif time_period in [120, 180, 240, 480] and other_hours_check == 0:
            print(f"For {time_period} minutes/{time_period//60} hours")
        elif time_period == 1440 and one_day_check:
            print("For 1440 minutes/1 day")
        elif time_period == 7200 and five_days_check:
            print("For 7200 minutes/5 days")
        else:
            result = False
        return result

    # Get minutes of the current day
    def get_minutes_of_day(self):
        current_date = datetime.now().date()
        start_of_day = datetime.combine(current_date, time.min)
        time_passed = (datetime.now() - start_of_day).total_seconds() // 60
        return time_passed

    # Get minutes data after post publication
    def get_minutes_after_publish(self, publish_date):
        time_delta_result = datetime.now() - datetime.strptime(publish_date,
                                                               "%m/%d/%Y %H:%M:%S")
        total_seconds = time_delta_result.total_seconds()
        minutes_passed = total_seconds // 60
        return minutes_passed

    # Get Last row index with data
    def get_last_row_index(self, worksheet):
        all_values = worksheet.get_all_values()

        # Find the last non-empty row
        last_row_id = None
        for i in range(len(all_values) - 1, -1, -1):
            if any(cell.strip() != "" for cell in all_values[i]):
                last_row_id = i + 1
                break
        return last_row_id

    # Create an empty dictionary to store the data for scraper logging
    data_store = {}

    # Function to store data in the dictionary
    def store_data(self, key, value):
        self.data_store[key] = value

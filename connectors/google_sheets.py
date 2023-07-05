import requests

from utils.logger import Logger


class GoogleSheet:
    def __int__(self):
        self.service = 'google_sheets'


    
    def get_links_post(self, link_table):

        # Get the resulting lists of link for Main Action
        result_links =  self.filter_posts(self.get_all_links_from_sheet, self.get_configuration_data) 
        return result_links
    

    def get_all_links_from_sheet(link_table):
        # Fetch posts links from Google Sheets

        all_links_data = []
        # Output the the combination of Link and Time of Publication 
        return all_links_data
    
    def filter_posts(links, config_data):
        # Input Links_data and Config_data

        # # Detailed Algorithm # #
        # Sort the posts for the last 10 days? - Move this setting to the Config File?
    
        # Filter data basing on the Config Data and Current Date (Calculate the difference) # 
        # NEED TO CLARIFY! WHEN SCRAPER IS CALLED ONCE ON THE LOCAL PC, THE CONFIG DATA DOES NOT MATTER!!!
        # NEED TO UNDERSTAND WHEN EACH SPECIFIC LINK HAS BEEN CHECKED BEFORE!!!
        # During 24 hours  ---> check posts each 60 mintes
        # Between 24 - 48 hours  ---> check posts each 120 mintes
        # Between 48 - 72 hours  ---> check posts each 180 mintes
        # Between 72 - 96 hours  ---> check posts each 1440 mintes
        # Between 96 - 120 hours  ---> check posts each 1440 mintes
        # Between 120 - 144 hours  ---> check posts each 1440 mintes
        # Between 144 - 168 hours  ---> check posts each 1440 mintes
        # Between 168 - 192 hours  ---> check posts each 1440 mintes

        # # #

        # Data structure for Links Data
        links_data = [{'link': 'https://www.linkedin.com/feed/update/urn:li:activity:...', 'link_type': 'linkedin', 'date': '05.07.2023'}, {'link': 'https://www.reddit.com/r/therewasanattempt/comments/...', 'link_type': 'reddit', 'date': '04.07.2023'}  ]
        links_data = [['https://www.linkedin.com/feed/update/urn:li:activity:', '05.07.2023'],  ['https://www.reddit.com/r/therewasanattempt/comments/...', '04.07.2023']]

        # Output final Links Data for scraping
        return 
    


    def get_configuration_data(link_table):
        # Read Config Table in Google Sheets

        # Output the Config Data 
        return

    def add_result_analytics(self, info, link_table):
        # Get Tab in the Google Sheet by name
        # Get the Content Info from parsing 

        # Write the info into the Google Shet row
        print("Data has been added")

        
    def add_srapper_run_result(self, link_table):
        # Get Tab in the Google Sheet by name

        ''' Save the following data:
            - Start Time of the Scrapper Cycle
            - End Time of the Scrapper Cycle
            - Number of Links processed
            - Errors & comments (will be saved into the separte txt file)
            - LinkedIn Posts  precesses
            - LinkedIn Comments in total ?
            - Reddit Posts precessed
            - Reddit Comments in total ?
        '''
        # Write the above logging info into the row 
        print("Data has been added")
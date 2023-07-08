# SMM Metrics Scraper

Project Description
This tool is designed to scrape and track key metrics from social media posts across various platforms and efficiently store this data for analysis and insights. It is designed to work autonomously, adhering to various scraping rules to ensure respectful interaction with social media platforms, and is integrated with Google Sheets for storing and tracking the data.

The key features of this tool include:

Scraping data from various social media platforms.
Configurable frequency for scraping based on post age.
Integration with Google Sheets for data storage and tracking.
Automation of scraping cycles.
Robust logging and planning for efficient tracking and error resolution.
Workflow
The program follows the below algorithm:

Retrieving Post Links and Configurations: The program retrieves the post links and their timestamps from the existing Google Sheets table. It also fetches the configuration rules that define how often different types of posts are queried (e.g., every 60 minutes for the first 24 hours, every 120 minutes afterwards, eventually reducing to once per 6 hours or daily).

Filtering Posts: Based on the retrieved rules, the program filters the list of posts and prepares a list for parsing.

Data Scraping: The program then parses the data from the posts using the links, focusing on extracting and saving the statistics related to each post rather than analyzing the content. The data is scraped carefully, mimicking human-like behavior with variable pauses to avoid being flagged by the social media platforms.

Data Storage: The statistics are then stored in an existing Google Sheets table, with new rows being added for each post after each parsing cycle.

Next Cycle Planning: The program then plans the next cycle (e.g., every 1 hour).

Logging: The program logs the results of each cycle, indicating the start and end times, when the next cycle is planned, the number of successfully processed links, and whether all the data arrived. If there were any errors, these are noted in a comment. The program also logs the IP address and the computer from which it is operating.

Next Cycle Announcement: The program indicates when the next cycle will be, providing clarity for the operator regarding the program's operation.

The goal of this tool is to enable efficient tracking and analysis of social media marketing efforts, making the data accessible for both the Content Manager/Social Media Manager for post tracking and the Marketing Director for data analysis and insights.

# File structure:

src: This is the main directory where the source code of the project resides.

scrapers: Each social media platform has its own scraper module.

integrations: Here is where we integrate with other systems, in this case, Google Sheets.

utils: This includes utility modules, like the config.py for managing the configuration settings, and logger.py for logging.

main.py: This is the main entry point of the application.

tests: This directory contains all unit tests. It's mirrored after the src directory for organization.

docs: This is where you can find all the documentation for the project, including design documents and usage instructions.

.gitignore: This file tells git which files or directories to ignore in the project.

README.md: This is the file you're reading now! A great place for project summary, setup steps, etc.

requirements.txt: This file lists the Python dependencies needed to run this project.

setup.py: This file is used for packaging the project, and can be run to install all necessary dependencies.

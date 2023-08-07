import os
import configparser

# Get the path to the .ini file
ini_file_path = "config_file.ini"

# Check if the .ini file exists
if os.path.exists(ini_file_path):
    # Create a configparser object
    config = configparser.ConfigParser()

    # Read the .ini file
    config.read(ini_file_path)

    # Access the data from the .ini file
    linkedin_profile_name = config.get("user_info", "linkedin_profile_name")
    reddit_profile_name = config.get("user_info", "reddit_profile_name")
    user_chrome_directory = config.get("user_info", "user_chrome_directory")
else:
    print("Config.ini file not found.")

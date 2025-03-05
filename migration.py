import json
import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import csv
import os

DAILY_DATA_DIR = os.path.join("timeout_data", "daily") # Updated directory for daily data
QUARTER_DATA_DIR = os.path.join("timeout_data", "quarters") # Updated directory for quarter data
CHART_OUTPUT_DIR = os.path.join("timeout_data", "charts") # Directory for charts

def migrate_timeout_data_to_yearly_files():
    """
    Migrates data from the existing timeout.csv to yearly CSV files in timeout_data/daily.
    This is a one-time function to organize existing data.
    """
    if not os.path.exists(DAILY_DATA_DIR):
        os.makedirs(DAILY_DATA_DIR)

    data_by_year = {} # Dictionary to hold data grouped by year

    with open('timeout.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date_str = row['Date']
            try:
                date_obj = datetime.strptime(date_str, '%Y-%b-%d')
                year_str = str(date_obj.year)
            except ValueError:
                print(f"Warning: Could not parse date '{date_str}'. Skipping row for migration.")
                continue

            if year_str not in data_by_year:
                data_by_year[year_str] = []
            data_by_year[year_str].append(row)

    for year_str, yearly_data in data_by_year.items():
        yearly_csv_file = os.path.join(DAILY_DATA_DIR, f"timeout_{year_str}.csv")
        file_exists = os.path.isfile(yearly_csv_file)

        with open(yearly_csv_file, 'w', newline='') as csvfile: # Use 'w' to overwrite/create for migration
            fieldnames = ['Date', 'Timeout', 'HTTP Error', 'No Timeout']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader() # Write header for each yearly file
            writer.writerows(yearly_data) # Write all rows for the year

        print(f"Migrated data to {yearly_csv_file}")

    print("Migration of timeout.csv data to yearly files complete.")
    # After successful migration, you can optionally delete timeout.csv:
    # os.remove('timeout.csv')
    # print("Original timeout.csv file deleted.")


if __name__ == "__main__":
  # Run the migration function ONCE to create yearly files from timeout.csv
  migrate_timeout_data_to_yearly_files()
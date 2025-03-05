import json
import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

DAILY_DATA_DIR = os.path.join("timeout_data", "daily")
QUARTER_DATA_DIR = os.path.join("timeout_data", "quarters")
CHART_OUTPUT_DIR = os.path.join("timeout_data", "charts")

def report_timeout():
  releases = json.loads(requests.get("https://raw.githubusercontent.com/lgdd/liferay-product-info/main/releases.json").text)
  date = dt.datetime.now()
  date_str = date.strftime('%Y-%b-%d')
  year_str = str(date.year)
  timed_out = 0
  http_error = 0

  for release in releases:
    url = release["url"]
    try:
      print("GET {0}".format(url))
      response = requests.get(url, timeout=10)
      response.raise_for_status()
      print("^^^ OK")
    except requests.exceptions.Timeout:
      print("^^^ Timeout")
      timed_out += 1
    except requests.exceptions.HTTPError:
      print("^^^ HTTP Error")
      http_error += 1
    except requests.exceptions.RequestException as e:
      print(e)

  no_timeout = len(releases) - (timed_out + http_error)

  if not os.path.exists(DAILY_DATA_DIR):
      os.makedirs(DAILY_DATA_DIR)
  yearly_csv_file = os.path.join(DAILY_DATA_DIR, f"timeout_{year_str}.csv")

  file_exists = os.path.isfile(yearly_csv_file)

  with open(yearly_csv_file, "a", newline='') as csvfile:
      fieldnames = ['Date', 'Timeout', 'HTTP Error', 'No Timeout']
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

      if not file_exists:
          writer.writeheader()

      writer.writerow({'Date': date_str, 'Timeout': timed_out, 'HTTP Error': http_error, 'No Timeout': no_timeout})


def report_timeout_per_quarter():
  quarter_data = {}

  for filename in os.listdir(DAILY_DATA_DIR):
      if filename.startswith("timeout_") and filename.endswith(".csv"):
          yearly_csv_file = os.path.join(DAILY_DATA_DIR, filename)
          with open(yearly_csv_file, 'r', newline='') as csvfile:
              reader = csv.DictReader(csvfile)
              for row in reader:
                  date_str = row['Date']
                  try:
                      date_obj = dt.datetime.strptime(date_str, '%Y-%b-%d')
                  except ValueError:
                      print(f"Warning: Could not parse date '{date_str}'. Skipping row from {filename}: {date_str}")
                      continue

                  year = date_obj.year
                  month = date_obj.month

                  if 1 <= month <= 3:
                      quarter = f"Q1 {year}"
                  elif 4 <= month <= 6:
                      quarter = f"Q2 {year}"
                  elif 7 <= month <= 9:
                      quarter = f"Q3 {year}"
                  else:
                      quarter = f"Q4 {year}"

                  timeout = int(row['Timeout']) if row['Timeout'].isdigit() else 0
                  http_error = int(row['HTTP Error']) if row['HTTP Error'].isdigit() else 0
                  no_timeout = int(row['No Timeout']) if row['No Timeout'].isdigit() else 0

                  if quarter not in quarter_data:
                      quarter_data[quarter] = {
                          'Timeout': 0,
                          'HTTP Error': 0,
                          'No Timeout': 0
                      }
                  quarter_data[quarter]['Timeout'] += timeout
                  quarter_data[quarter]['HTTP Error'] += http_error
                  quarter_data[quarter]['No Timeout'] += no_timeout

  if not os.path.exists(QUARTER_DATA_DIR):
      os.makedirs(QUARTER_DATA_DIR)

  for quarter, aggregated_data in quarter_data.items():
      quarter_parts = quarter.split()
      filename = os.path.join(QUARTER_DATA_DIR, f"{quarter_parts[1]}_{quarter_parts[0]}.csv")
      with open(filename, 'w', newline='') as csvfile:
          fieldnames = ['Quarter', 'Timeout', 'HTTP Error', 'No Timeout']
          writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

          writer.writeheader()
          writer.writerow({
              'Quarter': quarter,
              'Timeout': aggregated_data['Timeout'],
              'HTTP Error': aggregated_data['HTTP Error'],
              'No Timeout': aggregated_data['No Timeout']
          })

def update_chart_per_year(year, data_dir=QUARTER_DATA_DIR):
    if not os.path.exists(CHART_OUTPUT_DIR):
        os.makedirs(CHART_OUTPUT_DIR)

    year_str = str(year)
    yearly_data = []
    quarters = ["Q1", "Q2", "Q3", "Q4"]

    for quarter in quarters:
        csv_filename = os.path.join(data_dir, f"{year_str}_{quarter}.csv")
        if os.path.exists(csv_filename):
            df_quarter = pd.read_csv(csv_filename)
            if not df_quarter.empty:
                yearly_data.append(df_quarter)
        else:
            yearly_data.append(pd.DataFrame({'Quarter': [f"{quarter} {year}"], 'Timeout': [0], 'HTTP Error': [0], 'No Timeout': [0]}))


    if not yearly_data:
        print(f"No data found for year {year}. Skipping chart generation.")
        return

    df_year = pd.concat(yearly_data)
    df_year = df_year.set_index('Quarter')

    ax = df_year[['Timeout', 'HTTP Error', 'No Timeout']].plot(
        kind="bar",
        stacked=True,
        title=f"Timeouts (10s) & HTTP errors for URLs - {year}",
        ylabel="Number of release URLs",
        xlabel="Quarter",
        figsize=(10, 5),
        color=["#bf2c2c", "#700606", "#058700"]
    )

    for bars in ax.containers:
        labels = [int(bar.get_height()) if bar.get_height() > 0 else '' for bar in bars]
        ax.bar_label(bars, labels=labels, label_type='center', color='white')

    plt.xticks(rotation=0)
    plt.tight_layout()
    output_filename = os.path.join(CHART_OUTPUT_DIR, f"timeout_{year}.png")
    plt.savefig(output_filename)
    plt.close()

def update_chart():
  df = pd.read_csv('timeout.csv')

  ax = df.plot(
    kind="bar",
    stacked=True,
    title="Timeouts (10s) & HTTP errors for URLs found in https://releases.liferay.com/releases.json",
    ylabel="Number of release URLs",
    xlabel="",
    x=0,
    figsize=(20,5),
    color=["#bf2c2c", "#700606", "#058700"])

  for bars in ax.containers:
      labels = [int(bar.get_height()) if bar.get_height() > 0 else '' for bar in bars]
      ax.bar_label(bars, labels=labels, label_type='center', color='white')

  plt.xticks(rotation=45, ha='right')
  plt.tight_layout()
  plt.savefig("timeout.png")
  plt.close()

if __name__ == "__main__":
  report_timeout()
  report_timeout_per_quarter()
  years_to_chart = set()

  for filename in os.listdir(QUARTER_DATA_DIR):
      if filename.endswith(".csv"):
          year = filename.split('_')[0]
          if year.isdigit():
              years_to_chart.add(int(year))

  for year in sorted(list(years_to_chart)):
      update_chart_per_year(year, data_dir=QUARTER_DATA_DIR)
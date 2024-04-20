import json
import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

def report_timeout():
  releases = json.loads(requests.get("https://raw.githubusercontent.com/lgdd/liferay-product-info/main/releases.json").text)
  date = dt.datetime.now().strftime('%Y-%b-%d')
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

  with open("timeout.csv", "a") as csv:
    csv.write("{0},{1},{2},{3}\n".format(date,timed_out,http_error,no_timeout))

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

if __name__ == "__main__":
  report_timeout()
  update_chart()
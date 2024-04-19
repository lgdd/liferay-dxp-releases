import json
import requests

with open("timeout.md", "w+") as file:
  file.write("# Timed out release URLs (10s):\n")
print("Timed out release URLs (10s):\n")
releases = json.loads(requests.get("https://raw.githubusercontent.com/lgdd/liferay-product-info/main/releases.json").text)
timed_out = 0
for release in releases:
  url = release["url"]
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
  except requests.exceptions.Timeout:
    with open("timeout.md", "a") as file:
      file.write("- {0}\n".format(url))
    print(url)
    timed_out += 1
with open("timeout.md", "a") as file:
  file.write("## Result\n")
  file.write("**{0}/{1} timed out**".format(timed_out, len(releases)))
print("Result: {0}/{1}".format(timed_out, len(releases)))
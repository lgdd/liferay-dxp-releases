import json
import requests
import subprocess
from dotenv import load_dotenv
from tqdm import tqdm
from pathlib import Path
from bs4 import BeautifulSoup

def download_file(url, filename):
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    with open(filename, 'wb') as file, tqdm(
        desc=filename.name,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=block_size,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)
  except requests.exceptions.RequestException as e:
    print(e)

def create_release(url, release_key, release_title):
  try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all("a", href=True)

    for link in links:
      if "tomcat" in link["href"]:
        file_name = link["href"]
        absolute_url = url + "/" + file_name
        download_file(absolute_url, Path(file_name))
    try:
      print("Creating release '" + release_title + "' with tag '" + release_key + "'...")
      cmd_create_release = "gh release create " + release_key + " $(ls *tomcat*) -t '" + release_title + "'"
      subprocess.run(cmd_create_release, shell=True)
      print("Cleaning assets...")
      subprocess.run("rm *tomcat*", shell=True)
    except subprocess.CalledProcessError as e:
      print(e.output.decode("utf-8"))
      exit(1)
  except requests.exceptions.Timeout:
    print("Timed out for {0}".format(url))
  except requests.exceptions.HTTPError as e:
      print(e)

if __name__ == "__main__":
  load_dotenv()
  subprocess.run("gh config set prompt disabled", shell=True)
  releases = json.loads(requests.get("https://raw.githubusercontent.com/lgdd/liferay-product-info/main/releases.json").text)
  releases.reverse()
  for release in releases:
    url = release["url"]
    release_key = release["releaseKey"]
    release_title = release["productVersion"]
    if "dxp" in url:
      try:
        subprocess.check_output(
          "gh release view {0}".format(release_key),
          shell=True,
          stderr=subprocess.STDOUT)
        print("Release '" + release_title + "' already exists.")
      except subprocess.CalledProcessError as e:
        error_message = e.output.decode("utf-8")
        if "release not found" in error_message:
          create_release(url, release_key, release_title)
        else:
          print(error_message)
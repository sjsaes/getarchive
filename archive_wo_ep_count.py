# -*- coding: utf-8 -*-
"""Archive wo Ep. Count

Original file is located at
    https://colab.research.google.com/drive/1VCh6misxEx8CoXUTdB-OdhwO0v5fs_6L

# archive.rss (Without ep. count)
### [Github](https://github.com/sjsaes/getarchive)
It is recommended to run in Colab for more bandwidth, and download the resulting .zip file.

## Environment Variables
Modify the environment variables to change what this RSS script does.
It is made to work with Archive.org RSS feeds, but realistically any RSS feed with download/stream URLs should work.
It is recommended to use the episode threshold feature, as the downloads will take longer if you do not limit the files downloaded.

*   **rss_feed_url:** This variable declares where to retrieve the RSS feed URL. Point this to an archive.org RSS feed.
*   **download_dir:** Self explanatory. Point this towards a directory available to write and read from that you'll be able to download to.

# Run
From the ribbon, click "Runtime" and select "Run all". You may see a warning. Continue to run the script regardless.

Install dependencies **(Do not modify)**
"""

!pip install requests feedparser

"""Imports **(Do not modify)**"""

import os
import requests
import feedparser

"""Variables"""

rss_feed_url = "https://archive.org/services/collection-rss.php?collection=giant-bomb-audio"
download_dir = "/Volumes/SeaData/Giant Bomb Bombcast Rips"

"""Verify directory is ready **(Do not modify)**"""

os.makedirs(download_dir, exist_ok=True)

feed = feedparser.parse(rss_feed_url)

for entry in feed.entries:
    title = entry.title.replace("/", "_").replace("\\", "_").replace(":", "_").strip()
    if 'enclosures' in entry:
        for enclosure in entry.enclosures:
            if enclosure.type == 'audio/mpeg':
                mp3_url = enclosure.href
                file_name = os.path.join(download_dir, f"{title}.mp3")
                print(f"Downloading: {mp3_url}")
                response = requests.get(mp3_url, stream=True)
                if response.status_code == 200:
                    with open(file_name, 'wb') as mp3_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            mp3_file.write(chunk)
                    print(f"Saved: {file_name}")
                else:
                    print(f"Failed to download: {mp3_url} - Status code: {response.status_code}")
    else:
        print(f"No enc found for entry: {entry.title}")

"""Compress directory for easy downloading. Recommended way to get all files. Comment or disable line if you would prefer to not compress."""

shutil.make_archive(download_dir, 'zip', download_dir)
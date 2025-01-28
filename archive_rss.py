# -*- coding: utf-8 -*-
"""archive.rss
Original file is located at
    https://colab.research.google.com/drive/18kjqicvieaxGPXXeuUbrr-MPhkoT-4P5

# archive.rss/owensaez
It is recommended to run in Colab for more bandwidth, and download the resulting .zip file.

## Environment Variables
Modify the environment variables to change what this RSS script does.
It is made to work with Archive.org RSS feeds, but realistically any RSS feed with download/stream URLs should work.
It is recommended to use the episode threshold feature, as the downloads will take longer if you do not limit the files downloaded.

*   **rss_feed_url:** This variable declares where to retrieve the RSS feed URL. Point this to an archive.org RSS feed.
*   **download_dir:** Self explanatory. Point this towards a directory available to write and read from that you'll be able to download to.
*   **skipped_file:** .txt file to write the names and URLs of files skipped. You'll be able to manually download skipped files if the episode threshold variable wasn't helpful.
*   **episode_threshold:** Declares an integer to stop downloads at. Any files that have an episode number newer than this should be skipped, but anything lower will be downloaded.

# Run
From the ribbon, click "Runtime" and select "Run all". You may see a warning. Continue to run the script regardless.

Install dependencies **(Do not modify)**
"""

!pip install requests feedparser

"""Imports **(Do not modify)**"""

import os
import re
import requests
import feedparser
import shutil

"""Variables"""

rss_feed_url = "https://archive.org/services/collection-rss.php?collection=giant-bomb-audio"
download_dir = "./rips"

"""Verify directory is ready **(Do not modify)**"""

os.makedirs(download_dir, exist_ok=True)

"""[Optional] Skipped record"""

skipped_file = "skipped.txt"

"""Episode Threshold"""

episode_threshold = 850

feed = feedparser.parse(rss_feed_url)
episode_number_regex = re.compile(r'Giant Bombcast (\d+)')

with open(skipped_file, 'w') as skipped_log:
    for entry in feed.entries:
        title = entry.title
        match = episode_number_regex.search(title)

        if match:
            # extract and compare episode number
            episode_number = int(match.group(1))
            if episode_number < episode_threshold:
                if 'enclosures' in entry:
                    for enclosure in entry.enclosures:
                        if enclosure.type == 'audio/mpeg':
                            mp3_url = enclosure.href
                            sanitized_title = title.replace("/", "_").replace("\\", "_").replace(":", "_").strip()
                            file_name = os.path.join(download_dir, f"{sanitized_title}.mp3")
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
                    print(f"No enclosures found for entry: {title}")
            else:
                print(f"Skipped: {title} (Episode number {episode_number} is >= {episode_threshold})")
        else:
            # log titles missing ep number
            skipped_log.write(f"{title} - {entry.link}\n")
            print(f"Skipped: {title} (No episode number found)")

"""Compress directory for easy downloading. Recommended way to get all files. Comment or disable line if you would prefer to not compress."""

shutil.make_archive(download_dir, 'zip', download_dir)
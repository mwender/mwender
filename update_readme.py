import feedparser
import re

FEED_URL = "https://photos.mwender.com/feed/"
README_PATH = "README.md"
START_MARKER = "<!-- photo starts -->"
END_MARKER = "<!-- photo ends -->"

feed = feedparser.parse(FEED_URL)
latest = feed.entries[0]
link = latest.link
title = latest.title
content = latest.get("content", [{}])[0].get("value", "")

# Find the first image tag
img_match = re.search(r'<img[^>]+src="([^"]+)"', content)
img_url = img_match.group(1) if img_match else ""

# Markdown output
markdown = f"[![{title}]({img_url})]({link})"

# Read and update README
with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

updated = re.sub(
    f"{START_MARKER}.*?{END_MARKER}",
    f"{START_MARKER}\n{markdown}\n{END_MARKER}",
    readme,
    flags=re.DOTALL
)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(updated)

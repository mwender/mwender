import feedparser
import re

README_PATH = "README.md"

PHOTO_FEED_URL = "https://photos.mwender.com/feed/"
BLOG_FEED_URL = "https://mwender.com/feed/"

PHOTO_START = "<!-- photo starts -->"
PHOTO_END = "<!-- photo ends -->"
BLOG_START = "<!-- blog starts -->"
BLOG_END = "<!-- blog ends -->"

def update_section(content, start_marker, end_marker, replacement):
  return re.sub(
    f"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
    f"{start_marker}\n{replacement}\n{end_marker}",
    content,
    flags=re.DOTALL
  )

# === Process photo feed ===
photo_feed = feedparser.parse(PHOTO_FEED_URL)
latest_photo = photo_feed.entries[0]
photo_link = latest_photo.link
photo_title = latest_photo.title
photo_content = latest_photo.get("content", [{}])[0].get("value", "")

img_match = re.search(r'<img[^>]+src="([^"]+)"', photo_content)
photo_img_url = img_match.group(1) if img_match else ""

photo_md = f"[![{photo_title}]({photo_img_url})]({photo_link})"

# === Process blog feed ===
blog_feed = feedparser.parse(BLOG_FEED_URL)
blog_items = blog_feed.entries[:5]

blog_md = ""
for entry in blog_items:
  blog_md += f"- [{entry.title}]({entry.link})\n"

# === Update README.md ===
with open(README_PATH, "r", encoding="utf-8") as f:
  readme = f.read()

readme = update_section(readme, PHOTO_START, PHOTO_END, photo_md)
readme = update_section(readme, BLOG_START, BLOG_END, blog_md.strip())

with open(README_PATH, "w", encoding="utf-8") as f:
  f.write(readme)

import feedparser
import re
from datetime import datetime

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
photo_date = latest_photo.published_parsed
formatted_date = datetime(*photo_date[:6]).strftime("%m/%d/%Y")

# Try to get 800x600 from <media:content>
photo_img_url = ""
if "media_content" in latest_photo and len(latest_photo.media_content) > 0:
  photo_img_url = latest_photo.media_content[0].get("url", "")

# Fallback to scraping <img> tag from content:encoded
if not photo_img_url:
  content_html = latest_photo.get("content", [{}])[0].get("value", "")
  img_match = re.search(r'<img[^>]+src="([^"]+)"', content_html)
  if img_match:
    photo_img_url = img_match.group(1)

# Markdown-compatible retina display (800x600 image at 400x300 size)
photo_md = (
  f'<a href="{photo_link}">'
  f'<img src="{photo_img_url}" alt="{photo_title}" width="400" height="300" /></a>\n'
  f'<p><a href="{photo_link}">{photo_title} – {formatted_date}</a></p>'
)

# === Process blog feed ===
blog_feed = feedparser.parse(BLOG_FEED_URL)
blog_items = blog_feed.entries[:5]

blog_md = ""
for entry in blog_items:
  blog_md += f"- [{entry.title}]({entry.link})\n"

# === Update README.md ===
with open(README_PATH, "r", encoding="utf-8") as f:
  readme = f.read()

readme = update_section(readme, PHOTO_START, PHOTO_END, photo_md.strip())
readme = update_section(readme, BLOG_START, BLOG_END, blog_md.strip())

with open(README_PATH, "w", encoding="utf-8") as f:
  f.write(readme)

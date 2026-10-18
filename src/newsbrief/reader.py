from urllib.error import URLError
import ssl
import truststore
from datetime import timezone, datetime, timedelta
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

from .models import Feed, Story


def download_feed(feed: Feed) -> bytes:
    request = Request(
        feed.url,
        headers={"User-Agent":"FinancialNewsBrief/0.1"},
    ) 
    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    with urlopen(request, timeout=15, context=context) as response:
            return response.read()
   
def parse_feed(xml_data: bytes, feed: Feed) -> list[Story]:
    root = ET.fromstring(xml_data)
    stories = []

    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        summary = (item.findtext("description") or "").strip()
        published_text = (item.findtext("pubDate") or "").strip()

        if not title or not url or not published_text:
            continue

        try:
            published_at = parsedate_to_datetime(published_text)
        except (ValueError,TypeError):
            continue

        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        else:
            published_at = published_at.astimezone(timezone.utc)

        stories.append(
            Story(
                title=title,
                url=url,
                source=feed.name,
                category=feed.category,
                published_at=published_at,
                summary=summary,
            )
        )
    return stories


def read_all_feeds(feeds: list[Feed]) -> list[Story]:
    all_stories = []

    for feed in feeds:
        try:
            xml_data = download_feed(feed)
            stories = parse_feed(xml_data, feed)
        except (URLError, ET.ParseError) as error:
            print(f"Could not read {feed.name}: {error}")
            continue

        all_stories.extend(stories)

    return all_stories

def deduplicate_stories(stories: list[Story])->list[Story]:
    unique_stories  = []
    seen_urls = set()

    for story in stories:
        normalized_url = story.url.strip().rstrip("/")

        if normalized_url in seen_urls:
            continue
        seen_urls.add(normalized_url)
        unique_stories.append(story)
    return unique_stories

def filter_recent_stories(
stories: list[Story],
hours: int=24,
)-> list[Story]:
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    return [
        story 
        for story in stories
        if story.published_at >= cutoff
    ]
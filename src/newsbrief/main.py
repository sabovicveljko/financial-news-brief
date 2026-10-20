from .brief import format_daily_brief, select_balanced_stories
from .feeds import FEEDS
from .rates import fetch_eur_usd_rate
from .reader import (
    deduplicate_stories,
    filter_recent_stories,
    read_all_feeds,
)
from .telegram import send_message
from .database import get_sent_story_urls, initialize_database, mark_story_sent


def run_daily_brief()->None:
    initialize_database()
    sent_story_urls = get_sent_story_urls()
    
    stories = read_all_feeds(FEEDS)
    unique_stories = deduplicate_stories(stories)
    recent_stories = filter_recent_stories(unique_stories)
    
    unsent_stories = [
        story for story in recent_stories
        if story.url not in sent_story_urls
    ]
    
    selected_stories = select_balanced_stories(unsent_stories)
    rate = fetch_eur_usd_rate()
    message = format_daily_brief(selected_stories, rate)
    send_message(message)

    for story in selected_stories:
        mark_story_sent(story.url)

if __name__== "__main__":
    run_daily_brief()


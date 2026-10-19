from .brief import format_daily_brief, select_balanced_stories
from .feeds import FEEDS
from .rates import fetch_eur_usd_rate
from .reader import (
    deduplicate_stories,
    filter_recent_stories,
    read_all_feeds,
)
from .telegram import send_message


def run_daily_brief()->None:
    stories = read_all_feeds(FEEDS)
    unique_stories = deduplicate_stories(stories)
    recent_stories = filter_recent_stories(unique_stories)
    selected_stories = select_balanced_stories(recent_stories)
    rate = fetch_eur_usd_rate()
    message = format_daily_brief(selected_stories, rate)
    send_message(message)

if __name__== "__main__":
    run_daily_brief()


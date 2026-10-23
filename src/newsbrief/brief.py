from datetime import datetime
from zoneinfo import ZoneInfo

from .models import Story, ExchangeRate
from .rates import format_exchange_rate

LOCAL_TIMEZONE = ZoneInfo("Europe/Budapest")

def select_balanced_stories(
        stories: list[Story],
        stories_per_category: int = 3,
) -> list[Story]:
    selected = []
    counts = {}
    
    newest_first = sorted(
        stories,
        key= lambda story:story.published_at,
        reverse=True
    )
    
    for story in newest_first:
        category_count = counts.get(story.category,0)
        if category_count >= stories_per_category:
            continue

        selected.append(story)
        counts[story.category] = category_count + 1

    return selected

def format_daily_brief(
        stories: list[Story],
        rate: ExchangeRate,
)-> str:
    lines = [
        "DAILY FINANCIAL NEWS BRIEF",
        f"Generated: {datetime.now(LOCAL_TIMEZONE):%d %b %Y %H:%M %Z}",
        "",
        format_exchange_rate(rate),
    ]

    for category in ("Macro & policy", "Markets & business"):
        category_stories = [
            story for story in stories
            if story.category == category
        ]

        lines.extend(["", category])

        if not category_stories:
            lines.append("No new headlines since the last brief.")
            continue

        for story in category_stories:
            lines.append(f"• {story.title}")
            if story.sentiment and story.sentiment_score is not None:
                lines.append(
                    f"  Model tone: {story.sentiment.title()} "
                    f"({story.sentiment_score:.0%} score)"
                )
            lines.append(
                f"  {story.source} | "
                f"{story.published_at.astimezone(LOCAL_TIMEZONE):%d %b %Y %H:%M %Z}"
            )
            lines.append(f"  {story.url}")
     
    return "\n".join(lines)
 


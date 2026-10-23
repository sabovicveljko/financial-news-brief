from datetime import date, datetime, timezone
from decimal import Decimal
import unittest

from newsbrief.brief import format_daily_brief, select_balanced_stories
from newsbrief.models import ExchangeRate, Story


def make_story(
    title: str,
    category: str,
    hour: int,
    sentiment: str | None = None,
    sentiment_score: float | None = None,
) -> Story:
    return Story(
        title=title,
        url=f"https://example.com/{title.lower().replace(' ', '-')}",
        source="Test source",
        category=category,
        published_at=datetime(2026, 10, 20, hour, tzinfo=timezone.utc),
        summary="Test summary",
        sentiment=sentiment,
        sentiment_score=sentiment_score,
    )


class SelectBalancedStoriesTests(unittest.TestCase):
    def test_selects_newest_story_in_each_category(self) -> None:
        stories = [
            make_story("Older macro", "Macro & policy", 8),
            make_story("Newest macro", "Macro & policy", 10),
            make_story("Older market", "Markets & business", 9),
            make_story("Newest market", "Markets & business", 11),
        ]

        selected = select_balanced_stories(stories, stories_per_category=1)

        self.assertEqual(len(selected), 2)
        self.assertEqual(
            {story.title for story in selected},
            {"Newest macro", "Newest market"},
        )

class FormatDailyBriefTests(unittest.TestCase):
    def test_includes_sentiment_and_score(self) -> None:
        story = make_story(
            "Rates fall",
            "Markets & business",
            11,
            sentiment="positive",
            sentiment_score=0.898,
        )
        rate = ExchangeRate(
            rate_date=date(2026, 10, 20),
            base_currency="EUR",
            quote_currency="USD",
            value=Decimal("1.12"),
            source_url="https://example.com/rate",
        )

        message = format_daily_brief([story], rate)

        self.assertIn("Model tone: Positive (90% score)", message)


if __name__ == "__main__":
    unittest.main()
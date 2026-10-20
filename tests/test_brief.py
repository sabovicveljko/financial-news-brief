from datetime import datetime, timezone
import unittest

from newsbrief.brief import select_balanced_stories
from newsbrief.models import Story


def make_story(title: str, category: str, hour: int) -> Story:
    return Story(
        title=title,
        url=f"https://example.com/{title.lower().replace(' ', '-')}",
        source="Test source",
        category=category,
        published_at=datetime(2026, 10, 20, hour, tzinfo=timezone.utc),
        summary="Test summary",
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


if __name__ == "__main__":
    unittest.main()
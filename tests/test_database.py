import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from newsbrief.database import (
    get_sent_story_urls,
    initialize_database,
    mark_story_sent,
)


class SentStoryDatabaseTests(unittest.TestCase):
    def test_saves_and_deduplicates_story_urls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            test_db_path = Path(temporary_directory) / "test.sqlite3"

            with patch("newsbrief.database.DB_PATH", test_db_path):
                initialize_database()

                url = "https://example.com/story"
                mark_story_sent(url)
                mark_story_sent(url)

                self.assertEqual(get_sent_story_urls(), {url})


if __name__ == "__main__":
    unittest.main()
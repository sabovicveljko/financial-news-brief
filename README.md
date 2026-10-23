# Automated Financial News Brief

A Python project that gathers financial and macroeconomic stories from public RSS feeds and sends a brief to Telegram when run.

The brief includes source links, publication times, and the ECB EUR/USD reference rate. It removes duplicate stories and records sent story URLs in SQLite to avoid repeating them.

The project uses public RSS feeds and free tools. No paid news or AI APIs are required. It does not provide investment advice. Daily scheduling will be added as a later step.

## Features

- Collects headlines from Federal Reserve, European Central Bank, and CNBC RSS feeds.
- Filters for recent stories and removes duplicate links.
- Selects stories across macroeconomic and markets categories.
- Includes the ECB’s EUR/USD reference rate.
- Shows times in the Europe/Budapest time zone.
- Sends the brief through Telegram.
- Tracks sent story links in a local SQLite database.

## AI sentiment analysis

The project uses [ProsusAI/FinBERT](https://huggingface.co/ProsusAI/finbert) through PyTorch and Transformers to classify each selected headline as positive, negative, or neutral. The brief shows the model's selected label and score.

The model analyzes headline text; it does not summarize full articles, predict market direction, or provide investment advice. Its score is a model output, not a guarantee that the label is correct.

FinBERT's model weights are licensed under CC BY-NC-SA 4.0, which restricts commercial use. Review the [model license and usage terms](https://huggingface.co/ProsusAI/finbert) before using the model. The weights are downloaded when the model first runs rather than stored in this repository.

## Sources

| Source | Coverage | Feed |
|---|---|---|
| Federal Reserve | Macro & policy | [Press releases RSS](https://www.federalreserve.gov/feeds/press_all.xml) |
| European Central Bank | Macro & policy | [Press releases RSS](https://www.ecb.europa.eu/rss/press.html) |
| CNBC Business | Markets & business | [Business RSS](https://www.cnbc.com/id/10001147/device/rss/rss.html) |
| CNBC Finance | Markets & business | [Finance RSS](https://www.cnbc.com/id/10000664/device/rss/rss.html) |
| European Central Bank | EUR/USD reference rate | [USD exchange-rate RSS](https://www.ecb.europa.eu/rss/fxref-usd.html) |

## Limitations

- The brief displays headlines, sources, timestamps, and links. It does not summarize full articles or provide investment advice.
- It filters to stories from the previous 24 hours and selects up to three stories per category.
- Feed contents and availability depend on the publishers; missing or unavailable feeds can result in fewer headlines.
- The EUR/USD value is the ECB reference rate, not a live trading or transaction rate.
- Sent-story history is stored in a local SQLite file. If the program runs in a different environment, that history must be carried over or configured to persist, or previously sent stories could appear again.

## Requirements

- Python 3.12 or newer
- Git
- A Telegram bot and chat
- An internet connection

## Local setup (Windows PowerShell)

Replace `https://github.com/sabovicveljko/financial-news-brief.git` with your GitHub repository’s clone URL before running these commands:

```powershell
git clone https://github.com/sabovicveljko/financial-news-brief.git
cd financial-news-brief
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m pip install -r requirements-ai.txt
Copy-Item .env.example .env
```

Edit `.env` to add your Telegram bot token and chat ID. Keep `.env` private: never commit it or share its contents.

Run the brief:

```powershell
.\.venv\Scripts\python.exe -m newsbrief.main
```

Run the tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Daily automation with GitHub Actions

The workflow in `.github/workflows/daily-brief.yml` runs the brief every day at 08:15 Europe/Budapest time. You can also start it manually from the repository’s **Actions** tab.

To enable it in your own repository:

1. Add these repository secrets under **Settings → Secrets and variables → Actions**:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
2. Push the workflow file to the repository’s default branch.
3. Open **Actions → Daily Financial News Brief → Run workflow** to test it.

The workflow runs the project’s tests before sending the Telegram message. After sending, it commits the updated SQLite sent-story history so later runs can avoid repeating stories. This requires the workflow’s `GITHUB_TOKEN` to have permission to write repository contents.

The schedule uses GitHub-hosted runners. GitHub may delay scheduled runs during busy periods, so 08:15 is the intended start time, not a guaranteed delivery time. The database file must persist between runs; this workflow stores it in the repository.

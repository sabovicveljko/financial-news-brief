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

Replace `<repository-url>` with your GitHub repository’s clone URL before running these commands:

```powershell
git clone <repository-url>
cd financial-news-brief
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
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
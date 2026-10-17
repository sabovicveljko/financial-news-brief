from .models import Feed



FEEDS = [
    Feed(
        name="Federal Reserve",
        category = "Macro & policy",
        url="https://www.federalreserve.gov/feeds/press_all.xml"
    ),
    Feed(
        name="European Central Bank",
        category="Macro & policy",
        url="https://www.ecb.europa.eu/rss/press.html",
    ),
    Feed(
        name="CNBC Business",
        category="Markets & business",
        url="https://www.cnbc.com/id/10001147/device/rss/rss.html",
    ),
    Feed(
        name="CNBC Finance",
        category="Markets & business",
        url="https://www.cnbc.com/id/10000664/device/rss/rss.html",
    ),
]
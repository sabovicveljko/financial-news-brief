from datetime import datetime
from decimal import Decimal
import xml.etree.ElementTree as ET

from .models import ExchangeRate, Feed
from .reader import download_feed

ECB_USD_FEED = Feed(
    name="ECB EUR/USD reference rate",
    category="Macro & policy",
    url="https://www.ecb.europa.eu/rss/fxref-usd.html",
)

NAMESPACES = {
    "rss": "http://purl.org/rss/1.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "cb": "http://www.cbwiki.net/wiki/index.php/Specification_1.1",
}

def  fetch_eur_usd_rate() -> ExchangeRate:
    xml_data = download_feed(ECB_USD_FEED)
    root = ET.fromstring(xml_data)
    item = root.find(".//rss:item", NAMESPACES)
    if item is None:
        raise ValueError("The ECB feed contains no rate items.")
    exchange_rate = item.find(
        "cb:statistics/cb:exchangeRate",
        NAMESPACES,
        )
    if exchange_rate is None:
        raise ValueError("The ECB item has no exchange-rate data.")
    value_text = exchange_rate.findtext("cb:value", namespaces=NAMESPACES)
    base_currency = exchange_rate.findtext(
        "cb:baseCurrency",
        namespaces=NAMESPACES,
    )
    quote_currency = exchange_rate.findtext(
        "cb:targetCurrency",
        namespaces=NAMESPACES,
    )
    date_text = item.findtext("dc:date", namespaces=NAMESPACES)
    source_url = item.findtext("rss:link", namespaces=NAMESPACES)

    if not all((value_text, base_currency, date_text, quote_currency, source_url)):
        raise ValueError("The ECB item is missing a required field.")

    return ExchangeRate(
        rate_date=datetime.fromisoformat(date_text).date(),
        base_currency=base_currency,
        quote_currency=quote_currency,
        value=Decimal(value_text),
        source_url=source_url,
    )

def format_exchange_rate(rate: ExchangeRate) -> str:
    return (
        f"ECB reference rate ({rate.rate_date:%d %b %Y})\n"
        f"1 {rate.base_currency} = "
        f"{rate.value:.4f} {rate.quote_currency}\n"
        f"Source: {rate.source_url}"
    )
    
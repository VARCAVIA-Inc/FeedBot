# example_publisher/providers/jetfuel.py
#
# Preleva il prezzo Jet Fuel Gulf Coast da FRED
# Serie: DJFUELUSGULF  USD per gallone
#

import os, requests
from decimal import Decimal
from datetime import datetime, timezone
from example_publisher.interfaces import PriceProvider, Price

FRED_SERIES = "DJFUELUSGULF"                # puoi cambiarlo se vuoi un’altra serie
FRED_API = "https://api.stlouisfed.org/fred/series/observations"

class JetFuelProvider(PriceProvider):
    def __init__(self, fred_api_key: str):
        self.fred_api_key = fred_api_key

    def get_price(self) -> Price:
        params = {
            "series_id": FRED_SERIES,
            "api_key": self.fred_api_key,
            "limit": 1,
            "sort_order": "desc"
        }
        res = requests.get(FRED_API, params=params, timeout=10)
        res.raise_for_status()
        obs = res.json()["observations"][0]
        value = Decimal(obs["value"])
        ts = int(datetime.strptime(obs["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
        # confidence all’1 percento
        return Price(price=value, conf=value * Decimal("0.01"), publish_time=ts, exponent=-3)

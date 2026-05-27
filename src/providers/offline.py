"""Offline-first provider with optional JSON overrides."""

from __future__ import annotations

import json
from pathlib import Path

from src.config import Config
from src.models import MarketSnapshot, StockSnapshot
from src.providers.base import DataNotFoundError, MarketDataProvider
from src.providers.default_data import DEFAULT_MARKET, DEFAULT_STOCKS


class OfflineFirstProvider(MarketDataProvider):
    """Load local JSON fixture data first, then fall back to built-ins."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config.load()
        payload = self._load_payload()
        self._market = MarketSnapshot(**payload["market"])
        self._stocks = {
            item["code"]: StockSnapshot(
                notes=tuple(item.get("notes", [])),
                **{key: value for key, value in item.items() if key != "notes"},
            )
            for item in payload["stocks"]
        }

    @property
    def source_name(self) -> str:
        if self.config.sample_data_path:
            return "json-fixture"
        return "built-in-fixture"

    def _load_payload(self) -> dict:
        if not self.config.sample_data_path:
            return {"market": DEFAULT_MARKET, "stocks": DEFAULT_STOCKS}

        path = Path(self.config.sample_data_path)
        if not path.exists():
            return {"market": DEFAULT_MARKET, "stocks": DEFAULT_STOCKS}

        payload = json.loads(path.read_text(encoding="utf-8"))
        if "market" not in payload or "stocks" not in payload:
            return {"market": DEFAULT_MARKET, "stocks": DEFAULT_STOCKS}
        return payload

    def get_market_snapshot(self, date: str | None = None) -> MarketSnapshot:
        if date and date != self._market.date:
            return MarketSnapshot(date=date, **{key: value for key, value in self._market.to_dict().items() if key != "date"})
        return self._market

    def get_stock_snapshot(self, stock_code: str) -> StockSnapshot:
        try:
            return self._stocks[stock_code]
        except KeyError as exc:
            raise DataNotFoundError(stock_code) from exc

    def list_stock_candidates(self) -> list[StockSnapshot]:
        return list(self._stocks.values())

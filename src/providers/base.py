"""Provider interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import MarketSnapshot, StockSnapshot


class DataNotFoundError(KeyError):
    """Raised when requested market data is unavailable."""


class MarketDataProvider(ABC):
    """Common interface for market data providers."""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Human-readable provider name."""

    @abstractmethod
    def get_market_snapshot(self, date: str | None = None) -> MarketSnapshot:
        """Return the market snapshot for a date."""

    @abstractmethod
    def get_stock_snapshot(self, stock_code: str) -> StockSnapshot:
        """Return the stock snapshot for a given code."""

    @abstractmethod
    def list_stock_candidates(self) -> list[StockSnapshot]:
        """Return all candidate stocks known by the provider."""

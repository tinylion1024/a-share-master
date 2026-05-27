"""Risk controls for the A-share skill."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date as date_cls
from typing import Optional

from src.config import Config
from src.providers import MarketDataProvider, OfflineFirstProvider


@dataclass(frozen=True)
class RiskCheckResult:
    """Risk evaluation result."""

    stock_code: str
    is_clear: bool
    risk_level: str
    red_flags: list[str]
    warnings: list[str]
    earnings_window_risk: bool
    details: dict

    def to_dict(self) -> dict:
        return asdict(self)


class RiskChecker:
    """Apply mandatory trading guardrails."""

    def __init__(self, config: Optional[Config] = None, provider: Optional[MarketDataProvider] = None):
        self.config = config or Config.load()
        self.provider = provider or OfflineFirstProvider(self.config)
        self.earnings_death_window = (4, 20, 4, 30)

    def check(self, stock_code: str, date: Optional[str] = None) -> RiskCheckResult:
        stock = self.provider.get_stock_snapshot(stock_code)
        red_flags: list[str] = []
        warnings: list[str] = []

        if self.check_investigation(stock_code):
            red_flags.append("立案调查")
        if self.check_delisting_risk(stock_code):
            red_flags.append("退市预警")
        if self.check_earnings_shock(stock_code):
            red_flags.append("业绩巨亏")
        if self.check_reduction(stock_code):
            warnings.append("减持计划")
        if stock.turnover_million < self.config.min_daily_turnover_million:
            warnings.append("流动性不足")

        effective_date = date or date_cls.today().isoformat()
        earnings_window_risk = self.is_in_earnings_death_window(effective_date) and not stock.earnings_disclosed
        if earnings_window_risk:
            red_flags.append("业绩窗口未披露")

        if red_flags:
            risk_level = "R3"
        elif warnings:
            risk_level = "R2"
        else:
            risk_level = "R1"

        details = stock.to_dict()
        details["checked_date"] = effective_date
        return RiskCheckResult(
            stock_code=stock_code,
            is_clear=not red_flags,
            risk_level=risk_level,
            red_flags=red_flags,
            warnings=warnings,
            earnings_window_risk=earnings_window_risk,
            details=details,
        )

    def check_investigation(self, stock_code: str) -> bool:
        return self.provider.get_stock_snapshot(stock_code).under_investigation

    def check_delisting_risk(self, stock_code: str) -> bool:
        stock = self.provider.get_stock_snapshot(stock_code)
        return stock.delisting_risk or stock.name.upper().startswith("*ST")

    def check_reduction(self, stock_code: str) -> bool:
        return self.provider.get_stock_snapshot(stock_code).reduction_plan

    def check_earnings_shock(self, stock_code: str) -> bool:
        return self.provider.get_stock_snapshot(stock_code).earnings_shock

    def is_in_earnings_death_window(self, date: str) -> bool:
        month, day = int(date[5:7]), int(date[8:10])
        start_month, start_day, end_month, end_day = self.earnings_death_window
        return (month == start_month and day >= start_day) or (month == end_month and day <= end_day)

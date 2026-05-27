"""Unified high-availability skill facade."""

from __future__ import annotations

from typing import Optional

from src.config import Config
from src.core import AnalysisPipeline, IntegratedAnalyzer, RiskChecker
from src.modules import HighPRStockPicker, PostMarketAnalyzer, PreMarketAnalyzer, TradingPlanGenerator
from src.providers import MarketDataProvider, OfflineFirstProvider


class ASharesSkill:
    """Single entry point for agent-compatible skill execution."""

    def __init__(self, config: Optional[Config] = None, provider: Optional[MarketDataProvider] = None):
        self.config = config or Config.load()
        self.provider = provider or OfflineFirstProvider(self.config)
        self.pipeline = AnalysisPipeline(self.config, self.provider)
        self.analyzer = IntegratedAnalyzer(self.config, self.provider)
        self.risk_checker = RiskChecker(self.config, self.provider)
        self.stock_picker = HighPRStockPicker(self.config, self.provider)
        self.pre_market = PreMarketAnalyzer(self.config, self.provider)
        self.post_market = PostMarketAnalyzer(self.config, self.provider)
        self.trading_plan = TradingPlanGenerator(self.config, self.provider)

    def diagnose(
        self,
        stock_code: str,
        scenario: str = "诊股",
        horizon: str = "短线",
        risk_preference: str = "平衡型",
        date: str | None = None,
    ) -> dict:
        return self.pipeline.run_standard_flow(
            stock_code=stock_code,
            scenario=scenario,
            horizon=horizon,
            risk_preference=risk_preference,
            date=date,
        )

    def risk(self, stock_code: str, date: str | None = None) -> dict:
        return self.risk_checker.check(stock_code, date).to_dict()

    def pick(self, filter_names: list[str]) -> list[dict]:
        return [item.to_dict() for item in self.stock_picker.screen({"names": filter_names})]

    def pre_market_report(self, date: str) -> dict:
        return self.pre_market.generate_report(date).to_dict()

    def post_market_review(self, date: str) -> dict:
        return self.post_market.generate_review(date).to_dict()

    def trading_plan_report(self, stock_code: str, date: str) -> dict:
        return self.trading_plan.generate_plan(stock_code, date).to_dict()

    def self_check(self) -> dict:
        stocks = self.provider.list_stock_candidates()
        return {
            "config_valid": self.config.validate(),
            "offline_mode": self.config.offline_mode,
            "provider": self.provider.source_name,
            "supported_scenarios": ["diagnose", "risk", "pick", "pre-market", "post-market", "plan"],
            "sample_stock_codes": [stock.code for stock in stocks[:4]],
        }

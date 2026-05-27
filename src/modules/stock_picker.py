"""High risk-reward stock screener."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from src.config import Config
from src.providers import MarketDataProvider, OfflineFirstProvider


@dataclass(frozen=True)
class HighPRStock:
    """Candidate produced by the stock picker."""

    code: str
    name: str
    price: float
    ma20_position: float
    boll_position: float
    pe: float
    growth_q1: float
    turnover_rank: int
    catalyst: str
    entry_price: float
    target_price: float
    stop_loss: float
    risk_reward_ratio: float

    def to_dict(self) -> dict:
        return asdict(self)


class HighPRStockPicker:
    """Offline-first stock picker."""

    def __init__(self, config: Optional[Config] = None, provider: Optional[MarketDataProvider] = None):
        self.config = config or Config.load()
        self.provider = provider or OfflineFirstProvider(self.config)

    def screen(self, filters: Optional[dict] = None) -> list[HighPRStock]:
        filter_names = set(filters.get("names", [])) if filters else set()
        stocks = sorted(self.provider.list_stock_candidates(), key=lambda item: item.turnover_million, reverse=True)
        ranked: list[HighPRStock] = []

        for index, stock in enumerate(stocks, start=1):
            if stock.delisting_risk or stock.under_investigation:
                continue
            if "basic" in filter_names and (not stock.above_ma20 or stock.pe > 40):
                continue
            if "tech" in filter_names and (stock.momentum_score < 3 or stock.boll_position > 0.9):
                continue
            if "catalyst" in filter_names and not stock.catalyst:
                continue

            ranked.append(
                HighPRStock(
                    code=stock.code,
                    name=stock.name,
                    price=stock.price,
                    ma20_position=round(stock.price / stock.ma20, 2),
                    boll_position=stock.boll_position,
                    pe=stock.pe,
                    growth_q1=stock.q1_growth,
                    turnover_rank=index,
                    catalyst=stock.catalyst,
                    entry_price=round(min(stock.price, stock.resistance * 0.99), 2),
                    target_price=round(stock.resistance, 2),
                    stop_loss=round(stock.support, 2),
                    risk_reward_ratio=stock.risk_reward_ratio,
                )
            )

        return sorted(ranked, key=lambda item: item.risk_reward_ratio, reverse=True)

    def extract_technical_levels(self, stock_codes: list[str]) -> dict:
        result = {}
        for code in stock_codes:
            stock = self.provider.get_stock_snapshot(code)
            result[code] = {
                "ma20": stock.ma20,
                "support": stock.support,
                "resistance": stock.resistance,
                "boll_position": stock.boll_position,
            }
        return result

    def synthesize_plan(self, stock: HighPRStock, catalysts: list[str]) -> dict:
        confidence = "高" if stock.risk_reward_ratio >= 2.5 else "中"
        return {
            "entry": stock.entry_price,
            "target": stock.target_price,
            "stop_loss": stock.stop_loss,
            "confidence": confidence,
            "catalysts": catalysts,
        }

    def analyze_tianliang_market(self, total_volume: float) -> str:
        if total_volume > 20000:
            return "超级天量模式：只做有承接的大中军"
        if total_volume > 15000:
            return "天量模式：重视筹码换手和次日承接"
        if total_volume < 8000:
            return "缩量模式：只看低位核心"
        return "正常模式"

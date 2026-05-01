"""
四维评级系统
整合自: a-share-integrated-expert, a-share-profit-helper
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class FourDimensionRating:
    """
    四维评级

    机会⭐：上涨空间与概率 (1-5)
    安全⭐：风险程度 (1-5) - R3红线
    确定⭐：上涨逻辑清晰度 (1-5)
    舒适⭐：持有体验 (1-5)
    """

    opportunity: int      # 机会星 (1-5)
    safety: int           # 安全星 (1-5)
    certainty: int        # 确定星 (1-5)
    comfort: int          # 舒适星 (1-5)

    @property
    def total_score(self) -> float:
        """综合评分（加权）"""
        return (
            self.opportunity * 0.30 +
            self.safety * 0.25 +
            self.certainty * 0.25 +
            self.comfort * 0.20
        )

    @property
    def is_recommended(self) -> bool:
        """是否推荐（R3红线：安全⭐<3 禁止推荐）"""
        return self.safety >= 3 and self.opportunity >= 3 and self.certainty >= 3

    @property
    def level(self) -> str:
        """评级等级"""
        score = self.total_score
        if score >= 4.5:
            return "⭐⭐⭐⭐⭐ 立即买"
        elif score >= 3.5:
            return "⭐⭐⭐⭐ 可以买"
        elif score >= 2.5:
            return "⭐⭐⭐ 观望"
        return "⭐⭐ 回避"


@dataclass
class RiskLevel:
    """风险等级"""
    risk: str             # R1(低)/R2(中)/R3(高)
    opportunity: str       # O1(大)/O2(中)/O3(小)
    certainty: str         # C1(高)/C2(中)/C3(低)
    comfort_star: int      # 舒适度 (1-5星)


class RatingSystem:
    """
    四维评级系统

    评级维度：
    - Risk: 风险等级 (R1/R2/R3)
    - Opportunity: 机会等级 (O1/O2/O3)
    - Certainty: 确定性等级 (C1/C2/C3)
    - Comfort: 舒适度 (⭐)

    决策树：
    - 安全⭐ < 3 → 不买（R3红线）
    - 安全⭐≥3 + 机会⭐≥3 + 确定⭐≥3 → 可以买
    """

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}

    def rate_stock(self, stock_code: str) -> FourDimensionRating:
        """
        对股票进行四维评级

        Args:
            stock_code: 股票代码

        Returns:
            FourDimensionRating: 四维评级结果
        """
        # TODO: 接入分析系统
        raise NotImplementedError("等待 API 集成")

    def calculate_comfort(self, price_position: str, volume_pattern: str) -> int:
        """
        计算舒适度

        判定准则：
        - 5星（极佳）：底部分歧转一致、缩量回踩关键均线、行业中军稳步放量
        - 3星（一般）：追涨非一字板龙头、板块内跟涨个股
        - 1星（风险）：一字板排单、高位放量分歧、业绩盲盒期

        Args:
            price_position: 价格位置描述
            volume_pattern: 量能模式

        Returns:
            int: 舒适度星级 (1-5)
        """
        score = 3  # 默认一般

        if "底部分歧转一致" in price_position or "缩量回踩" in price_position:
            score = 5
        elif "一字板" in price_position or "高位放量分歧" in price_position:
            score = 1
        elif "追涨" in price_position:
            score = 3

        return score

    def check_r3红线(self, safety_star: int) -> bool:
        """
        检查R3红线

        Args:
            safety_star: 安全星 (1-5)

        Returns:
            bool: True if 触发红线
        """
        return safety_star < 3
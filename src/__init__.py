"""A-Shares Master"""

from .core import (
    IntegratedAnalyzer,
    FourDimensionRating,
    RiskChecker,
    AnalysisPipeline,
)
from .modules import (
    PreMarketAnalyzer,
    PostMarketAnalyzer,
    HighPRStockPicker,
    TradingPlanGenerator,
)

__version__ = "2.0.0"

__all__ = [
    # Core
    "IntegratedAnalyzer",
    "FourDimensionRating",
    "RiskChecker",
    "AnalysisPipeline",
    # Modules
    "PreMarketAnalyzer",
    "PostMarketAnalyzer",
    "HighPRStockPicker",
    "TradingPlanGenerator",
]
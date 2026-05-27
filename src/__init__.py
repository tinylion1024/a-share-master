"""A-Shares Master"""

from .config import Config
from .core import (
    IntegratedAnalyzer,
    FourDimensionRating,
    RatingSystem,
    RiskChecker,
    AnalysisPipeline,
)
from .modules import (
    PreMarketAnalyzer,
    PostMarketAnalyzer,
    HighPRStockPicker,
    TradingPlanGenerator,
)
from .skill import ASharesSkill

__version__ = "2.0.0"

__all__ = [
    "Config",
    # Core
    "IntegratedAnalyzer",
    "FourDimensionRating",
    "RatingSystem",
    "RiskChecker",
    "AnalysisPipeline",
    # Modules
    "PreMarketAnalyzer",
    "PostMarketAnalyzer",
    "HighPRStockPicker",
    "TradingPlanGenerator",
    "ASharesSkill",
]

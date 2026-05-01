"""配置管理"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """A-Shares Master 配置"""
    # API Keys
    mx_apikey: Optional[str] = None
    em_api_key: Optional[str] = None
    iwencai_base_url: str = "https://openapi.iwencai.com"
    iwencai_api_key: Optional[str] = None

    # Trading params
    max_position_ratio: float = 0.5    # 最大仓位50%
    max_single_position: float = 0.3   # 单只最大30%
    stop_loss_ratio: float = 0.07     # 止损7%

    # Cache & Log
    data_cache_dir: str = "/tmp/a_shares_cache"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        return cls(
            mx_apikey=os.getenv("MX_APIKEY"),
            em_api_key=os.getenv("EM_API_KEY"),
            iwencai_base_url=os.getenv("IWENCAI_BASE_URL", "https://openapi.iwencai.com"),
            iwencai_api_key=os.getenv("IWENCAI_API_KEY"),
            max_position_ratio=float(os.getenv("MAX_POSITION_RATIO", "0.5")),
            max_single_position=float(os.getenv("MAX_SINGLE_POSITION", "0.3")),
            stop_loss_ratio=float(os.getenv("STOP_LOSS_RATIO", "0.07")),
            data_cache_dir=os.getenv("DATA_CACHE_DIR", "/tmp/a_shares_cache"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    def validate(self) -> bool:
        """验证必要配置"""
        required = [self.mx_apikey, self.em_api_key]
        return all(required)
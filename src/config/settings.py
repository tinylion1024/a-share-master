"""Runtime configuration for the A-share skill."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Optional


def _to_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Config:
    """Skill configuration with offline-first defaults."""

    mx_apikey: Optional[str] = None
    em_api_key: Optional[str] = None
    iwencai_base_url: str = "https://openapi.iwencai.com"
    iwencai_api_key: Optional[str] = None

    max_position_ratio: float = 0.5
    max_single_position: float = 0.3
    stop_loss_ratio: float = 0.07
    profit_target_multiplier: float = 3.0

    min_daily_turnover_million: float = 50.0
    data_cache_dir: str = "/tmp/a_shares_cache"
    sample_data_path: Optional[str] = None
    offline_mode: bool = True
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables only."""
        return cls(
            mx_apikey=os.getenv("MX_APIKEY"),
            em_api_key=os.getenv("EM_API_KEY"),
            iwencai_base_url=os.getenv("IWENCAI_BASE_URL", "https://openapi.iwencai.com"),
            iwencai_api_key=os.getenv("IWENCAI_API_KEY"),
            max_position_ratio=float(os.getenv("MAX_POSITION_RATIO", "0.5")),
            max_single_position=float(os.getenv("MAX_SINGLE_POSITION", "0.3")),
            stop_loss_ratio=float(os.getenv("STOP_LOSS_RATIO", "0.07")),
            profit_target_multiplier=float(os.getenv("PROFIT_TARGET_MULTIPLIER", "3")),
            min_daily_turnover_million=float(os.getenv("MIN_DAILY_TURNOVER_MILLION", "50")),
            data_cache_dir=os.getenv("DATA_CACHE_DIR", "/tmp/a_shares_cache"),
            sample_data_path=os.getenv("A_SHARE_SKILL_DATA_PATH"),
            offline_mode=_to_bool(os.getenv("A_SHARE_SKILL_OFFLINE_MODE"), True),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    @classmethod
    def from_file(cls, path: str | Path) -> "Config":
        """Load configuration from a JSON file."""
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            mx_apikey=payload.get("env", {}).get("mx_apikey"),
            em_api_key=payload.get("env", {}).get("em_apikey"),
            iwencai_base_url=payload.get("env", {}).get("iwencai_base_url", "https://openapi.iwencai.com"),
            iwencai_api_key=payload.get("env", {}).get("iwencai_api_key"),
            max_position_ratio=float(payload.get("trading", {}).get("max_total_position", 0.5)),
            max_single_position=float(payload.get("trading", {}).get("max_position_per_stock", 0.3)),
            stop_loss_ratio=float(payload.get("trading", {}).get("stop_loss_rate", 0.07)),
            profit_target_multiplier=float(payload.get("trading", {}).get("profit_target_multiplier", 3.0)),
            min_daily_turnover_million=float(payload.get("filters", {}).get("min_daily_volume", 50000000)) / 1_000_000,
            data_cache_dir=payload.get("env", {}).get("data_cache_dir", "/tmp/a_shares_cache"),
            sample_data_path=payload.get("env", {}).get("sample_data_path"),
            offline_mode=_to_bool(payload.get("env", {}).get("offline_mode"), True),
            log_level=payload.get("env", {}).get("log_level", "INFO"),
        )

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "Config":
        """Merge JSON file config with environment overrides."""
        file_config = cls()
        if config_path:
            path = Path(config_path)
            if path.exists():
                file_config = cls.from_file(path)

        env_config = cls.from_env()
        merged = asdict(file_config)
        for key, value in asdict(env_config).items():
            if value not in (None, "", False):
                merged[key] = value
        if os.getenv("A_SHARE_SKILL_OFFLINE_MODE") is not None:
            merged["offline_mode"] = env_config.offline_mode
        return cls(**merged)

    def validate(self) -> bool:
        """The skill is valid if offline mode or at least one live credential exists."""
        if self.offline_mode:
            return True
        return any([self.mx_apikey, self.em_api_key, self.iwencai_api_key])

    def missing_live_credentials(self) -> list[str]:
        """Return missing live credentials when offline mode is disabled."""
        if self.offline_mode:
            return []
        required = {
            "MX_APIKEY": self.mx_apikey,
            "EM_API_KEY": self.em_api_key,
            "IWENCAI_API_KEY": self.iwencai_api_key,
        }
        return [key for key, value in required.items() if not value]

    def as_dict(self) -> dict[str, Any]:
        """Serialize the config."""
        return asdict(self)

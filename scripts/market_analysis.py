#!/usr/bin/env python3
"""Market analysis script."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli import render_json
from src.skill import ASharesSkill


def main() -> None:
    parser = argparse.ArgumentParser(description="市场分析脚本")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="日期 (YYYY-MM-DD)")
    args = parser.parse_args()

    payload = ASharesSkill().analyzer.analyze_liquidity_pattern(args.date)
    print(render_json(payload))


if __name__ == "__main__":
    main()

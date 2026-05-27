#!/usr/bin/env python3
"""Post-market review script."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli import render_json, render_post_market
from src.skill import ASharesSkill


def main() -> None:
    parser = argparse.ArgumentParser(description="盘后复盘脚本")
    parser.add_argument("--date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="日期 (YYYY-MM-DD)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    args = parser.parse_args()

    payload = ASharesSkill().post_market_review(args.date)
    print(render_json(payload) if args.format == "json" else render_post_market(payload))


if __name__ == "__main__":
    main()

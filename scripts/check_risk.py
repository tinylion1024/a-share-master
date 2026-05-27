#!/usr/bin/env python3
"""Risk scanner script."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli import render_json, render_risk_report
from src.skill import ASharesSkill


def main() -> None:
    parser = argparse.ArgumentParser(description="风险扫描脚本")
    parser.add_argument("--code", type=str, required=True, help="股票代码")
    parser.add_argument("--date", type=str, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--format", choices=["markdown", "json"], default="json", help="输出格式")
    args = parser.parse_args()

    payload = ASharesSkill().risk(args.code, args.date)
    print(render_json(payload) if args.format == "json" else render_risk_report(payload))


if __name__ == "__main__":
    main()

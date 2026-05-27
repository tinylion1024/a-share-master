#!/usr/bin/env python3
"""Stock picker script."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli import normalize_filters, render_json, render_stock_picker
from src.skill import ASharesSkill


def main() -> None:
    parser = argparse.ArgumentParser(description="智能选股脚本")
    parser.add_argument("--filters", nargs="+", default=["basic", "tech", "catalyst"], help="启用的过滤器")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    args = parser.parse_args()

    filters = normalize_filters(args.filters)
    payload = ASharesSkill().pick(filters)
    print(render_json(payload) if args.format == "json" else render_stock_picker(payload, filters))


if __name__ == "__main__":
    main()

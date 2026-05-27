#!/usr/bin/env python3
"""Unified runner for the A-share skill."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.cli import (
    normalize_filters,
    render_diagnosis,
    render_json,
    render_post_market,
    render_pre_market,
    render_risk_report,
    render_stock_picker,
    render_trading_plan,
)
from src.skill import ASharesSkill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A-share skill runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("self-check", help="检查 Skill 是否可运行")

    risk = subparsers.add_parser("risk", help="风险扫描")
    risk.add_argument("--code", required=True, help="股票代码")
    risk.add_argument("--date", help="日期 (YYYY-MM-DD)")

    diagnose = subparsers.add_parser("diagnose", help="诊股")
    diagnose.add_argument("--code", required=True, help="股票代码")
    diagnose.add_argument("--scenario", default="诊股", help="场景名称")
    diagnose.add_argument("--horizon", default="短线", help="持仓周期")
    diagnose.add_argument("--risk-preference", default="平衡型", help="风险偏好")
    diagnose.add_argument("--date", help="日期 (YYYY-MM-DD)")

    pick = subparsers.add_parser("pick", help="选股")
    pick.add_argument("--filters", nargs="+", default=["basic", "tech", "catalyst"], help="过滤器")

    pre_market = subparsers.add_parser("pre-market", help="盘前分析")
    pre_market.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日期 (YYYY-MM-DD)")

    post_market = subparsers.add_parser("post-market", help="盘后复盘")
    post_market.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日期 (YYYY-MM-DD)")

    plan = subparsers.add_parser("plan", help="交易计划")
    plan.add_argument("--code", required=True, help="股票代码")
    plan.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日期 (YYYY-MM-DD)")

    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    skill = ASharesSkill()

    if args.command == "self-check":
        payload = skill.self_check()
        print(render_json(payload) if args.format == "json" else render_json(payload))
        return

    if args.command == "risk":
        payload = skill.risk(args.code, args.date)
        print(render_json(payload) if args.format == "json" else render_risk_report(payload))
        return

    if args.command == "diagnose":
        payload = skill.diagnose(args.code, args.scenario, args.horizon, args.risk_preference, args.date)
        print(render_json(payload) if args.format == "json" else render_diagnosis(payload))
        return

    if args.command == "pick":
        filters = normalize_filters(args.filters)
        payload = skill.pick(filters)
        print(render_json(payload) if args.format == "json" else render_stock_picker(payload, filters))
        return

    if args.command == "pre-market":
        payload = skill.pre_market_report(args.date)
        print(render_json(payload) if args.format == "json" else render_pre_market(payload))
        return

    if args.command == "post-market":
        payload = skill.post_market_review(args.date)
        print(render_json(payload) if args.format == "json" else render_post_market(payload))
        return

    if args.command == "plan":
        payload = skill.trading_plan_report(args.code, args.date)
        print(render_json(payload) if args.format == "json" else render_trading_plan(payload))
        return

    parser.error(f"unknown command: {args.command}")


if __name__ == "__main__":
    main()

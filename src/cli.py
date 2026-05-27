"""CLI helpers and renderers."""

from __future__ import annotations

import json
from typing import Iterable


def normalize_filters(values: Iterable[str]) -> list[str]:
    filters: list[str] = []
    for raw in values:
        for item in raw.split(","):
            token = item.strip()
            if token and token not in filters:
                filters.append(token)
    return filters or ["basic", "tech", "catalyst"]


def render_json(payload: object) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def render_risk_report(payload: dict) -> str:
    red_flags = "、".join(payload["red_flags"]) if payload["red_flags"] else "无"
    warnings = "、".join(payload["warnings"]) if payload["warnings"] else "无"
    return (
        f"# 风险扫描 {payload['stock_code']}\n\n"
        f"- 风险等级: {payload['risk_level']}\n"
        f"- 红线项目: {red_flags}\n"
        f"- 警告项目: {warnings}\n"
        f"- 结论: {'可继续跟踪' if payload['is_clear'] else '禁止推荐'}"
    )


def render_stock_picker(candidates: list[dict], filters: list[str]) -> str:
    lines = [
        "# 智能选股报告",
        "",
        f"筛选条件: {', '.join(filters)}",
        "",
        "| 股票 | 代码 | PE | Q1增长 | 风险收益比 | 催化因素 |",
        "|------|------|----|--------|------------|----------|",
    ]
    for item in candidates:
        lines.append(
            f"| {item['name']} | {item['code']} | {item['pe']} | {item['growth_q1']}% | "
            f"{item['risk_reward_ratio']} | {item['catalyst'] or '无'} |"
        )
    if not candidates:
        lines.append("| - | - | - | - | - | 无符合条件标的 |")
    return "\n".join(lines)


def render_diagnosis(payload: dict) -> str:
    rating = payload["rating_4d"]
    conclusion = payload["conclusion"]
    return (
        f"## {payload['stock_code']} 诊断报告\n\n"
        f"- 场景: {payload['needs_clarified']['scenario']}\n"
        f"- 四维评级: {rating['level']}\n"
        f"- 风险等级: {payload['risk']['risk_level']}\n"
        f"- 建议动作: {conclusion['action']}\n"
        f"- 买入价: {conclusion['entry_price']}\n"
        f"- 止损价: {conclusion['stop_loss']}\n"
        f"- 目标价: {conclusion['target_price']}\n"
        f"- 建议仓位: {round(conclusion['position_ratio'] * 100)}%\n"
        f"- 结论: {conclusion['summary']}"
    )


def render_pre_market(payload: dict) -> str:
    return (
        f"# 盘前报告 {payload['date']}\n\n"
        f"- 隔夜情绪: {payload['overnight_sentiment']}\n"
        f"- 政策重点: {'；'.join(payload['policy_highlights'])}\n"
        f"- 昨日遗留: {payload['yesterday_leverage']}\n"
        f"- 乐观剧本: {payload['today_script_optimistic']}\n"
        f"- 悲观剧本: {payload['today_script_pessimistic']}\n"
        f"- 置信度: {payload['confidence']}"
    )


def render_post_market(payload: dict) -> str:
    summary = payload["index_summary"]
    return (
        f"# 盘后复盘 {payload['date']}\n\n"
        f"- 成交额(亿): {summary['成交额(亿)']}\n"
        f"- 涨跌比: {summary['涨跌比']}\n"
        f"- 流动性模式: {summary['流动性模式']}\n"
        f"- 情绪监控: {payload['sentiment_monitor']}\n"
        f"- 核心个股: {'、'.join(payload['key_stocks'])}\n"
        f"- 板块轮动: {payload['sector_rotation']}\n"
        f"- 明日关注: {'；'.join(payload['tomorrow_focus'])}"
    )


def render_trading_plan(payload: dict) -> str:
    return (
        f"# 交易计划 {payload['stock_name']} ({payload['stock_code']})\n\n"
        f"- 日期: {payload['date']}\n"
        f"- 乐观触发: {'；'.join(payload['optimistic_triggers'])}\n"
        f"- 乐观计划: {payload['optimistic_entry']} -> {payload['optimistic_target']} "
        f"(止损 {payload['optimistic_stop_loss']}, 仓位 {round(payload['optimistic_position'] * 100)}%)\n"
        f"- 悲观触发: {'；'.join(payload['pessimistic_triggers'])}\n"
        f"- 风控: 等级 {payload['risk_control']['risk_level']}，红线 {payload['risk_control']['red_flags'] or ['无']}"
    )

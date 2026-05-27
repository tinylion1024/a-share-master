---
name: a-shares-master
description: "Analyze A-share trades with resilient offline workflows."
version: 2.1.0
author: tinylion1024
license: MIT
platforms: [linux, macos]
homepage: https://github.com/tinylion1024/a-share-profit-helper
user-invocable: true
tags: [finance, stocks, a-share, trading]
category: research
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/tinylion1024/a-share-profit-helper","skillKey":"a-shares-master","os":["linux","macos"],"requires":{"bins":["python3"]},"envVars":[{"name":"A_SHARE_SKILL_OFFLINE_MODE","required":false,"description":"Enable offline-first execution."},{"name":"A_SHARE_SKILL_DATA_PATH","required":false,"description":"Path to fixture JSON with market and stock data."},{"name":"IWENCAI_API_KEY","required":false,"description":"Optional live Iwencai credential."},{"name":"MX_APIKEY","required":false,"description":"Optional live MX credential."},{"name":"EM_API_KEY","required":false,"description":"Optional live Eastmoney credential."}]},"hermes":{"category":"research","tags":["finance","stocks","a-share","trading"],"related_skills":["browser","spreadsheets"],"config":{"offline_mode":"A_SHARE_SKILL_OFFLINE_MODE","sample_data_path":"A_SHARE_SKILL_DATA_PATH"}}}
---

# A-Shares Master Skill

This skill produces deterministic A-share `诊股` / `选股` / `风控` / `盘前盘后复盘` output from local fixtures or optional live credentials. It is designed to stay usable when market APIs are absent, rate-limited, or only partially configured.

## When To Use

- The user asks whether a stock can be bought, held, reduced, or avoided.
- The user wants a pre-market view, post-market review, or a two-scenario trading plan.
- The runtime is missing live APIs and the agent still needs a reliable answer from local fixtures.
- The agent must use `terminal` with a single, stable entrypoint that works in both OpenClaw and Hermes-style environments.

## Prerequisites

- Run inside `{baseDir}` or the repository root.
- Python 3.9+ is enough for offline mode.
- Live credentials are optional. See `.env.example` for `IWENCAI_API_KEY`, `MX_APIKEY`, `EM_API_KEY`.
- To override built-in fixtures, point `A_SHARE_SKILL_DATA_PATH` at a JSON file containing `market` and `stocks`.

## How To Run

Prefer the unified entrypoint:

```bash
cd {baseDir}
python3 scripts/run_skill.py self-check
python3 scripts/run_skill.py risk --code 300750
python3 scripts/run_skill.py diagnose --code 300750 --date 2026-05-28
python3 scripts/run_skill.py pick --filters basic,tech,catalyst
python3 scripts/run_skill.py pre-market --date 2026-05-28
python3 scripts/run_skill.py post-market --date 2026-05-28
python3 scripts/run_skill.py plan --code 300750 --date 2026-05-28
```

For machine-readable output:

```bash
python3 scripts/run_skill.py --format json risk --code 300750
```

## Quick Reference

- `terminal`
  Run all commands in this skill through the terminal tool or a shell-capable agent step.
- `scripts/run_skill.py`
  Single agent-friendly entrypoint.
- `src/skill.py`
  Unified facade used by all scripts.
- `src/providers/offline.py`
  Offline-first provider with JSON fixture override support.
- `src/core/`
  Analysis, rating, risk, and workflow logic.
- `scripts/run_tests.sh`
  Runs `pytest` when available, otherwise falls back to `unittest`.

## Procedure

1. Run `python3 scripts/run_skill.py self-check` before using live scenarios.
2. If the user asks for 风控 only, call `risk`.
3. If the user asks for 买/卖/持建议, call `diagnose`.
4. If the user asks for what to buy, call `pick`.
5. If the user needs actionable prices and position sizing, call `plan`.
6. Use `--format json` when another agent or tool will parse the output.
7. If live data is unavailable, stay in offline mode instead of failing hard.

## Pitfalls

- Do not assume live credentials exist; the skill is designed to degrade gracefully.
- Do not call the legacy scripts first; they are thin wrappers around `run_skill.py`.
- Do not treat offline fixture output as live investment advice.
- Do not edit `references/` to change behavior. The executable behavior lives in `src/` and `scripts/`.

## Verification

- Run `python3 scripts/run_skill.py self-check`.
- Run `sh scripts/run_tests.sh`.
- If `pytest` is installed, the same tests should also pass via `python3 -m pytest -q tests`.

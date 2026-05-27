# A股散户盈利助手

一个面向 Agent 的 A 股分析 Skill，目标是用离线优先、可回退的方式输出稳定的 `诊股 / 选股 / 风控 / 盘前盘后复盘 / 交易计划` 结果。

## 当前改造方向

- 统一入口：所有能力收敛到 `scripts/run_skill.py`
- 高可用：默认离线模式，不依赖外部 API 也能返回结构化结果
- 兼容 Agent：`SKILL.md` 采用 OpenClaw / Hermes 都能消费的元数据形式
- 可测试：仓库内置自检和测试脚本

## 快速开始

```bash
python3 scripts/run_skill.py self-check
python3 scripts/run_skill.py risk --code 300750
python3 scripts/run_skill.py diagnose --code 300750 --date 2026-05-28
python3 scripts/run_skill.py pick --filters basic,tech,catalyst
python3 scripts/run_skill.py plan --code 300750 --date 2026-05-28
sh scripts/run_tests.sh
```

## 配置

- 默认离线模式：见 `.env.example`
- 自定义本地样本数据：设置 `A_SHARE_SKILL_DATA_PATH=/path/to/data.json`
- 若接入真实 API，可配置 `IWENCAI_API_KEY`、`MX_APIKEY`、`EM_API_KEY`

## 目录

```text
src/
  config/      统一配置
  core/        分析 / 评级 / 风控 / 工作流
  modules/     盘前、盘后、选股、交易计划
  providers/   离线优先数据层
  skill.py     单一 Skill 入口
scripts/
  run_skill.py 统一 CLI
  run_tests.sh 测试入口
tests/
  skills/      技能兼容性和行为测试
```

## 说明

当前版本重点解决的是“Skill 可运行、可验证、可在多 Agent 环境降级工作”。真实行情 API 的更深接入仍可继续往这个骨架上补。

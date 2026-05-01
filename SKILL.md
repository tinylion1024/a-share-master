---
name: a-shares-master
description: |
  A股综合分析系统：集成"新闻/政策、社交情绪、市场流动性、显性风险"四维分析。

  核心能力：
  - 四维评级选股（机会/安全/确定/舒适）
  - 15场景SOP（选股/诊股/复盘等）
  - 盘前报告/盘后复盘/交易计划
  - 高PR股票筛选
  - 风险合规检查

  触发：选股、诊股、买股、卖股、复盘、大盘分析、仓位管理、止损止盈

depends_on: depends_on.yml

env:
  - MX_APIKEY
  - EM_API_KEY
  - IWENCAI_BASE_URL
  - IWENCAI_API_KEY
---

# A股全能策略专家 (A-Shares Master)

> 帮散户赚钱，以「复利增长」为北极星目标

---

## 核心体系

```
三维看市场：消息 ── 情绪 ── 技术
四维选股级：机会 ── 安全 ── 确定 ── 舒适
```

---

## 能力模块

| 模块 | 说明 |
|------|------|
| `src/modules/pre_market.py` | 盘前报告生成 |
| `src/modules/post_market.py` | 盘后复盘分析 |
| `src/modules/stock_picker.py` | 高PR选股系统 |
| `src/modules/trading_plan.py` | 双剧本交易计划 |
| `src/core/analyzer.py` | 综合分析引擎 |
| `src/core/rating.py` | 四维评级系统 |
| `src/core/risk_checker.py` | 风险合规检查 |
| `src/core/pipeline.py` | 工作流编排 |

---

## 标准工作流

```
用户问"能买吗XXX"
        │
        ▼
┌───────────────────┐
│ Step 0: 需求澄清   │
│   分析类型/周期/偏好 │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Step 1: 三维看市场 │
│   消息/情绪/技术    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Step 2: 四维选股   │
│   机会/安全/确定/舒适│
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Step 3: 输出结论   │
│   买入价+止损价+目标价│
│   + 置信度+仓位     │
└───────────────────┘
```

---

## Step 0：需求澄清 + 场景识别

### 场景识别

| 用户需求 | 场景 | SOP |
|----------|------|-----|
| **赚钱引擎** | | |
| 不知道买什么 | 选股 | [references/flow/make-money/stock-picker.md](references/flow/make-money/stock-picker.md) |
| 纠结买不买 | 诊股 | [references/flow/make-money/stock-diagnosis.md](references/flow/make-money/stock-diagnosis.md) |
| 纠结卖不卖 | 持仓诊断 | [references/flow/make-money/position-diagnosis.md](references/flow/make-money/position-diagnosis.md) |
| 被套了 | 解套 | [references/flow/make-money/unstuck.md](references/flow/make-money/unstuck.md) |
| 亏多少必须走 | 止损 | [references/flow/make-money/stop-loss.md](references/flow/make-money/stop-loss.md) |
| 赚多少要跑 | 止盈 | [references/flow/make-money/take-profit.md](references/flow/make-money/take-profit.md) |
| **学习引擎** | | |
| 今天怎么看 | 大盘前瞻 | [references/flow/learn/market-outlook.md](references/flow/learn/market-outlook.md) |
| 为什么涨/跌 | 大盘总结 | [references/flow/learn/market-summary.md](references/flow/learn/market-summary.md) |
| 操作对吗 | 每日复盘 | [references/flow/learn/daily-review.md](references/flow/learn/daily-review.md) |
| 为什么涨/跌 | 案例拆解 | [references/flow/learn/case-analysis.md](references/flow/learn/case-analysis.md) |
| 为什么亏 | 错误反思 | [references/flow/learn/error-reflection.md](references/flow/learn/error-reflection.md) |
| 怎么赚到的 | 经验沉淀 | [references/flow/learn/experience.md](references/flow/learn/experience.md) |
| **进化引擎** | | |
| 记录这笔 | 案例记录 | [references/flow/evolve/case-record.md](references/flow/evolve/case-record.md) |
| 更新规则 | 规律更新 | [references/flow/evolve/rule-update.md](references/flow/evolve/rule-update.md) |
| 调整参数 | 模型优化 | [references/flow/evolve/model-tune.md](references/flow/evolve/model-tune.md) |

### 必要信息确认

| 问题 | 选项 |
|------|------|
| 持仓周期？ | 短线(5日) / 中线(20日) / 长线(60日) |
| 风险偏好？ | 保守型 / 平衡型 / 激进型 |

> 详细SOP：[references/flow/README.md](references/flow/README.md)

---

## Step 1：三维看市场

| 维度 | 分析内容 |
|------|---------|
| **消息** | 政策、宏观、行业、公司公告 |
| **情绪** | 散户情绪、大V观点、游资动向（TGB热度） |
| **技术** | 趋势、均线、成交量、MACD |

**信号组合：**

| 信号 | 市场判断 | 操作 |
|---------|---------|------|
| 🟢🟢🟢 | 强势上涨 | 积极做多 |
| 🟢🟡🟢 | 震荡偏强 | 精选个股 |
| 🟡🟡🟡 | 震荡整理 | 高抛低吸 |
| 🔴🔴🔴 | 弱势下跌 | 休息/空仓 |

> 详细：[references/core/four-dimensions.md](references/core/four-dimensions.md)

---

## Step 2：四维选股评级

| 维度 | 星级 | 说明 |
|------|------|------|
| **机会⭐** | 1-5 | 上涨空间与概率 |
| **安全⭐** | 1-5 | 风险程度（R3红线） |
| **确定⭐** | 1-5 | 上涨逻辑清晰度 |
| **舒适⭐** | 1-5 | 持有体验（位置/波动） |

**决策树：**
```
安全⭐ < 3 → 不买（R3红线）
安全⭐≥3 + 机会⭐≥3 + 确定⭐≥3 → 可以买
```

**综合评级：**
```
综合分 = 机会⭐×30% + 安全⭐×25% + 确定⭐×25% + 舒适⭐×20%

4.5+ → ⭐⭐⭐⭐⭐ 立即买
3.5+ → ⭐⭐⭐⭐ 可以买
2.5+ → ⭐⭐⭐ 观望
```

> 详细：[references/core/rating/](references/core/rating/)

---

## Step 3：输出结论

| 必备内容 | 示例 |
|---------|------|
| 买入价 | XX.XX，突破确认后介入 |
| 止损价 | XX.XX，跌破必须走 |
| 目标价 | XX.XX，止盈参考 |
| 置信度 | 高/中/低 + 理由 |
| 仓位建议 | 首仓X成、最大X成 |

**标准格式：**

```markdown
## [股票] 诊断报告

**评级**：⭐⭐⭐⭐ | **置信度**：中高
**三维**：消息🟢 情绪🟢 技术🟢
**四维**：机会4 安全4 确定5 舒适3

| 参数 | 价位 | 说明 |
|------|------|------|
| 买入价 | XX.XX | 突破确认后介入 |
| 止损价 | XX.XX | 跌破必须走 |
| 目标价 | XX.XX | 止盈参考 |
| 仓位 | X成 | 不超过总仓位X成 |

*本报告仅供参考，不构成投资建议*
```

---

## 🚫 硬规则

违反以下任一规则，直接取消资格：

| # | 规则 | 原因 |
|---|------|------|
| 1 | **R3红线** | 安全⭐<3 禁止推荐 |
| 2 | **止损7%** | 不执行止损是亏损主因 |
| 3 | **T+1** | 当日买不可卖 |
| 4 | **流动性** | 成交额<5000万不做主要标的 |
| 5 | **仓位** | 单只≤30%，总≤50% |
| 6 | **Disclaimer** | 必须注明仅供参考 |

> 详细：[references/guides/rules.md](references/guides/rules.md)

---

## 🔄 反馈循环

```
操作执行 → 结果收集 → 学习更新
     ↑                        ↓
     └──── 案例积累 ←→ 规则优化
```

> 详细：[references/core/feedback-loop.md](references/core/feedback-loop.md)

---

## 📑 文档索引

| 文档 | 内容 |
|------|------|
| [references/flow/README.md](references/flow/README.md) | 15场景SOP索引 |
| [references/core/rating/](references/core/rating/) | 四维评分详解 |
| [references/core/four-dimensions.md](references/core/four-dimensions.md) | 三维分析详解 |
| [references/core/tgb-sentiment.md](references/core/tgb-sentiment.md) | TGB情绪分析 |
| [references/guides/rules.md](references/guides/rules.md) | 硬规则详解 |
| [references/guides/data-sources.md](references/guides/data-sources.md) | 数据源指南 |
| [references/guides/scenes.md](references/guides/scenes.md) | 场景体系 |
| [references/guides/anchors.md](references/guides/anchors.md) | 买卖锚点 |
| [references/install.md](references/install.md) | 安装指南 |

---

## ⚡ 快速命令

```bash
# 风控扫描
python3 scripts/check_risk.py --code 300750

# 选股筛选
python3 scripts/stock_picker.py --filters basic,tech

# 交易计划
python3 scripts/trading_plan.py --stock 300750

# 市场分析
python3 scripts/market_analysis.py
```

---

## 吸收的子能力

以下能力已从独立skill合并到本skill：

| 原Skill | 能力 | 整合位置 |
|---------|------|---------|
| `a-share-integrated-expert` | 四维分析+舒适度判定 | `src/core/rating.py` |
| `a-share-v2-analyzer` | 天量行情分析 | `src/core/analyzer.py` |
| `a-share-daily-pre-opening-report` | 盘前报告 | `src/modules/pre_market.py` |
| `a-share-market-synthesis` | 开盘哨站+复盘 | `src/modules/post_market.py` |
| `a-share-detailed-reviewer` | 每日复盘 | `src/modules/post_market.py` |
| `high-pr-stock-picker` | 高PR选股 | `src/modules/stock_picker.py` |
| `trading-plan-generator` | 双剧本交易计划 | `src/modules/trading_plan.py` |
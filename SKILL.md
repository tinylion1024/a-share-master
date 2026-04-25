---
name: a-share-profit-helper
description: |
  A股散户盈利助手，专注帮助散户赚钱、复利增长。

  触发：选股、诊股、买股、卖股、复盘、大盘分析、仓位管理、止损止盈
  不适用：美股、港股、期货、期权、量化策略

depends_on:
  - akshare-stock           # A股数据
  - mx-finance-data         # 财务数据
  - mx-macro-data          # 宏观数据
  - mx-stocks-screener     # 选股筛选
  - mx-finance-search       # 市场搜索
  - mx-financial-assistant  # 问答助手
  - stock-diagnosis        # 股票诊断
  - stock-earnings-review   # 业绩点评
  - industry-stock-tracker  # 行业追踪
  - taoguba-hot           # 社区情绪
  - open-gstack-browser   # 浏览器工具

env:
  - MX_APIKEY
  - EM_API_KEY
---

# A股散户盈利助手

> 帮散户赚钱，以「复利增长」为北极星目标

---

## 核心体系

```
三维看市场：消息 ── 情绪 ── 技术
四维选股级：机会 ── 安全 ── 确定 ── 舒适
```

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

## Step 0：需求澄清

| 问题 | 选项 |
|------|------|
| 分析类型？ | 买入前 / 持仓诊断 |
| 持仓周期？ | 短线(5日) / 中线(20日) / 长线(60日) |
| 风险偏好？ | 保守型 / 平衡型 / 激进型 |

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
| [references/core/rating/](references/core/rating/) | 四维评分详解 |
| [references/core/four-dimensions.md](references/core/four-dimensions.md) | 三维分析详解 |
| [references/core/tgb-sentiment.md](references/core/tgb-sentiment.md) | TGB情绪分析 |
| [references/guides/rules.md](references/guides/rules.md) | 硬规则详解 |
| [references/guides/scenes.md](references/guides/scenes.md) | 场景体系 |
| [references/guides/anchors.md](references/guides/anchors.md) | 买卖锚点 |
| [references/install.md](references/install.md) | 安装指南 |

---

## ⚡ 快速命令

```bash
python3 scripts/config_manager.py   # 配置向导
python3 scripts/check_risk.py --code 300750  # 风控扫描
python3 scripts/stock_picker.py --filters basic,tech  # 选股
python3 scripts/trading_plan.py --stock 300750  # 交易计划
```

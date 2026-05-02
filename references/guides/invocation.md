# 调用链路指南

> 用户问法 → 场景 → SOP → 子skill 的完整映射

---

## 场景触发表

| 用户问法关键词 | 场景 | 对应SOP | 主调skill |
|--------------|------|---------|----------|
| **选股** | | | |
| "有什么能赚钱" | 选股 | [flow/make-money/stock-picker.md](../flow/make-money/stock-picker.md) | mx-stocks-screener, mx-finance-data |
| "推荐股票" | 选股 | 同上 | mx-stocks-screener |
| "高PR选股" | 选股 | 同上 | mx-stocks-screener |
| **诊股** | | | |
| "能买XXX吗" | 诊股 | [flow/make-money/stock-diagnosis.md](../flow/make-money/stock-diagnosis.md) | market-data-query, check_risk |
| "帮我看看XXX" | 诊股 | 同上 | market-data-query |
| "XXX怎么样" | 诊股 | 同上 | market-data-query |
| "XXX可以买入吗" | 诊股 | 同上 | market-data-query |
| **持仓诊断** | | | |
| "XXX还能持有吗" | 持仓诊断 | [flow/make-money/position-diagnosis.md](../flow/make-money/position-diagnosis.md) | market-data-query |
| "帮我看看持仓" | 持仓诊断 | 同上 | market-data-query |
| **解套** | | | |
| "XXX被套了" | 解套 | [flow/make-money/unstuck.md](../flow/make-money/unstuck.md) | market-data-query, mx-finance-data |
| "能解套吗" | 解套 | 同上 | market-data-query |
| **止损** | | | |
| "亏多少必须走" | 止损 | [flow/make-money/stop-loss.md](../flow/make-money/stop-loss.md) | market-data-query |
| "止损怎么设" | 止损 | 同上 | market-data-query |
| **止盈** | | | |
| "赚多少要跑" | 止盈 | [flow/make-money/take-profit.md](../flow/make-money/take-profit.md) | market-data-query |
| "止盈怎么设" | 止盈 | 同上 | market-data-query |
| **大盘分析** | | | |
| "今天怎么看" | 大盘前瞻 | [flow/learn/market-outlook.md](../flow/learn/market-outlook.md) | index-data-query, macro-data-query |
| "大盘怎么样" | 大盘前瞻 | 同上 | index-data-query |
| **复盘** | | | |
| "操作对吗" | 每日复盘 | [flow/learn/daily-review.md](../flow/learn/daily-review.md) | market-data-query, announcement-search |
| "今天复盘" | 每日复盘 | 同上 | market-data-query |
| **案例分析** | | | |
| "为什么涨" | 案例拆解 | [flow/learn/case-analysis.md](../flow/learn/case-analysis.md) | news-search, announcement-search |
| "为什么跌" | 案例拆解 | 同上 | news-search, announcement-search |
| **错误反思** | | | |
| "为什么亏" | 错误反思 | [flow/learn/error-reflection.md](../flow/learn/error-reflection.md) | market-data-query |
| **经验沉淀** | | | |
| "怎么赚到的" | 经验沉淀 | [flow/learn/experience.md](../flow/learn/experience.md) | - |
| **案例记录** | | | |
| "记录这笔" | 案例记录 | [flow/evolve/case-record.md](../flow/evolve/case-record.md) | - |
| **规则更新** | | | |
| "更新规则" | 规律更新 | [flow/evolve/rule-update.md](../flow/evolve/rule-update.md) | - |
| **模型调优** | | | |
| "调整参数" | 模型优化 | [flow/evolve/model-tune.md](../flow/evolve/model-tune.md) | - |

---

## 场景 → SOP 执行流程

### 选股场景（stock-picker）

```
用户：想赚钱 → 触发选股
  │
  ▼
[Step 0] 澄清需求 → 持仓周期/风险偏好/仓位上限
  │
  ▼
[Step 1] 三维看市场 → 判断大盘环境是否适合选股
  │         调用：index-data-query, macro-data-query
  │
  ▼
[Step 2] 三重过滤筛选
  │         调用：mx-stocks-screener → 基本面+趋势+流动性
  │         调用：mx-finance-data → 技术位提取
  │         调用：mx-financial-assistant → 催化剂合成
  │
  ▼
[Step 3] 四维评级 → 机会/安全/确定/舒适
  │
  ▼
[Step 4] R3红线过滤 → 安全⭐<3 直接排除
  │
  ▼
输出：选股报告（推荐标的+理由+买入/止损/目标价+仓位）
```

### 诊股场景（stock-diagnosis）

```
用户：能买XXX吗 → 触发诊股
  │
  ▼
[Step 0] 确认股票代码/持仓周期/买入预算
  │
  ▼
[Step 1] 环境自检 → MX_APIKEY/EM_API_KEY + 流动性扫描
  │         调用：market-analysis.py
  │
  ▼
[Step 2] R3风险扫描（必须先过）
  │         调用：check_risk.py --code XXX
  │         触发 → 输出"不买"，结束
  │
  ▼
[Step 3] 日期对齐 → 严禁混淆"昨日异动"与"今日实时"
  │
  ▼
[Step 4] 三维看市场 → 消息/情绪/技术信号组合
  │
  ▼
[Step 5] 四维评级 → 机会/安全/确定/舒适
  │
  ▼
[Step 6] 买入舒适度判定
  │
  ▼
输出：诊股报告（结论+三维+四维+买入价/止损价/目标价/仓位）
```

---

## 数据获取优先级

### 硬数据（必须用官方/Iwencai）

| 数据类型 | 首选 | 备选1 | 备选2 |
|----------|------|--------|--------|
| 行情数据 | Iwencai(market-data-query) | MX(mx-data) | AkShare |
| 财务数据 | Iwencai(financial-data-query) | MX(mx-finance-data) | 公司公告 |
| 选股筛选 | Iwencai(a-share-screener) | MX(mx-stocks-screener) | AkShare |
| 研报新闻 | Iwencai(news-search) | MX(mx-finance-search) | 交易所 |
| 资金流向 | Iwencai(market-data-query) | MX(mx-finance-data) | AkShare |

### 软数据（可参考社区）

| 数据类型 | 来源 |
|----------|------|
| 情绪热度 | taoguba-hot |
| 大V观点 | 雪球、微博（需交叉验证） |

---

## 子skill调用规范

### 调用格式

```markdown
## [场景] 调用链

### 1. 数据获取
调用：market-data-query
输入：股票代码 + 日期
输出：行情数据（股价/成交量/均线）

### 2. 风险扫描
调用：stock-diagnosis 或 check_risk
输入：股票代码
输出：R3风险判定

### 3. 综合分析
调用：mx-financial-assistant 或 mx-finance-data
输入：分析目标 + 数据
输出：结论 + 建议
```

### 常用skill清单

| skill | 用途 |
|-------|------|
| `market-data-query` | 行情数据（股价/成交量/均线） |
| `mx-stocks-screener` | 选股筛选 |
| `mx-finance-data` | 财务数据 + 技术位 |
| `mx-finance-search` | 市场搜索（新闻/公告/研报） |
| `mx-financial-assistant` | 智能问答（合成分析） |
| `check_risk` | R3风险扫描 |
| `taoguba-hot` | 社区情绪热度 |
| `akshare-stock` | AkShare行情（备选） |

---

## 输出规范

所有场景输出必须包含：

```markdown
## [场景] 报告

**数据来源**：Iwencai(market-data-query) + MX(mx-finance-data)
**更新时间**：YYYY-MM-DD HH:MM:SS

[具体内容...]

*本报告仅供参考，不构成投资建议*
```

---

## 关联文档

- [data-sources.md](./data-sources.md) — 数据源完整指南
- [rules.md](./rules.md) — 硬规则（R3红线/止损7%/T+1/仓位）
- [scenes.md](./scenes.md) — 场景体系详解
- [anchors.md](./anchors.md) — 买卖锚点
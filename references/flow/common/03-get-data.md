# 公共SOP 3：获取可信数据

> 从可靠来源获取分析所需数据

---

## 目的

确保数据来源可靠，避免使用错误/过时数据。

---

## 数据源分级

| 级别 | 来源 | 可靠性 | 用途 |
|------|------|--------|------|
| **官方** | 交易所、东方财富、同花顺 | ⭐⭐⭐⭐⭐ | 行情、公告、财务 |
| **Iwencai** | 问财API（需配置API_KEY） | ⭐⭐⭐⭐⭐ | 选股、财务、研报、新闻 |
| **准官方** | Wind、Choice | ⭐⭐⭐⭐⭐ | 机构数据 |
| **社区** | 淘股吧、雪球 | ⭐⭐⭐ | 情绪、观点 |
| **小众** | 股吧、消息群 | ⭐⭐ | 仅作提醒，慎用 |

---

## 操作步骤

### Step 1：确定需要的数据

根据场景确定需要哪些数据：

| 场景 | 必需数据 | 推荐数据源 |
|------|----------|------------|
| 选股 | 行情、成交量、趋势、财务 | Iwencai(A股选股) + AkShare |
| 诊股 | 行情、R3风险、四维评分 | Iwencai(行情) + AkShare |
| 持仓诊断 | 行情，成本价、盈亏 | Iwencai(行情) + AkShare |
| 大盘分析 | 指数、成交额，资金流向 | Iwencai(指数) + AkShare |
| 复盘 | 当日所有行情数据 | Iwencai(行情) + AkShare |

---

### Step 2：获取三类必要数据

#### 3.1 数据优先级（Fallback链）

```
问财SKILL > MX（妙想）API > AkShare
```

#### 3.2 三类必要数据

**A. 市场技术数据**

| 数据项 | 首选 | 备选1 | 备选2 |
|--------|------|--------|--------|
| 实时行情 | Iwencai(market-data-query) | MX(mx-data) | AkShare |
| 股价/涨跌 | Iwencai(market-data-query) | MX(mx-data) | AkShare |
| 成交量/额 | Iwencai(market-data-query) | MX(mx-data) | AkShare |
| 均线/MA | Iwencai(market-data-query) | MX(mx-data) | AkShare |
| 指数数据 | Iwencai(index-data-query) | MX(mx-data) | AkShare |
| 板块行情 | Iwencai(sector-screener) | MX(mx-data) | AkShare |
| 资金流向 | Iwencai(market-data-query) | MX(mx-data) | AkShare |

**B. 消息新闻数据**

| 数据项 | 首选 | 备选1 | 备选2 |
|--------|------|--------|--------|
| 实时新闻 | Iwencai(news-search) | MX(mx-finance-search) | - |
| 公告 | Iwencai(announcement-search) | MX(mx-finance-search) | 交易所 |
| 研报 | Iwencai(research-report-search) | MX(mx-finance-search) | - |
| 宏观政策 | Iwencai(macro-data-query) | MX(mx-macro-data) | - |
| 行业数据 | Iwencai(industry-data-query) | MX(mx-macro-data) | - |
| 事件数据 | Iwencai(event-data-query) | MX(mx-finance-search) | - |

**C. 情绪文本数据**

| 数据项 | 来源 | 说明 |
|--------|------|------|
| TGB热度 | taoguba-hot | 淘股吧热门帖子情绪 |
| V观点 | taoguba-hot | 大V观点提取 |
| 社区情绪 | 雪球、微博 | 需交叉验证 |

---

### Step 3：数据校验

**三重校验：**

1. **来源校验**：数据来自≥2个独立源
2. **逻辑校验**：涨幅 = (收盘价 - 昨收) / 昨收
3. **异常校验**：偏离历史均值>30%需复核

### Step 4：标注数据来源

```markdown
【数据来源】
行情数据：Iwencai(market-data-query)
财务数据：Iwencai(financial-data-query)
消息数据：Iwencai(news-search/announcement-search)
情绪数据：淘股吧热度
更新时间：YYYY-MM-DD HH:MM:SS
数据时效：<5分钟/当日有效/历史数据
```

---

## 数据时效性

| 数据类型 | 接受时效 | 超时处理 |
|----------|----------|----------|
| 实时行情 | <5分钟 | 降级参考 |
| 今日成交 | <15分钟 | 降级参考 |
| 公告/新闻 | <24小时 | 标记时间戳 |
| 财务数据 | 最新一期 | 使用季报/年报 |
| 历史数据 | 无限制 | 可用 |

---

## 常见错误

| 错误 | 后果 | 正确做法 |
|------|------|----------|
| 用单一来源 | 数据可能有误 | 多源交叉验证 |
| 用过时数据 | 判断失误 | 检查时间戳 |
| 用小众来源 | 虚假信息 | 优先官方/Iwencai |
| 缺情绪数据 | 维度不全 | 补充TGB热度 |

---

## 关联SOP

- 公共SOP 1：[01-clarify-needs.md](01-clarify-needs.md)
- 公共SOP 2：[02-define-time-window.md](02-define-time-window.md)
- 详细规则：[references/guides/data-sources.md](../../guides/data-sources.md)

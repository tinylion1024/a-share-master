# 高 PR 选股 (High PR Stock Picker)

## 三重过滤器链

### Step 1: 基本面、趋势、流动性筛选

使用 `mx-stocks-screener` 筛选处于上升趋势且高流动性的股票：

```bash
python3 get_data.py \
  --query "股价在20日均线上方，且成交额排名前50，市盈率<40的A股" \
  --select-type A股
```

> 高换手率确保趋势有大量资金支撑，提高支撑位的可靠性

### Step 2: 技术数据提取

使用 `mx-finance-data` 提取具体技术位（MA20、BOLL 等）：

```bash
python3 get_data.py "查询 [股票代码] 的最新股价、20日均线位置及BOLL轨道"
```

### Step 3: 情报合成与计划

使用 `mx-financial-assistant` 结合技术数据与近期催化剂：

```bash
python3 generate_answer.py \
  --query "分析 [个股] 的高盈亏比机会。结合：1. [近期事件/催化剂]；2. 一季度业绩；3. 20日均线支撑。给出买入/目标/止损建议。" \
  --deep-think
```

## 选股标准

| 维度 | 标准 |
|------|------|
| 基本面 | PE < 25（或行业平均），Q1/年度增长 > 20% |
| 技术面 | 价格在 20/60 日均线的 2-3% 范围内 |
| 催化剂 | 必须有明确"上涨理由"（政策、供应链断供、全球同行带动） |
| 风险收益 | 目标收益 ≥ 3 × 止损距离 |

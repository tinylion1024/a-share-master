# 安装指南

## 环境要求

- Python 3.8+
- Node.js 16+（部分依赖需要）
- 网络能访问东方财富、淘股吧等国内站点

---

## 依赖 Skill 安装

### 自动安装

使用 `/install` 命令安装所有依赖：

```bash
# 数据获取类
/install akshare-stock          # A股 AkShare 数据
/install mx-finance-data        # 财务数据
/install mx-macro-data          # 宏观数据

# 选股分析类
/install mx-stocks-screener     # 智能选股
/install stock-earnings-review   # 业绩点评
/install industry-stock-tracker  # 行业/个股追踪
/install initiation-of-coverage-or-deep-dive  # 个股首次覆盖/深度研究

# 研究报告类
/install industry-research-report       # 行业研究
/install topic-research-report         # 专题深度研究
/install comparable-company-analysis   # 可比公司分析

# 问答诊断类
/install mx-financial-assistant       # 妙想问答助手
/install stock-diagnosis              # 股票综合诊断
/install fund-diagnosis               # 基金综合诊断
/install stock-market-hotspot-discovery # 热点发现

# 搜索类
/install mx-finance-search       # 市场搜索

# 浏览器工具
/install open-gstack-browser    # 浏览器工具
```

### 手动克隆

如果 `/install` 命令不可用，手动克隆到 `~/.claude/skills/`：

```bash
mkdir -p ~/.claude/skills

# 克隆各依赖 skill
git clone https://github.com/tinylion1024/akshare-stock.git ~/.claude/skills/akshare-stock
git clone https://github.com/tinylion1024/mx-finance-data.git ~/.claude/skills/mx-finance-data
git clone https://github.com/tinylion1024/mx-macro-data.git ~/.claude/skills/mx-macro-data
git clone https://github.com/tinylion1024/mx-stocks-screener.git ~/.claude/skills/mx-stocks-screener
git clone https://github.com/tinylion1024/stock-earnings-review.git ~/.claude/skills/stock-earnings-review
git clone https://github.com/tinylion1024/industry-stock-tracker.git ~/.claude/skills/industry-stock-tracker
git clone https://github.com/tinylion1024/initiation-of-coverage-or-deep-dive.git ~/.claude/skills/initiation-of-coverage-or-deep-dive
git clone https://github.com/tinylion1024/industry-research-report.git ~/.claude/skills/industry-research-report
git clone https://github.com/tinylion1024/topic-research-report.git ~/.claude/skills/topic-research-report
git clone https://github.com/tinylion1024/comparable-company-analysis.git ~/.claude/skills/comparable-company-analysis
git clone https://github.com/tinylion1024/mx-financial-assistant.git ~/.claude/skills/mx-financial-assistant
git clone https://github.com/tinylion1024/stock-diagnosis.git ~/.claude/skills/stock-diagnosis
git clone https://github.com/tinylion1024/fund-diagnosis.git ~/.claude/skills/fund-diagnosis
git clone https://github.com/tinylion1024/stock-market-hotspot-discovery.git ~/.claude/skills/stock-market-hotspot-discovery
git clone https://github.com/tinylion1024/mx-finance-search.git ~/.claude/skills/mx-finance-search
git clone https://github.com/tinylion1024/open-gstack-browser.git ~/.claude/skills/open-gstack-browser
```

---

## 依赖 Skill 清单

| Skill | 功能 | 必需 |
|-------|------|------|
| **akshare-stock** | A股 AkShare 数据 | 核心 |
| **mx-finance-data** | 财务数据 | 核心 |
| **mx-macro-data** | 宏观数据 | 核心 |
| **mx-stocks-screener** | 智能选股 | 核心 |
| **mx-finance-search** | 市场搜索 | 核心 |
| **mx-financial-assistant** | 妙想问答助手 | 核心 |
| **stock-diagnosis** | 股票综合诊断 | 核心 |
| **stock-earnings-review** | 业绩点评 | 推荐 |
| **industry-stock-tracker** | 行业/个股追踪 | 推荐 |
| **initiation-of-coverage-or-deep-dive** | 个股首次覆盖/深度研究 | 推荐 |
| **industry-research-report** | 行业研究 | 推荐 |
| **topic-research-report** | 专题深度研究 | 推荐 |
| **fund-diagnosis** | 基金综合诊断 | 可选 |
| **stock-market-hotspot-discovery** | 热点发现 | 可选 |
| **comparable-company-analysis** | 可比公司分析 | 可选 |
| **open-gstack-browser** | 浏览器工具 | 必需 |

---

## 环境变量配置

### API 密钥获取

> 首次运行时系统会询问，以下提前配置可跳过运行时询问

| 服务 | 获取地址 | 说明 |
|------|---------|------|
| MX API | https://mx.com | 量化数据 API |
| EM API | https://eastmoney.com | 东方财富 API |

### 配置方式

**方式一：运行时询问（推荐）**

首次运行任意脚本时会自动触发配置向导：

```bash
python3 scripts/check_risk.py --code 300750
```

向导会询问：
- MX API 密钥
- EM API 密钥
- 用户昵称
- 投资风格（保守/平衡/激进）
- 筛选偏好

**方式二：手动配置**

```bash
# 复制配置模板
cp config.json.example config.json

# 编辑 config.json 填入密钥
```

```json
{
  "env": {
    "mx_apikey": "your_mx_apikey",
    "em_apikey": "your_em_apikey"
  }
}
```

---

## 依赖检查

安装完成后验证：

```bash
for skill in \
  akshare-stock \
  mx-finance-data \
  mx-macro-data \
  mx-stocks-screener \
  mx-finance-search \
  mx-financial-assistant \
  stock-diagnosis \
  stock-earnings-review \
  industry-stock-tracker \
  initiation-of-coverage-or-deep-dive \
  industry-research-report \
  topic-research-report \
  fund-diagnosis \
  stock-market-hotspot-discovery \
  comparable-company-analysis \
  open-gstack-browser; do
  if [ -d "$HOME/.claude/skills/$skill" ]; then
    echo "✅ $skill"
  else
    echo "❌ $skill - 未安装"
  fi
done
```

期望输出：

```
✅ akshare-stock
✅ mx-finance-data
✅ mx-macro-data
✅ mx-stocks-screener
✅ mx-finance-search
✅ mx-financial-assistant
✅ stock-diagnosis
✅ stock-earnings-review
✅ industry-stock-tracker
✅ initiation-of-coverage-or-deep-dive
✅ industry-research-report
✅ topic-research-report
✅ fund-diagnosis
✅ stock-market-hotspot-discovery
✅ comparable-company-analysis
✅ open-gstack-browser
```

---

## Python 依赖

```bash
pip install pandas akshare requests
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

---

## 常见问题

### Q: /install 命令无效？

确保 Claude Code 版本支持 `/install` 命令，或使用手动克隆方式。

### Q: 浏览器工具无法使用？

确保已安装 `open-gstack-browser`，并配置好浏览器驱动。

### Q: 报错 "No module named 'akshare'"？

执行 `pip install akshare` 安装 Python 依赖。

---

## 验证安装

```bash
# 测试配置向导
python3 scripts/config_manager.py

# 测试风控扫描
python3 scripts/check_risk.py --code 300750

# 测试市场分析
python3 scripts/market_analysis.py
```

无报错即安装成功。

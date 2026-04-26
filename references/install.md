# 安装指南

## 环境要求

- Python 3.8+
- Node.js 16+（部分依赖需要）
- 网络能访问东方财富、淘股吧等国内站点

---

## 依赖 Skill 安装

### 1. Iwencai SkillHub CLI

Iwencai 数据源需要先安装 CLI：

```bash
# 下载安装脚本
curl -sSL https://www.iwencai.com/skillhub/static/0.0.4/download_and_install.sh | bash

# 添加到 PATH（如果未自动添加）
export PATH="$HOME/.local/bin:$PATH"
```

### 2. Iwencai Skill 安装

安装 Iwencai 数据源技能：

```bash
export PATH="$HOME/.local/bin:$PATH"

# 安装16个Iwencai技能
iwencai-skillhub-cli install market-data-query          # 行情数据
iwencai-skillhub-cli install financial-data-query      # 财务数据
iwencai-skillhub-cli install a-share-screener         # A股选股
iwencai-skillhub-cli install sector-screener          # 板块选股
iwencai-skillhub-cli install research-report-search    # 研报搜索
iwencai-skillhub-cli install announcement-search       # 公告搜索
iwencai-skillhub-cli install news-search             # 新闻搜索
iwencai-skillhub-cli install macro-data-query         # 宏观数据
iwencai-skillhub-cli install industry-data-query       # 行业数据
iwencai-skillhub-cli install event-data-query       # 事件数据
iwencai-skillhub-cli install basic-info-query         # 基本资料
iwencai-skillhub-cli install index-data-query         # 指数数据
iwencai-skillhub-cli install convertible-bond-screener  # 可转债选股
iwencai-skillhub-cli install etf-screener            # ETF选股
iwencai-skillhub-cli install fund-screener           # 基金选股
iwencai-skillhub-cli install futures-options-data-query  # 期货期权
```

### 3. MX/AkShare Skill 安装

使用 `/install` 命令安装：

```bash
# AkShare数据
/install akshare-stock

# MX妙想数据
/install mx-finance-data        # 财务数据
/install mx-macro-data          # 宏观数据
/install mx-stocks-screener     # 智能选股
/install mx-finance-search       # 市场搜索
/install mx-financial-assistant  # 妙想问答助手

# 诊断类
/install stock-diagnosis              # 股票综合诊断
/install stock-earnings-review        # 业绩点评
/install industry-stock-tracker       # 行业/个股追踪

# 研究类
/install industry-research-report       # 行业研究
/install topic-research-report         # 专题深度研究
/install initiation-of-coverage-or-deep-dive  # 个股深度研究

# 情绪类
/install taoguba-hot           # 社区情绪

# 浏览器工具
/install open-gstack-browser   # 浏览器工具
```

### 4. 手动克隆（备选）

如果 `/install` 命令不可用：

```bash
mkdir -p ~/.claude/skills

# Iwencai（需先安装CLI）
# Iwencai CLI自动安装到 ~/.iwencai-skillhub/

# MX/AkShare
git clone https://github.com/tinylion1024/akshare-stock.git ~/.claude/skills/akshare-stock
git clone https://github.com/tinylion1024/mx-finance-data.git ~/.claude/skills/mx-finance-data
git clone https://github.com/tinylion1024/mx-macro-data.git ~/.claude/skills/mx-macro-data
git clone https://github.com/tinylion1024/mx-stocks-screener.git ~/.claude/skills/mx-stocks-screener
git clone https://github.com/tinylion1024/mx-finance-search.git ~/.claude/skills/mx-finance-search
git clone https://github.com/tinylion1024/mx-financial-assistant.git ~/.claude/skills/mx-financial-assistant
git clone https://github.com/tinylion1024/stock-diagnosis.git ~/.claude/skills/stock-diagnosis
git clone https://github.com/tinylion1024/stock-earnings-review.git ~/.claude/skills/stock-earnings-review
git clone https://github.com/tinylion1024/industry-stock-tracker.git ~/.claude/skills/industry-stock-tracker
git clone https://github.com/tinylion1024/industry-research-report.git ~/.claude/skills/industry-research-report
git clone https://github.com/tinylion1024/topic-research-report.git ~/.claude/skills/topic-research-report
git clone https://github.com/tinylion1024/initiation-of-coverage-or-deep-dive.git ~/.claude/skills/initiation-of-coverage-or-deep-dive
git clone https://github.com/tinylion1024/taoguba-hot.git ~/.claude/skills/taoguba-hot
git clone https://github.com/tinylion1024/open-gstack-browser.git ~/.claude/skills/open-gstack-browser
```

---

## 依赖 Skill 清单

### Iwencai（数据源）

| Skill | 功能 | 必需 |
|-------|------|------|
| **market-data-query** | 行情数据 | 核心 |
| **financial-data-query** | 财务数据 | 核心 |
| **a-share-screener** | A股选股 | 核心 |
| **sector-screener** | 板块选股 | 核心 |
| **news-search** | 新闻搜索 | 核心 |
| **announcement-search** | 公告搜索 | 核心 |
| **research-report-search** | 研报搜索 | 推荐 |
| **macro-data-query** | 宏观数据 | 推荐 |
| **industry-data-query** | 行业数据 | 推荐 |
| **event-data-query** | 事件数据 | 推荐 |
| **basic-info-query** | 基本资料 | 推荐 |
| **index-data-query** | 指数数据 | 推荐 |
| **convertible-bond-screener** | 可转债选股 | 可选 |
| **etf-screener** | ETF选股 | 可选 |
| **fund-screener** | 基金选股 | 可选 |
| **futures-options-data-query** | 期货期权 | 可选 |

### MX/AkShare（备选数据源）

| Skill | 功能 | 必需 |
|-------|------|------|
| **akshare-stock** | AkShare数据 | 核心 |
| **mx-finance-data** | MX财务数据 | 核心 |
| **mx-macro-data** | MX宏观数据 | 核心 |
| **mx-stocks-screener** | MX智能选股 | 核心 |
| **mx-finance-search** | MX市场搜索 | 核心 |
| **mx-financial-assistant** | 妙想问答助手 | 核心 |
| **stock-diagnosis** | 股票综合诊断 | 核心 |
| **taoguba-hot** | 社区情绪 | 推荐 |
| **stock-earnings-review** | 业绩点评 | 推荐 |
| **industry-stock-tracker** | 行业/个股追踪 | 推荐 |
| **open-gstack-browser** | 浏览器工具 | 必需 |

---

## 环境变量配置

### API 密钥获取

| 服务 | 获取地址 | 说明 |
|------|---------|------|
| **IWENCAI API** | https://open.iwencai.com | 问财数据API（必需） |
| **MX API** | https://mx.com | 妙想量化API（必需） |
| **EM API** | https://eastmoney.com | 东方财富API（可选） |

### 配置方式

**方式一：运行时询问（推荐）**

首次运行任意脚本时会自动触发配置向导：

```bash
python3 scripts/check_risk.py --code 300750
```

向导会询问：
- IWENCAI API 密钥
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

**方式三：环境变量**

```bash
# Iwencai（必需）
export IWENCAI_BASE_URL=https://openapi.iwencai.com
export IWENCAI_API_KEY=your_iwencai_apikey

# MX（必需）
export MX_APIKEY=your_mx_apikey

# EM（可选）
export EM_API_KEY=your_em_apikey
```

---

## 依赖检查

安装完成后验证：

```bash
# Iwencai CLI
which iwencai-skillhub-cli

# Iwencai Skills
ls ~/.claude/skills/ | grep -E "(market-data|financial-data|a-share|sector|news|announcement|research|macro|industry|event|basic|index|convertible|etf|fund|futures)" || echo "需要安装Iwencai Skills"

# MX/AkShare Skills
for skill in \
  akshare-stock \
  mx-finance-data \
  mx-macro-data \
  mx-stocks-screener \
  mx-finance-search \
  mx-financial-assistant \
  stock-diagnosis \
  taoguba-hot \
  stock-earnings-review \
  industry-stock-tracker \
  open-gstack-browser; do
  if [ -d "$HOME/.claude/skills/$skill" ]; then
    echo "✅ $skill"
  else
    echo "❌ $skill - 未安装"
  fi
done
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

### Q: Iwencai 安装失败？

确保已安装 CLI：
```bash
curl -sSL https://www.iwencai.com/skillhub/static/0.0.4/download_and_install.sh | bash
```

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

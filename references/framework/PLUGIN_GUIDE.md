# 插件开发指南

本文档介绍如何为 A-Shares Master 开发插件。

## 插件类型

| 插件类型 | 接口 | 说明 |
|----------|------|------|
| 数据源插件 | `DataSourcePlugin` | 获取市场数据 |
| 情绪源插件 | `SentimentPlugin` | 获取社区情绪 |
| 指标插件 | `IndicatorPlugin` | 计算技术指标 |
| 报告插件 | `ReportPlugin` | 生成自定义报告 |

## 开发步骤

### 1. 创建插件文件

```python
# src/plugins/your_plugin.py
from typing import Dict, Any, List
from src.plugins.base import BasePlugin


class YourDataSourcePlugin(BasePlugin):
    """数据源插件示例"""

    name = "your_data_source"
    version = "1.0.0"
    description = "自定义数据源"

    def initialize(self) -> None:
        """初始化插件"""
        # 连接数据源、验证配置等
        self._initialized = True

    def cleanup(self) -> None:
        """清理资源"""
        pass

    def fetch_market_data(self, date: str) -> Dict[str, Any]:
        """获取市场数据"""
        return {
            "date": date,
            "data": [],
        }

    def fetch_stock_data(self, code: str, date: str) -> Dict[str, Any]:
        """获取个股数据"""
        return {
            "code": code,
            "date": date,
            "data": {},
        }
```

### 2. 在注册表注册

```python
# src/plugins/__init__.py
from src.plugins.your_plugin import YourDataSourcePlugin

# 在模块加载时注册
PluginRegistry.register("your_data_source", YourDataSourcePlugin())
```

### 3. 使用插件

```python
from src.plugins import PluginRegistry

plugin = PluginRegistry.get("your_data_source")
if plugin:
    data = plugin.fetch_market_data("2024-01-15")
```

## 插件配置

插件通过 `config/module_config.json` 配置：

```json
{
  "plugins": {
    "data_sources": {
      "default": "mx_data",
      "fallback": "akshare",
      "custom": {
        "your_data_source": {
          "enabled": true,
          "priority": 1
        }
      }
    }
  }
}
```

## 最佳实践

1. **错误处理**：插件应捕获自身异常，不影响主流程
2. **缓存**：高频数据应实现缓存机制
3. **降级**：主数据源失败时支持自动降级
4. **监控**：记录调用日志便于问题排查

## 内置插件

| 插件名 | 类型 | 说明 |
|--------|------|------|
| mx_data | 数据源 | MX API 数据源 |
| akshare | 数据源 | akshare 数据源（备用） |
| taoguba | 情绪源 | 淘股吧情绪 |
| xueqiu | 情绪源 | 雪球情绪（备用） |

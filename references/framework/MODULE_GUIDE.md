# 模块开发指南

本文档介绍如何为 A-Shares Master 开发新的功能模块。

## 模块结构

每个功能模块应遵循以下结构：

```
src/modules/
├── __init__.py           # 模块注册
├── pre_market.py         # 盘前分析模块（示例）
└── your_module.py        # 你的新模块
```

## 开发步骤

### 1. 创建模块文件

```python
# src/modules/your_module.py
import argparse
from typing import Dict, Any

from src.core.context import ExecutionContext, ExecutionMode


class YourModule:
    """
    模块描述

    职责:
    - 功能点1
    - 功能点2
    """

    name = "your_module"

    def execute(self, context: ExecutionContext) -> Dict[str, Any]:
        """
        执行模块逻辑

        Args:
            context: 执行上下文

        Returns:
            Dict: 包含 'report' 键的字典
        """
        # 实现逻辑
        result = {
            "data": {},
            "report": self._generate_markdown_report({}),
        }
        return result

    def _generate_markdown_report(self, data: Dict[str, Any]) -> str:
        """生成 Markdown 报告"""
        lines = [
            "# 模块报告",
            "",
            "内容...",
            "",
            "---",
            "*本报告仅供参考，不构成投资建议*",
        ]
        return "\n".join(lines)


def main():
    """CLI 入口"""
    parser = argparse.ArgumentParser(description="你的模块")
    parser.add_argument("--stock", type=str, help="股票代码")
    args = parser.parse_args()

    from datetime import datetime

    context = ExecutionContext(
        mode=ExecutionMode.YOUR_MODE,
        date=datetime.now().strftime("%Y-%m-%d"),
        stock_code=args.stock,
    )

    module = YourModule()
    result = module.execute(context)
    print(result["report"])


if __name__ == "__main__":
    main()
```

### 2. 在 `__init__.py` 中注册

```python
# src/modules/__init__.py
from src.modules.your_module import YourModule

__all__ = [
    # ... 其他模块
    "YourModule",
]

MODULE_REGISTRY = {
    # ... 其他模块
    "your_module": YourModule,
}
```

### 3. 在 `ExecutionMode` 中添加新模式

编辑 `src/core/context.py`：

```python
class ExecutionMode(Enum):
    # ... 其他模式
    YOUR_MODE = "your_mode"  # 新增
```

### 4. 测试模块

```bash
python3 src/modules/your_module.py --stock 300750
```

## 最佳实践

1. **输入验证**：在 `execute()` 开始时验证必要参数
2. **错误处理**：捕获异常并添加到 `context.errors`
3. **报告格式**：始终使用 Markdown 格式输出
4. **数据源**：优先使用配置的数据源插件
5. **单元测试**：为模块编写单元测试

## 示例：添加技术指标模块

参见 `src/modules/` 下的现有实现。

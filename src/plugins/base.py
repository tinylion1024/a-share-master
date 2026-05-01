"""插件基类"""
from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """插件基类"""

    name: str = ""
    version: str = "1.0.0"

    @abstractmethod
    def execute(self, *args, **kwargs):
        """执行插件"""
        pass

    def __repr__(self) -> str:
        return f"<{self.name} v{self.version}>"
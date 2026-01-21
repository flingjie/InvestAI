from abc import ABC, abstractmethod
from typing import Dict, Any
from enum import Enum

class TrendType(Enum):
    UPTREND = "Uptrend – buying could be considered"
    NEUTRAL = "Neutral – recommended to wait and see"
    DOWNTREND = "Downtrend – weak, exercise caution"



class BaseSignal(ABC):

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> dict:
        """
        context 中包含：
        - 行情数据
        - 基本面数据
        - 事件数据
        """
        pass

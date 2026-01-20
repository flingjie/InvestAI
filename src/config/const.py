from enum import Enum, unique

@unique  # 装饰器确保成员值唯一，防止逻辑冲突
class MarketType(Enum):
    US = 'US'
    SH = 'SH'
    SZ = 'SZ'
    HK = 'HK'
    UNSUPPORT = 'UNSUPPORT'

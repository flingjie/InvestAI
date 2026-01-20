import re
from config.const import MarketType

def get_fullcode(code: str) -> str:
    if code.startswith("00") or code.startswith("30"):
        if '.' in code:
            code = code.split('.')[0]
        return f"sz{code}"
    elif code.startswith("60"):
        if '.' in code:
            code = code.split('.')[0]
        return f"sh{code}"
    else:
        return code


def identify_market(symbol):
    symbol = str(symbol).upper()
    
    if symbol.endswith('.SS') or symbol.endswith('.SH') or symbol.startswith('sh') or symbol.startswith('ss'):
        return MarketType.SH
    if symbol.endswith('.SZ') or symbol.startswith('sz'):
        return MarketType.SZ
    if symbol.endswith('.HK'):
        return MarketType.HK
    
    if symbol.isalpha() or symbol.startswith('^'):
        return MarketType.US
    
    if symbol.isdigit():
        if symbol.startswith(('60', '68')): return MarketType.SH
        if symbol.startswith(('00', '30')): return MarketType.SZ
        if len(symbol) <= 4: return "港股 (猜测)"
        
    return MarketType.UNSUPPORT


def extract_code(fullcode: str) -> str:
    """
    基于正则提取基础股票6位数代码
    """
    pattern = r"^(sh|sz)?(\d{6})$"
    match = re.match(pattern, fullcode)
    if match:
        return match.group(2)
    return fullcode
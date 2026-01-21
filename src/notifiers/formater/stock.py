from notifiers.formater.base import get_trend_emoji
from signals.base import TrendType
from config import STRATEGY_CONFIG
from utils.json import to_pretty_json

def format_trend_signal_message(data: dict) -> str:
    """
    Format trend monitoring results into a Slack / Feishu notification message
    """

    name = data.get("name")
    price = data.get("price")
    ma_short = data.get("ma_short")
    ma_long = data.get("ma_long")
    trend = data.get("trend")
    pullback = data.get("pullback")
    breakout = data.get("breakout")
    rsi = data.get("rsi")
    cci = data.get("cci")

    # === Structure evaluation ===
    pullback_desc = "Detected" if pullback else "Not detected"
    breakout_desc = "Confirmed" if breakout else "Not confirmed"

    # === RSI / CCI timing description ===
    rsi_ok = STRATEGY_CONFIG.rsi.min <= rsi <= STRATEGY_CONFIG.rsi.max
    cci_ok = STRATEGY_CONFIG.cci.min <= cci <= STRATEGY_CONFIG.cci.max

    if rsi_ok:
        rsi_desc = "within the effective range"
    elif rsi < STRATEGY_CONFIG.rsi.min:
        rsi_desc = "weak"
    else:
        rsi_desc = "strong"

    if cci_ok:
        cci_desc = "within the normal fluctuation range"
    elif cci < STRATEGY_CONFIG.cci.min:
        cci_desc = "oversold"
    else:
        cci_desc = "overheated"

    # === Overall evaluation ===
    if trend == TrendType.UPTREND and (pullback or breakout) and rsi_ok and cci_ok:
        final_desc = "Trend and timing conditions are met. This matches a trend-following buy setup."
    else:
        final_desc = (
            "The current trend, structure, or timing conditions are not met. "
            "This does not qualify as a trend-following setup. It is better to continue observing."
        )

    # === Build message ===
    message = (
        f"Stock: {name}{get_trend_emoji(trend)}\n"
        f"Current Price: {price:.2f}\n"
        f"MA_{STRATEGY_CONFIG.trend.moving_averages.short} / "
        f"MA_{STRATEGY_CONFIG.trend.moving_averages.long}: "
        f"{ma_short:.2f} / {ma_long:.2f}\n"
        f"Market Trend: {trend.value}\n\n"
        f"Structure:\n"
        f"- Pullback pattern: {pullback_desc}\n"
        f"- Breakout pattern: {breakout_desc}\n\n"
        f"Timing indicators (soft filters):\n"
        f"- RSI: {rsi:.1f} ({rsi_desc})\n"
        f"- CCI: {cci:.1f} ({cci_desc})\n\n"
        f"Overall assessment:\n"
        f"{final_desc}\n\n"
        f"━━━━━━━━━━━━━━━━"
    )

    return message


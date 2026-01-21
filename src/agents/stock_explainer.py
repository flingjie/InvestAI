from .prompts.helper import get_prompt_from_template
from .llm import get_response_by_llm
import json
from utils.json import to_pretty_json
from config import SYS_CONFIG


def explain_stock_trend(current_state: dict):
    language = SYS_CONFIG.language
    template_name = f"stock_explainer_{language}.md"
    prompt = get_prompt_from_template(template_name, {"current_state":to_pretty_json(current_state)})
    response = get_response_by_llm(prompt)
    return response


if __name__ == "__main__":
    current_state = {
        "price": 16.77,
        "ma_short": 17.23,
        "ma_long": 17.55,
        "trend": "弱势，请注意避险",
        "pullback": False,
        "breakout": False,
        "volume": 10080808.0,
        "volume_ma": 12856244.4,
        "volume_ok": False,
        "rsi": 46.15,
        "rsi_ok": True,
        "cci": -86.21,
        "cci_ok": True,
        "timing_ok": False,
        "name": "佐力药业"
        }
    print(explain_stock_trend(current_state))

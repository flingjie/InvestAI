from .prompts.helper import get_prompt_from_template
from .llm import get_response_by_llm
from utils.json import to_pretty_json
from config import SYS_CONFIG


def explain_index_trend(current_state: dict):
    language = SYS_CONFIG.language  
    template_name = f"index_explainer_{language}.md"
    prompt = get_prompt_from_template(template_name, {"current_state":to_pretty_json(current_state)})
    response = get_response_by_llm(prompt)
    return response


if __name__ == "__main__":
    current_state = [
        {
            "price": 4657.24,
            "ma_short": 4582.73,
            "ma_long": 4600.7,
            "trend": "建议观望",
            "pullback": False,
            "breakout": False,
            "name": "沪深300"
        },
        {
            "price": 7458.84,
            "ma_short": 7160.45,
            "ma_long": 7200.89,
            "trend": "建议观望",
            "pullback": False,
            "breakout": False,
            "name": "中证500"
        },
        {
            "price": 7605.53,
            "ma_short": 7365.39,
            "ma_long": 7405.19,
            "trend": "建议观望",
            "pullback": False,
            "breakout": False,
            "name": "中证1000"
        }
        ]
    print(explain_index_trend(current_state))

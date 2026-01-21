from .prompts.helper import get_prompt_from_template
from .llm import get_response_by_llm
import json
import yaml
from utils.json import to_pretty_json
from config import STRATEGY_CONFIG, LLM_CONFIG, STRATEGY_CONFIG_PATH
from config import SYS_CONFIG



def edit_strategy(current_strategy: dict, user_input: str):
    language = SYS_CONFIG.language
    template_name = f"strategy_editor_{language}.md"
    prompt = get_prompt_from_template(template_name, {
        "current_strategy":to_pretty_json(current_strategy), "user_input":user_input}
    )
    response = get_response_by_llm(prompt, model_name=LLM_CONFIG.base_model)
    return response


if __name__ == "__main__":
    with open(STRATEGY_CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
        print(edit_strategy(raw, "激进派、喜欢做几天就出的短线波动"))

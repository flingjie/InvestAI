from .prompts.helper import get_prompt_from_template
from .llm import get_response_by_llm
import json
from utils.json import to_pretty_json
from config import STRATEGY_CONFIG, LLM_CONFIG, SYS_CONFIG


def explain_strategy(current_strategy: dict):
    language = SYS_CONFIG.language
    template_name = f"strategy_explainer_{language}.md"
    prompt = get_prompt_from_template(template_name, {"current_strategy":to_pretty_json(current_strategy)})
    response = get_response_by_llm(prompt, model_name=LLM_CONFIG.base_model)
    return response


if __name__ == "__main__":
    print(explain_strategy(STRATEGY_CONFIG))

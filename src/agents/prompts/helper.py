import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from log import logger

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get_prompt_from_template(
    prompt_name: str, vars: dict
) -> str:
    try:
        # logger.debug(f"get prompt from template {prompt_name}")
        template = env.get_template(prompt_name)
        return template.render(**vars)
    except Exception as e:
        raise ValueError(f"Error applying template {prompt_name}: {e}")
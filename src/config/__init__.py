from .config import *
from .loader import load_strategy_config, load_notification_config, load_schedule_config, load_llm_config, load_sys_config


STRATEGY_CONFIG = load_strategy_config(STRATEGY_CONFIG_PATH)
NOTIFICATION_CONFIG = load_notification_config(CONFIG_PATH)
SCHEDULE_CONFIG = load_schedule_config(CONFIG_PATH)
LLM_CONFIG = load_llm_config(CONFIG_PATH)
SYS_CONFIG = load_sys_config(CONFIG_PATH)

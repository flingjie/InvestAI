import yaml
from pathlib import Path
from .strategy import StrategyConfig
from .config import NotificationConfig, ScheduleConfig, LLMConfig, SysConfig
import os
import re

ENV_PATTERN = re.compile(r"\$\{([^}^{]+)\}")


def inject_env_vars(value):
    """
    将 ${VAR_NAME} 替换为环境变量
    """
    if isinstance(value, str):
        match = ENV_PATTERN.fullmatch(value)
        if match:
            env_key = match.group(1)
            if env_key not in os.environ:
                raise RuntimeError(f"Missing environment variable: {env_key}")
            return os.environ[env_key]
        return value

    if isinstance(value, dict):
        return {k: inject_env_vars(v) for k, v in value.items()}

    if isinstance(value, list):
        return [inject_env_vars(v) for v in value]

    return value


def load_yaml_with_env(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return inject_env_vars(data)


def load_strategy_config(path: str | Path) -> StrategyConfig:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return StrategyConfig(**data)



def load_notification_config(path: str) -> NotificationConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    
    # 注入环境变量
    raw = inject_env_vars(raw)
    
    return NotificationConfig.model_validate(raw["notification"])


def load_schedule_config(path: str | Path) -> ScheduleConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    
    return ScheduleConfig.model_validate(raw["schedule"])


def load_llm_config(path: str | Path) -> LLMConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    # 注入环境变量
    raw = inject_env_vars(raw)
    return LLMConfig.model_validate(raw["llm"])



def load_sys_config(path: str | Path) -> SysConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return SysConfig.model_validate(raw["system"])
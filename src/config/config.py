from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "./logs"
WATCHLIST_PATH = "./conf/watchlist.json"
INDEX_POOL_PATH = "./conf/index_pool.json"
STRATEGY_CONFIG_PATH = "./conf/strategy.yaml"
CONFIG_PATH = "./conf/invest_ai.yaml"

class SlackChannelConfig(BaseModel):
    enabled: bool
    type: Literal["slack"] = "slack"

    token: str = Field(
        ..., description="Slack Bot Token，通常从环境变量注入"
    )
    default_channel: str = Field(
        ..., description="默认 Slack 频道"
    )

    message_format: Literal["markdown", "text"] = "markdown"
    description: Optional[str] = None


class WebhookEndpointConfig(BaseModel):
    name: str
    url: str


class WebhookChannelConfig(BaseModel):
    enabled: bool
    type: Literal["webhook"] = "webhook"

    endpoints: List[WebhookEndpointConfig]
    description: Optional[str] = None


class SMTPConfig(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = True


class EmailChannelConfig(BaseModel):
    enabled: bool
    type: Literal["email"] = "email"

    smtp: SMTPConfig
    from_: str = Field(
        ..., alias="from", description="发件人地址"
    )
    to: List[str]

    description: Optional[str] = None

class ConsoleChannelConfig(BaseModel):
    enabled: bool
    type: Literal["console"] = "console"

    description: Optional[str] = None

NotificationChannelConfig = (
    SlackChannelConfig
    | WebhookChannelConfig
    | EmailChannelConfig
    | ConsoleChannelConfig
)


class NotificationConfig(BaseModel):
    enabled: bool

    channels: Dict[str, NotificationChannelConfig]


class ScheduleConfig(BaseModel):
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)


class LLMConfig(BaseModel):
    provider: str
    base_model: str
    reason_model: str
    base_url: str
    api_key: Optional[str] = None


class SysConfig(BaseModel):
    language: str


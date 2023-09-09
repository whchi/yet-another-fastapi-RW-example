import logging
from typing import Any, List

from slack_sdk import WebhookClient
from slack_sdk.errors import SlackApiError

from app.core import get_app_settings
from app.core.settings import AppSettings

from .provider_contract import ProviderContract


class SlackHandler(logging.Handler):

    def __init__(self, app_config: AppSettings):
        super().__init__()
        self.app_config = app_config
        self.logger_config = get_app_settings()

    def format(self, record: logging.LogRecord) -> List[Any]:  # type: ignore
        icon = {
            logging.CRITICAL: ':boom:',
            logging.ERROR: ':bomb:',
            logging.WARN: ':broken_heart:',
            logging.INFO: ':information_source:',
            logging.DEBUG: ':cockroach:'
        }
        message_debug_block = {}
        if self.app_config.APP_DEBUG:
            message_debug_block = {
                'type': 'section',
                'text': {
                    'type': 'plain_text',
                    'text': f'{record.pathname}:{record.lineno}@{record.funcName}'
                }
            }
        return [{
            'type': 'header',
            'text': {
                'type':
                    'plain_text',
                'text':
                    f'[{self.app_config.APP_ENV}] {icon[record.levelno]} {record.levelname}'
            }
        }, {
            'type': 'divider'
        }, message_debug_block, {
            'type': 'section',
            'text': {
                'type': 'mrkdwn',
                'text': f'*Message*\n```{record.getMessage()}```'
            }
        }]

    def emit(self, record: logging.LogRecord) -> None:
        blocks = self.format(record)
        try:
            client = WebhookClient(url=self.logger_config.SLACK_WEBHOOK_URL)
            client.send(blocks=blocks)
        except SlackApiError as e:
            print(f'Error sending message to Slack: {e}.')


class SlackProvider(ProviderContract):

    def __init__(self) -> None:
        self.logger = logging.getLogger('slack-logger')
        self.logger.setLevel(super().app_config.log_level)
        self.logger.addHandler(SlackHandler(super().app_config))

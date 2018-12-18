from typing import Dict, Any
from pathlib import Path
import requests
import json
import yaml

MAX_NOTIFY_MEMORY = 1000
SLACK_SECRET_PATH = 'secret/slack.yml'


class EventNotifier:
    def __init__(self):
        self._notified_list = []
        self._config = self._load_config()

    def was_notified(self, event: Dict) -> bool:
        return event['id'] in self._notified_list

    def notify(self, event: Dict) -> None:
        self._post_slack(self._format(event))
        self._regist_id(event['id'])

    def _format(self, event: Dict) -> str:
        return '{subject} - {facility} ({start}〜)'.format(
            start=event['start']['dateTime'],
            subject=event['subject'],
            facility=event['facilities'][0]['name'] if event['facilities'] else '',
        )

    def _post_slack(self, text: str) -> None:
        payload = {
            'text': text,
        }
        requests.post(self._config['webhook'], data=json.dumps(payload))

    def _regist_id(self, id_: int) -> None:
        self._notified_list.append(id_)
        if len(self._notified_list) > MAX_NOTIFY_MEMORY:
            self._notified_list = self._notified_list[-MAX_NOTIFY_MEMORY:]

    def _load_config(self, secret_path: str = SLACK_SECRET_PATH) -> Any:
        root_path = Path(__file__).parents[1]
        file_path = root_path / secret_path
        with open(file_path) as f:
            return yaml.load(f)


if __name__ == '__main__':
    notifier = EventNotifier()
    notifier.notify({
        'id': 1234,
        'subject': 'test',
        'facilities': [{'name': 'facility'}],
        'start': {'dateTime': '2018-10-10T00:00:00+09:00'},
    })

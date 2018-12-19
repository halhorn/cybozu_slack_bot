import os
from datetime import datetime, timedelta
import base64
from typing import Any
from pathlib import Path
import yaml
import requests

SECRET_PATH = 'secret/cybouzu.yml'
URL = 'https://{sub_domain}.cybozu.com:443/g/api/v1/schedule/events'


class EventFetcher:
    def __init__(self):
        self._config = self._load_config()
        if 'pass' not in self._config:
            self._config['pass'] = os.environ.get('CYBOUZU_PASS')
        if not self._config.get('pass'):
            raise Exception('pass is not set')

    def _load_config(self, secret_path: str = SECRET_PATH) -> Any:
        root_path = Path(__file__).parents[1]
        file_path = root_path / secret_path
        with open(file_path) as f:
            return yaml.load(f)

    def get_event_list(self, notify_buffer_sec: int, limit: int = 100):
        result = self.request(notify_buffer_sec, limit)
        event_list = result['events']
        event_list = [event for event in event_list if event['eventType'] != 'ALL_DAY']
        return event_list

    def request(self, notify_buffer_sec: int, limit: int = 100):
        raw_auth = '{id}:{pass}'.format(**self._config)
        auth = base64.b64encode(raw_auth.encode('utf-8')).decode('utf-8')
        url = URL.format(**self._config)
        start = datetime.now()
        end = start + timedelta(seconds=notify_buffer_sec)

        payload = {
            'limit': limit,
            'orderBy': 'start asc',
            'rangeStart': self._date2str(start),
            'rangeEnd': self._date2str(end),
            'fields': ','.join(['id', 'start', 'subject', 'facilities', 'eventType']),
        }
        header = {
            'X-Cybozu-Authorization': auth,
            'Authorization': f'Basic {auth}',
        }
        res = requests.get(url, params=payload, headers=header)

        if res.status_code != 200:
            raise Exception(res.reason)

        return res.json()

    def _date2str(self, dt):
        return dt.strftime('%Y-%m-%dT%H:%M:%S+09:00')


if __name__ == '__main__':
    manager = CybouzuRequestManager()
    print(manager.request(60 * 5))

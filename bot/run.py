import time
from typing import Dict
from bot.cybouzu_request_manager import CybouzuRequestManager

INTERVAL_SEC = 10
NOTIFY_BUFFER_SEC = 60 * 5
MAX_NOTIFY_MEMORY = 1000


def execute() -> None:
    i = 0
    event_list = []
    event_notifier = EventNotifier()
    while True:
        event_list = check()

        for event in event_list:
            if event_notifier.was_notified(event):
                continue
            event_notifier.notify(event)
        time.sleep(INTERVAL_SEC)
        i += 1


def check() -> None:
    request_manager = CybouzuRequestManager()
    result = request_manager.request(NOTIFY_BUFFER_SEC)
    event_list = result['events']
    event_list = [event for event in event_list if event['eventType'] != 'ALL_DAY']
    return event_list


class EventNotifier:
    def __init__(self):
        self._notified_list = []

    def was_notified(self, event: Dict) -> bool:
        return event['id'] in self._notified_list

    def notify(self, event: Dict) -> None:
        print(self._format(event))
        self._notified_list.append(event['id'])
        if len(self._notified_list) > MAX_NOTIFY_MEMORY:
            self._notified_list = self._notified_list[-MAX_NOTIFY_MEMORY:]

    def _format(self, event: Dict) -> str:
        return '{subject} - {facility} ({start}〜)'.format(
            start=event['start']['dateTime'],
            subject=event['subject'],
            facility=event['facilities'][0]['name'] if event['facilities'] else '',
        )


if __name__ == '__main__':
    execute()

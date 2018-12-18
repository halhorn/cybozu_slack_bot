import time
from bot.cybouzu_request_manager import CybouzuRequestManager
from bot.event_notifier import EventNotifier

INTERVAL_SEC = 10
NOTIFY_BUFFER_SEC = 60 * 5


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


if __name__ == '__main__':
    execute()

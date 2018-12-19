import time
from bot.event_fetcher import EventFetcher
from bot.event_notifier import EventNotifier

INTERVAL_SEC = 60
NOTIFY_BUFFER_SEC = 60 * 5  # 何分前にイベントを通知するか（ただし最大 INTERVAL_SEC 分ずれます）


class Runner:
    def __init__(self) -> None:
        self._event_fetcher = EventFetcher()
        self._event_notifier = EventNotifier()

    def run(self) -> None:
        while True:
            try:
                self._get_event_and_notify()
            except KeyboardInterrupt:
                print('keyboard Interrupt.')
                return
            except Exception as e:
                print('ERROR')
                print(e)

            time.sleep(INTERVAL_SEC)

    def _get_event_and_notify(self) -> None:
        event_list = self._event_fetcher.get_event_list(NOTIFY_BUFFER_SEC)

        for event in event_list:
            if self._event_notifier.was_notified(event):
                continue
            self._event_notifier.notify(event)


if __name__ == '__main__':
    Runner().run()

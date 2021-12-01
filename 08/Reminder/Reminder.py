import asyncio

from abc import abstractmethod
from dataclasses import dataclass

from ApplicationSettings import application_settings
from DataStorage import SqliteDataStorage
from Desktop import Desktop


@dataclass
class Notification:
    original: str
    translation: str
    transcription: str

    def __init__(self, notification: dict):
        self.original = notification['original']
        self.translation = notification['translation']
        self.transcription = notification['transcription']


class AbstractNotifier(object):
    @abstractmethod
    def send_notification(self, notification: Notification):
        pass


class StdOutputNotifier(AbstractNotifier):
    def send_notification(self, notification: Notification):
        print(notification)


class DesktopNotifier(AbstractNotifier):
    def send_notification(self, notification: Notification):
        Desktop.send_notification(
            notification.original,
            f'{notification.translation} {notification.transcription}'
        )


async def main():
    notifiers = {
        'stdout': StdOutputNotifier,
        'desktop': DesktopNotifier,
    }

    while True:
        notifier = notifiers.get(application_settings.notifier, StdOutputNotifier)()
        storage = SqliteDataStorage(application_settings.collection)

        await asyncio.sleep(application_settings.timeout)
        notifier.send_notification(Notification(storage.get_any_object()))

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

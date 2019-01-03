import logging
from abc import abstractmethod
from time import sleep

from bus import queues
from bus.api import Bus, Handler, Message

logger = logging.getLogger(__name__)


class SimplePersistingHandler(Handler):

    @abstractmethod
    def prepare_data_to_persist(self, payload):
        pass

    def handle(self, message: Message, bus: Bus):
        payload_to_persist = self.prepare_data_to_persist(message.payload)
        bus.send(queues.QUEUE_PERSIST, Message(payload_to_persist))


class PersisterHandler(Handler):

    def handle(self, message: Message, bus: Bus):
        self.persist(message.payload)

    @staticmethod
    def persist(data):
        logger.info('Persisting %s', data)
        sleep(2)

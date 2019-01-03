import os
from sys import argv

from bus import queues
from bus.impl.rabbitmq import RmqBus
from handler.lighthouse import LighthouseCalculateScoreHandler
from handler.persist import PersisterHandler


HANDLERS = {
    'lighthouse': (queues.QUEUE_LIGHTHOUSE_COMPUTE, LighthouseCalculateScoreHandler()),
    'persister': (queues.QUEUE_PERSIST, PersisterHandler())
}


def register_handlers():
    print("Starting worker")

    bus = RmqBus(os.getenv('mq_host', 'localhost'))
    for handler_name in argv:
        if handler_name in HANDLERS:
            queue, handler = HANDLERS[handler_name]
            bus.subscribe(queue, handler)

    bus.start_consuming()


if __name__ == '__main__':
    register_handlers()

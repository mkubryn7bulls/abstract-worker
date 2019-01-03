import os
from time import sleep

from bus import queues
from bus.api import Message
from bus.impl.rabbitmq import RmqBus

bus = RmqBus(os.getenv('mq_host', 'localhost'))


def main():
    while True:
        bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://google.com'))
        bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://facebook.com'))
        bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://linkedin.com'))
        print("Messages sent")
        sleep(30)


if __name__ == '__main__':
    main()

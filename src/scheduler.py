import os
from time import sleep

from bus import queues
from bus.api import Message
from bus.impl.rabbitmq import RmqBus
from metrics.serp import SerpRequest

bus = RmqBus(os.getenv('mq_host', 'localhost'))


def main():
    bus.send(queues.SERP_CREATE_TASKS, Message([
        SerpRequest('restauracja wegańska', 'Warsaw,Masovian Voivodeship,Poland'),
        SerpRequest('restauracja grochów', 'Warsaw,Masovian Voivodeship,Poland'),
        SerpRequest('restauracja dla wegan', 'Warsaw,Masovian Voivodeship,Poland'),
    ]))

    while True:
        # bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://google.com'))
        # bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://facebook.com'))
        # bus.send(queues.QUEUE_LIGHTHOUSE_COMPUTE, Message('https://linkedin.com'))
        bus.send(queues.SERP_COLLECT_FINISHED_TASKS, Message(None)),
        print("Messages sent")
        sleep(10)


if __name__ == '__main__':
    main()

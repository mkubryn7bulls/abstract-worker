import logging
import os
from sys import argv

from bus import queues
from bus.impl.rabbitmq import RmqBus
from handler.lighthouse import LighthouseCalculateScoreHandler
from handler.persist import PersisterHandler
from handler.serp import SerpCreateTasks, SerpCollectFinishedTasksHandler, SerpCollectTaskResults

HANDLERS = {
    'lighthouse': [(queues.QUEUE_LIGHTHOUSE_COMPUTE, LighthouseCalculateScoreHandler())],
    'persister': [(queues.QUEUE_PERSIST, PersisterHandler())],
    'serp': [
        (queues.SERP_REQUESTS, SerpCreateTasks()),
        (queues.SERP_DFS_COLLECT_FINISHED_TASKS, SerpCollectFinishedTasksHandler()),
        (queues.SERP_DFS_COLLECT_TASK_RESULTS, SerpCollectTaskResults()),
    ],
}


def init_logging():
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')

    logging.getLogger("pika").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def register_handlers():
    print("Starting worker")
    init_logging()

    bus = RmqBus(os.getenv('mq_host', 'localhost'))
    for handler_name in argv:
        if handler_name in HANDLERS:
            for queue, handler in HANDLERS[handler_name]:
                bus.subscribe(queue, handler)

    bus.start_consuming()


if __name__ == '__main__':
    register_handlers()

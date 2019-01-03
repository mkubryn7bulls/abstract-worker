import logging

from bus.api import Handler, Message, Bus
from bus.queues import SERP_COLLECT_RESULTS
from handler.persist import SimplePersistingHandler
from handler.serp.dataforseo import DfsApiClient, DfsApiException

logger = logging.getLogger(__name__)
api_key = 'Basic <HERE GOES YOUR SECRET API KEY>'


class SerpCreateTasks(Handler):
    def handle(self, message: Message, bus: Bus):
        with DfsApiClient(api_key) as client:
            logger.debug('Creating SERP tasks: %s', message.payload)
            client.create_serp_tasks(message.payload)


class SerpCollectFinishedTasksHandler(Handler):
    def handle(self, message: Message, bus: Bus):
        with DfsApiClient(api_key) as client:
            logger.debug('Collecting finished SERP tasks')
            task_ids = client.get_finished_tasks()
            for task_id in task_ids:
                logger.debug('SERP task %s is finished. Scheduled for collecting results')
                bus.send(SERP_COLLECT_RESULTS, Message(task_id))


class SerpCollectTaskResults(SimplePersistingHandler):
    def prepare_data_to_persist(self, payload):
        with DfsApiClient(api_key) as client:
            logger.debug('Collecting results of task %s', payload)
            serp_result = client.get_serp_task(payload)
            return serp_result

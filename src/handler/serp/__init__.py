import logging

from bus.api import Handler, Message, Bus
from bus.queues import SERP_DFS_COLLECT_TASK_RESULTS
from handler.persist import SimplePersistingHandler
from handler.serp.dataforseo import DfsApiClient, DfsApiException

logger = logging.getLogger(__name__)
api_key = 'Basic bWt1YnJ5bkA3YnVsbHMuY29tOjRZTERnNUx6WUU1SG1ycFM='


class SerpCreateTasks(Handler):
    """
    Handles SerpRequest from the SERP_REQUESTS queue and registers SERP tasks for each request
    in the DataForSEO.com API.
    """
    def handle(self, message: Message, bus: Bus):
        with DfsApiClient(api_key) as client:
            logger.debug('Creating SERP tasks: %s', message.payload)
            client.create_serp_tasks(message.payload)


class SerpCollectFinishedTasksHandler(Handler):
    """
    Collects the list of finished SERP tasks from the DataForSEO API and sends each the task id
    to the SERP_DFS_COLLECT_TASK_RESULTS queue.

    Note that DataForSEO API does not charge clients for this action thus it might be repeated in a loop.
    """
    def handle(self, message: Message, bus: Bus):
        with DfsApiClient(api_key) as client:
            logger.debug('Collecting finished SERP tasks')
            task_ids = client.get_finished_tasks()
            for task_id in task_ids:
                logger.debug('SERP task %s is finished. Scheduled for collecting results')
                bus.send(SERP_DFS_COLLECT_TASK_RESULTS, Message(task_id))


class SerpCollectTaskResults(SimplePersistingHandler):
    """
    Handles incoming task ids by fetching their results from DataForSEO API,
    """
    def prepare_data_to_persist(self, payload):
        with DfsApiClient(api_key) as client:
            logger.debug('Collecting results of task %s', payload)
            serp_result = client.get_serp_task(payload)
            return serp_result

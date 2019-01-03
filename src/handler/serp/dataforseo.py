import logging
from logging import DEBUG
from time import sleep
from typing import List, Optional, Dict

import requests

from metrics.serp import SerpRequest, SerpPosition, SerpResponse

logger = logging.getLogger(__name__)


class DfsApiException(Exception):
    pass


class DfsApiClient:
    """
    Client for communication with dataforseo.com services
    """

    def __init__(self, api_key, **api_ops):
        self._api_key = api_key
        self._api_ops = api_ops
        self._client_session = None

    def __enter__(self):
        self._client_session = self._create_connection()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._client_session.close()

    def _build_api_url(self, endpoint):
        api_version = self._api_ops.get('api_version', 'v2')
        return "https://api.dataforseo.com/%s/%s" % (api_version, endpoint)

    def _build_headers(self):
        return {'Authorization': self._api_key, 'Content-Type': 'application/json'}

    @staticmethod
    def _create_connection():
        return requests.Session()

    @staticmethod
    def _handle_api_response(resp):
        if resp.status_code == 200:
            response_json = resp.json()
            if response_json.get('status') != 'ok':
                raise DfsApiException("API responded with status %s" % response_json.get('status'))
            return response_json.get('results')
        else:
            raise DfsApiException("API responded with HTTP code %s" % resp.status)

    def _post_json(self, json, endpoint):
        return self._handle_api_response(
            self._client_session.post(self._build_api_url(endpoint), json=json, headers=self._build_headers())
        )

    def _get_json(self, endpoint):
        return self._handle_api_response(
            self._client_session.get(self._build_api_url(endpoint), headers=self._build_headers())
        )

    def create_serp_tasks(self, serp_requests: List[SerpRequest]) -> Dict[str, str]:
        """
        Creates SERP task inside DataForSeo
        :return task id of the created task
        :raises DfsApiException when there's a non-ok response from the API
        """
        logger.debug("Creating SERP tasks for requests: %s", serp_requests)
        payload = {
            r.get_id(): {
                'key': r.keywords,
                'loc_name_canonical': r.location,
                'se_name': self._api_ops.get('se_name', 'google.pl'),
                'se_language': self._api_ops.get('se_language', 'Polish'),
                'priority': self._api_ops.get('priority', 1),
            } for r in serp_requests}

        result = self._post_json({'data': payload}, 'srp_tasks_post')
        tasks = {request_id: task.get('task_id') for request_id, task in result.items()}

        if logger.isEnabledFor(DEBUG):
            logger.debug("Registered SERP tasks: %s", {tasks.get(req.get_id()): req for req in serp_requests})

        return tasks

    def get_serp_task(self, task_id) -> Optional[SerpResponse]:
        """
        Gets the result of a SERP task from the DataForSeo API or null if the response is not (yet) there
        """
        logger.debug('Collecting results for task %s', task_id)
        res = self._get_json('srp_tasks_get/%s' % task_id)

        if res and res.get('organic'):
            listing = [SerpPosition(o['result_position'], o['result_url'], o['result_title']) for o in res['organic']]
            return SerpResponse(listing, [])

        return None

    def get_finished_tasks(self) -> [int]:
        response = self._get_json('srp_tasks_get')
        return [result.get('task_id') for result in response]

    def wait_for_results(self, task_id) -> Optional[SerpResponse]:
        """
        Awaits for results of given tasks and then returns the result.

        This method will try to collect the result of the given task immediately and if there are no
        results it will put itself into sleep for configured amount of time and try again. This process is repeated
        up to the configured amount of times.
        """
        result = self.get_serp_task(task_id)
        tries = self._api_ops.get('api_wait_tries', 10)
        interval = self._api_ops.get('api_wait_time', 30)

        for i in range(tries):
            if result:
                return result

            logger.debug("Waiting for task %s. Try: %s/%s", task_id, i, tries)
            sleep(interval)
            result = self.get_serp_task(task_id)

        logger.warning("Waiting for task %s timed out", task_id)
        return None

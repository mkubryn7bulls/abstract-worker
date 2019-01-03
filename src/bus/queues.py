from bus.api import Queue

QUEUE_LIGHTHOUSE_COMPUTE = Queue('lighthouse-compute')
QUEUE_PERSIST = Queue('persist')

SERP_CREATE_TASKS = Queue('serp-create-tasks')
SERP_COLLECT_FINISHED_TASKS = Queue('serp-collect-finished-tasks', max_length=1)
SERP_COLLECT_RESULTS = Queue('serp-collect-results')

from bus.api import Queue

QUEUE_LIGHTHOUSE_COMPUTE = Queue('lighthouse-compute')
QUEUE_PERSIST = Queue('persist')

SERP_REQUESTS = Queue('serp-requests')
SERP_DFS_COLLECT_FINISHED_TASKS = Queue('serp-dfs-collect-finished-tasks', max_length=1)
SERP_DFS_COLLECT_TASK_RESULTS = Queue('serp-dfs-collect-task-results')

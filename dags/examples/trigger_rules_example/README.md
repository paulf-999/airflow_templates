## Trigger Rules Example

**Description**:    Example showing how trigger rules work. Where the trigger rule options consist of:

* `all_success` (default) - gets triggered when all upstream tasks have succeeded.
* `all_failed` - task gets triggered if all of its parent tasks have failed.
* `all_done` - trigger your task once all tasks are done, regardless of their state. Potentially useful if there is a task that you always want to execute regardless of the upstream task’s states
* `one_failed` (see example) - As soon as one of the upstream tasks fails, your task gets triggered. Can be useful if you have some long running tasks and want to do something as soon as one fails.
* `one_success` - Like with one_failed, but the opposite. As soon as one of the upstream tasks succeeds, your task gets triggered.
* `none_failed` - Your task gets triggered if all upstream tasks have succeeded or been skipped. Only useful if you want to handle the skipped status.
* `none_failed_min_one_success` - your task gets triggered if all upstream tasks haven’t failed and at least one has succeeded.
* `none_skipped` - your task gets triggered if no upstream tasks are skipped. If they are all in success or failed.

See the following for more details: https://marclamberti.com/blog/airflow-trigger-rules-all-you-need-to-know/

**Date Created**:   28-11-2022

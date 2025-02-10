---
navigation_title: Transforms
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-troubleshooting.html
---

# Troubleshoot transforms [transform-troubleshooting]

Use the information in this section to troubleshoot common problems.

For issues that you cannot fix yourself … we’re here to help. If you are an existing Elastic customer with a support contract, please create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Or post in the [Elastic forum](https://discuss.elastic.co/).

If you encounter problems with your {{transforms}}, you can gather more information from the following files and APIs:

* Lightweight audit messages are stored in `.transform-notifications-read`. Search by your `transform_id`.
* The [get {{transform}} statistics API](https://www.elastic.co/guide/en/elasticsearch/reference/current/get-transform-stats.html) provides information about the {{transform}} status and failures.
* If the {{transform}} exists as a task, you can use the [task management API](https://www.elastic.co/guide/en/elasticsearch/reference/current/tasks.html) to gather task information. For example: `GET _tasks?actions=data_frame/transforms*&detailed`. Typically, the task exists when the {{transform}} is in a started or failed state.
* The {{es}} logs from the node that was running the {{transform}} might also contain useful information. You can identify the node from the notification messages. Alternatively, if the task still exists, you can get that information from the get {{transform}} statistics API. For more information, see [*Elasticsearch application logging*](../../deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md).


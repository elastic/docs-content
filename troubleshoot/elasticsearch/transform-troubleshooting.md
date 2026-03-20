---
navigation_title: Transforms
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-troubleshooting.html
applies_to:
  stack:
  serverless:
products:
  - id: elasticsearch
  - id: cloud-serverless
---

# Troubleshoot transforms [transform-troubleshooting]

Use the information in this section to troubleshoot common problems.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

If you encounter problems with your transforms, you can gather more information from the following files and APIs:

* Lightweight audit messages are stored in `.transform-notifications-read`. Search by your `transform_id`.
* The [get transform statistics API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-get-transform-stats) provides information about the transform status and failures.
* If the transform exists as a task, you can use the [task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks) to gather task information. For example: `GET _tasks?actions=data_frame/transforms*&detailed`. Typically, the task exists when the transform is in a started or failed state.
* {applies_to}`serverless: unavailable` The {{es}} logs from the node that was running the transform might also contain useful information. You can identify the node from the notification messages. Alternatively, if the task still exists, you can get that information from the get transform statistics API. For more information, refer to [](/deploy-manage/monitor/logging-configuration/elasticsearch-log4j-configuration-self-managed.md).


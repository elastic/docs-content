---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-monitoring-ece-set-retention.html
applies:
  ece: all
---

# Set the retention period for logging and metrics indices [ece-monitoring-ece-set-retention]

Elastic Cloud Enterprise sets up default index lifecycle management (ILM) policies on the logging and metrics indices it collects. By default, metrics indices are kept for one day and logging indices are kept for seven days. This retention period can be adjusted.

You might need to adjust the retention period for one of the following reasons:

* If your business requires you to retain logs and metrics for longer than the default period.
* If the volume of logs and metrics collected is high enough to require reducing the amount of storage space consumed.

To customize the retention period, set up a custom lifecycle policy for logs and metrics indices:

1. [Create a new index lifecycle management (ILM) policy](../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) in the logging and metrics cluster.
2. Create a new, legacy-style, index template that matches the data view (formerly *index pattern*) that you wish to customize lifecycle for.
3. Specify a lifecycle policy in the index template settings.
4. Choose a higher `order` for the template so the specified lifecycle policy will be used instead of the default.


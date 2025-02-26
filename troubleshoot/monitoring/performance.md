---
navigation_title: "Performance"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-scenario_why_is_performance_degrading_over_time.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echscenario_why_is_performance_degrading_over_time.html
---

# Troubleshoot performance degrading over time[ec-scenario_why_is_performance_degrading_over_time]

You have a smaller {{es}} cluster and you’ve noticed that performance seems to have declined recently. The response time during searches seems to have gone up, and overall the system just doesn’t seem to perform quite as well as it used to. You have already looked at the cluster performance metrics and have confirmed that both index and search response times have increased steadily and remained higher than before. So what explains the performance degradation?

When you look in the **Cluster Performance Metrics** section of the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), you get the following metrics:

:::{image} /images/cloud-metrics-credits.png
:alt: CPU usage versus CPU credits over time
:::

Between just after 00:10 and 00:20, excessively high CPU usage consumes all CPU credits until no more credits are available. CPU credits enable boosting the assigned CPU resources temporarily to improve performance on smaller clusters up to and including 8 GB of RAM when it is needed most, but CPU credits are by their nature limited. You accumulate CPU credits when you use less than your assigned share of CPU resources, and you consume credits when you use more CPU resources than assigned. As you max out your CPU resources, CPU credits permit your cluster to consume more than 100% of the assigned resources temporarily, which explains why CPU usage exceeds 100%, with usage peaks that reach well over 400% for one node. As CPU credits are depleted, CPU usage gradually drops until it returns to 100% at 00:30 when no more CPU credits are available. You can also notice that after 00:30 credits gradually begin to accumulate again.

If you need your cluster to be able to sustain a certain level of performance, you cannot rely on CPU boosting to handle the workload except temporarily. To ensure that performance can be sustained, consider increasing the size of your cluster.

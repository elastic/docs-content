---
navigation_title: "Cluster response time"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-scenario_why_are_my_cluster_response_times_suddenly_so_much_worse.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echscenario_why_are_my_cluster_response_times_suddenly_so_much_worse.html
---

# Troubleshoot slow cluster response time [ec-scenario_why_are_my_cluster_response_times_suddenly_so_much_worse]

Your {{es}} cluster is humming along nicely with good performance until you suddenly notice that response times increase substantially, for both index response times and search response times. The cluster is slow to respond for about 10 minutes, after which performance returns to a normal level.

Initially, you think that perhaps memory pressure is to blame, because you already know that [high memory pressure can cause performance issues](/troubleshoot/monitoring/high-memory-pressure.md). You look at the **Cluster Performance Metrics** section of the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body) and, after some zooming in to the right time frame, you get these metrics:

:::{image} /images/cloud-metrics-response-times.png
:alt: Cluster performance metrics
:::

Memory pressure is not the culprit. The **Memory Pressure per Node** metric is always well below 75%, and there is virtually no garbage collection overhead, which is consistent with low memory pressure. Similarly, CPU usage spiked and caused CPU boosting to kick in, but there were more than enough CPU credits to sustain the CPU usage spikes to over 300%. The cluster was not constrained by CPU resources, either.

So what caused the sudden increase in response times? The key to the puzzle lies in the **Number of Requests** metric, which indicates the number of requests that a cluster receives per second. Beginning shortly before 13:32, there was a substantial increase in the number of user requests per second. The number of requests per second continued to rise until the requests began to plateau as your cluster reached its maximum throughput, which in turn caused response times to rise. The number of requests remained at a high level for approximately five minutes, until they started to drop off again around 13:40. Overall, the sustained increase of user requests lasted a bit over 10 minutes, consistent with the slowdown you observed.

This cluster was sized to handle a certain number of user requests. As the user requests exceeded the maximum throughput that a cluster of this size could sustain, response times increased. To avoid such a slowdown, you either need to control the volume of user requests that reaches the {{es}} cluster or you need to size your cluster to be able to accommodate a sudden increase in user requests.
---
navigation_title: "High memory pressure"
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-metrics-memory-pressure.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-metrics-memory-pressure.html
---

# Troubleshoot high memory pressure

When you load up an {{es}} cluster with an indexing and search workload that matches the size of the cluster well, you typically get the classic JVM heap sawtooth pattern as memory gets used and then gets freed up again by the garbage collector. Memory usage increases until it reaches 75% and then drops again as memory is freed up:

:::{image} /images/cloud-metrics-memory-pressure-sawtooth.png
:alt: The classic JVM sawtooth pattern that shows memory usage
:::

Now let’s suppose you have a cluster with three nodes and much higher memory pressure overall. In this example, two of the three nodes are maxing out very regularly for extended periods and one node is consistently hovering around the 75% mark.

:::{image} /images/cloud-metrics-high-memory-pressure.png
:alt: High memory pressure
:::

High memory pressure works against cluster performance in two ways: As memory pressure rises to 75% and above, less memory remains available, but your cluster now also needs to spend some CPU resources to reclaim memory through garbage collection. These CPU resources are not available to handle user requests while garbage collection is going on. As a result, response times for user requests increases as the system becomes more and more resource constrained. If memory pressure continues to rise and reaches near 100%, a much more aggressive form of garbage collection is used, which will in turn affect cluster response times dramatically.

:::{image} /images/cloud-metrics-high-response-times.png
:alt: High response times
:::

In our example, the **Index Response Times** metric shows that high memory pressure leads to a significant performance impact. As two of the three nodes max out their memory several times and plateau at 100% memory pressure for 30 to 45 minutes at a time, there is a sharp increase in the index response times around 23:00, 00:00, and 01:00. Search response times, which are not shown, also increase but not as dramatically. Only the node in blue that consistently shows a much healthier memory pressure that rarely exceeds 75% can sustain a lower response time.

If the performance impact from high memory pressure is not acceptable, you need to increase the cluster size or reduce the workload.


## Increase the deployment size [ec_increase_the_deployment_size]

Scaling with {{ech}} is easy: simply log in to the {{ecloud}} Console, select your deployment, select edit, and either increase the number of zones or the size per zone.


## Reduce the workload [ec_reduce_the_workload]

By understanding and adjusting the way your data is indexed, retained, and searched you can reduce the amount of memory used and increase performance.


### Sharding strategy [ec_sharding_strategy]

{{es}} indices are divided into shards. Understanding shards is important when tuning {{es}}. Check [Size your shards](/deploy-manage/production-guidance/optimize-performance/size-shards.md) in the {{es}} documentation to learn more.


### Data retention [ec_data_retention]

The total amount of data being searched affects search performance. Check the tutorial [Automate rollover with index lifecycle management](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md) (ILM) to automate data retention policies.


### Tune for search speed [ec_tune_for_search_speed]

The documentation [Tune for search speed](/deploy-manage/production-guidance/optimize-performance/search-speed.md) provides details on how to analyze queries, optimize field types, minimize the fields searched, and more.

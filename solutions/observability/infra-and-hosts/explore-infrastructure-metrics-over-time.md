---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/explore-metrics.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Explore infrastructure metrics over time [explore-metrics]

The **Metrics Explorer** page enables you to create time-series visualizations based on aggregation of your metrics, chart them against related metrics, and break them down per the field of your choice. You can group and create visualizations of metrics for one or more resources that you are monitoring.

Additionally, for detailed analyses of your metrics, you can annotate and save visualizations for your custom dashboards by using the [Time Series Visual Builder (TSVB)](/explore-analyze/visualize/legacy-editors/tsvb.md) within {{kib}}.

To open **Metrics Explorer**, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

:::{image} /solutions/images/observability-metrics-explorer.png
:alt: Metrics Explorer
:screenshot:
:::

To learn more about the metrics shown on this page, refer to the [Metrics reference](/reference/observability/metrics-reference.md) documentation.

::::{tip}
If there are no metrics to display, {{kib}} prompts you to add a metrics integration. Click **Add a metrics integration** to get started. If you want to add more data in the future, click **Add data** from any page in the {{infrastructure-app}}.

Need help getting started? Follow the steps in [Get started with logs and metrics](get-started-with-system-metrics.md).

::::


By default, the Metrics Explorer page displays the CPU usage for hosts, Kubernetes pods, and Docker containers. The initial configuration has the **Average** aggregation selected, the **of** field is populated with the default metrics, and the **graph per** dropdown is set to `Everything`.

As an example, let’s view the system load metrics for hosts we’re currently monitoring.

1. In the **of** field, delete the selected metrics, and then add `system.load.1`, `system.load.5`, and `system.load.15`.

    The graph displays the average values of the metrics you selected.

2. In the **graph per** dropdown, add `host.name`.

    There is now an individual graph displaying the average values of the metrics for each host.

    :::{image} /solutions/images/observability-metrics-explorer-filter.png
    :alt: Metrics Explorer query
    :screenshot:
    :::

3. Select **Actions** in the top right-hand corner of one of the graphs and then click **Add filter**.

    This graph now displays the metrics only for that host. The filter has added a [{{kib}} Query Language](/explore-analyze/query-filter/languages/kql.md) filter for `host.name` in the second row of the Metrics Explorer configuration.

4. Let’s analyze some host-specific metrics. In the **of** field, delete each one of the system load metrics.
5. To explore the outbound network traffic, enter the `host.network.egress.bytes` metric. This is a monotonically increasing value, so from the aggregation dropdown, select `Rate`.
6. Hosts have multiple network interfaces, so it is more meaningful to display one graph for each network interface. From the **graph per** dropdown, add the `system.network.name` field.

    There is now a separate graph for each network interface.

7. Let’s visualize one of the graphs in [TSVB](/explore-analyze/visualize/legacy-editors/tsvb.md). Choose a graph, click **Actions**, and then select **Open In Visualize**.

    In this visualization the max of `host.network.egress.bytes` is displayed, filtered by `host.name` and `system.network.name`.

    :::{image} /solutions/images/observability-metrics-time-series.png
    :alt: Time series chart
    :screenshot:
    :::

    The `derivative` aggregation is used to calculate the difference between each bucket. By default, the value of units is automatically set to `1s`, along with the `positive only` aggregation.

8. To calculate the network traffic for all the interfaces, from the **group by** dropdown, select `Terms` and add the `system.network.name` field.
9. You will also need to add the **Series Agg** aggregation and the **Sum** function. From the **Aggregation** dropdown, select `Series Agg`, and from the **Function** dropdown, select `Sum`.
10. If you would like to save this visualization and add it to a custom dashboard later, click **Save**.

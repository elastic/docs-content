---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/legacy-editors.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Legacy editors [legacy-editors]

Legacy editors are still available but have been replaced by better alternatives. Consider using one of the [modern editors](../visualize.md) offered in Elastic such as **Lens**.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
To create a legacy visualization, navigate to the **Dashboards** page, go to **Visualizations** > **Create visualization** > **Legacy**, then select **TSVB** or **Aggregation-based**. Consider using [Lens](../visualize.md) instead if you have never used these panel types.

:::

:::{applies-item} stack: ga 9.0-9.3
To create a legacy visualization, click the {icon}`search` **Search** icon on the menu bar and search for **Visualize library**. Select **Create visualization** > **Legacy**, then select **TSVB** or **Aggregation-based**. Consider using [Lens](../visualize.md) instead if you have never used these panel types.
:::

::::


The legacy editors are:

- [Aggregation-based](legacy-editors/aggregation-based.md)
- [TSVB](legacy-editors/tsvb.md)
- [Timelion](legacy-editors/timelion.md)
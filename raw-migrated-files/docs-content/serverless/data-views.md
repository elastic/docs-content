# {{data-sources-cap}} [data-views]

This content applies to: [![Elasticsearch](../../../images/serverless-es-badge.svg "")](../../../solutions/search.md) [![Observability](../../../images/serverless-obs-badge.svg "")](../../../solutions/observability.md) [![Security](../../../images/serverless-sec-badge.svg "")](../../../solutions/security/elastic-security-serverless.md)

A {{data-source}} can point to one or more indices, [data streams](../../../manage-data/data-store/index-types/data-streams.md), or [index aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/alias.html). For example, a {{data-source}} can point to your log data from yesterday or all indices that contain your data.


## Create a data view [data-views-create-a-data-view]

After you’ve loaded your data, follow these steps to create a {{data-source}}:

1. Go to **{{project-settings}} → {{manage-app}} → {{data-views-app}}**. Alternatively, go to **Discover** and open the data view menu.

    ![How to set the {{data-source}} in Discover](../../../images/serverless-discover-find-data-view.png "")

2. Click **Create a {{data-source}}**.
3. Give your {{data-source}} a name.
4. Start typing in the **Index pattern** field, and Elastic looks for the names of indices, data streams, and aliases that match your input. You can view all available sources or only the sources that the data view targets.

    :::{image} ../../../images/serverless-discover-create-data-view.png
    :alt: Create data view
    :class: screenshot
    :::

    * To match multiple sources, use a wildcard (*). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
    * To match multiple single sources, enter their names, separated by a comma.  Do not include a space after the comma. `filebeat-a,filebeat-b` matches two indices.
    * To exclude a source, use a minus sign (-), for example, `-test3`.

5. Open the **Timestamp field** dropdown, and then select the default field for filtering your data by time.

    * If you don’t set a default time field, you can’t use global time filters on your dashboards. This is useful if you have multiple time fields and want to create dashboards that combine visualizations based on different timestamps.
    * If your index doesn’t have time-based data, choose **I don’t want to use the time filter**.

6. Click **Show advanced settings** to:

    * Display hidden and system indices.
    * Specify your own {{data-source}} name. For example, enter your {{es}} index alias name.

7. Click **Save {{data-source}} to Elastic**.

You can manage your data views in **{{project-settings}} → {{manage-app}} → {{data-views-app}}**.


### Create a temporary {{data-source}} [data-views-create-a-temporary-data-source]

Want to explore your data or create a visualization without saving it as a data view? Select **Use without saving** in the **Create {{data-source}}** form in **Discover**. With a temporary {{data-source}}, you can add fields and create an {{es}} query alert, just like you would a regular {{data-source}}. Your work won’t be visible to others in your space.

A temporary {{data-source}} remains in your space until you change apps, or until you save it.

::::{admonition} Temporary {{data-sources}} are not available in the {{data-views-app}} app.
:class: note


::::



## Delete a {{data-source}} [data-views-delete-a-data-source]

When you delete a {{data-source}}, you cannot recover the associated field formatters, runtime fields, source filters, and field popularity data. Deleting a {{data-source}} does not remove any indices or data documents from {{es}}.

::::{admonition} Deleting a {{data-source}} breaks all visualizations, saved searches, and other saved objects that reference the data view.
:class: important


::::


1. Go to **{{project-settings}} → {{manage-app}} → {{data-views-app}}**.
2. Find the {{data-source}} that you want to delete, and then click ![Delete](../../../images/serverless-trash.svg "") in the **Actions** column.

---
description: Create a Kibana data view so Discover, Lens, and other analytics features can access your Elasticsearch indices, data streams, or aliases.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Create a data view [settings-create-pattern]

Create a {{data-source}} to make your own {{es}} data available in **Discover**, **Lens**, and other analytics features.

## Before you begin [create-data-view-prereqs]

* You need a role with the `Data View Management` {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
* If a read-only indicator appears, you don't have sufficient privileges to create or save {{data-sources}}, and the buttons to do so aren't visible.
* You need data already indexed into {{es}}. Some workflows create a {{data-source}} for you automatically instead — refer to [Data views](../data-views.md#data-views-how-you-get-one).

## Create a data view [create-data-view-steps]

1. Open **Lens** or **Discover**, and then open the data view menu.

   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: How to set the {{data-source}} in Discover
   :screenshot:
   :width: 50%
   :::

2. Select **Create a {{data-source}}**.
3. Give your {{data-source}} a name.
4. Start entering text in the **Index pattern** field, and {{kib}} looks for the names of indices, data streams, and aliases that match your input. You can view all available sources or only the sources that the data view targets.
   ![Create data view](/explore-analyze/images/kibana-create-data-view.png "")

    * To match multiple sources, use a wildcard (*). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
    * To match multiple single sources, enter their names, separated by a comma. Do not include a space after the comma. `filebeat-a,filebeat-b` matches two indices.
    * To exclude a source, use a minus sign (-), for example, `-test3`.
    * To search across clusters or projects, or to point to a rollup index, refer to [Data view search syntax](data-view-search-syntax.md).

5. Open the **Timestamp field** dropdown, and then select the default field for filtering your data by time.

    * If you don't set a default time field, you can't use global time filters on your dashboards. This is useful if you have multiple time fields and want to create dashboards that combine visualizations based on different timestamps.
    * If your index doesn't have time-based data, select **I don't want to use the time filter**.

6. Select **Show advanced settings** to:

    * Allow hidden and system indices.
    * Set a **Custom data view ID**. By default, {{kib}} assigns a randomly generated ID to the {{data-source}} saved object. Setting a custom, human-readable ID (for example, `logs-prod`) makes the {{data-source}} easier to recreate with the same ID across spaces, deployments, or environments, so that dashboards and visualizations that reference it keep working. Refer to [Manage dashboards as code](/explore-analyze/dashboards/manage-dashboards-as-code.md) for how stable IDs keep dashboards portable.

7. $$$reload-fields$$$ Select **Save {{data-source}} to {{kib}}**.

You can now select your new {{data-source}} from the data view menu in **Discover**, **Lens**, and other analytics features. Manage it from the **Data Views** page under the **Management** menu.

## Create a temporary {{data-source}} [_create_a_temporary_data_source]

Want to explore your data or create a visualization without saving it as a data view? Select **Use without saving** in the **Create {{data-source}}** form in **Discover** or **Lens**. With a temporary {{data-source}}, you can add fields and create an {{es}} query alert, the same way you would with a regular {{data-source}}. Your work isn't visible to others in your space.

A temporary {{data-source}} remains in your space until you change apps, or until you save it.

:::{image} /explore-analyze/images/ad-hoc-data-view.gif
:alt: how to create an ad-hoc data view
:screenshot:
:::

::::{note}
Temporary {{data-sources}} aren't available in the **Management** menu.
::::

## Related pages

* [Data view search syntax](data-view-search-syntax.md)
* [Data views](../data-views.md)
* [Delete a data view](delete-data-view.md)
* [Duplicate a data view](duplicate-data-view.md)

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

* You need a role with the **Data View Management** {{kib}} privilege and the `view_index_metadata` {{es}} privilege. Refer to [Defining roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md).
* If a **Read only** badge appears, you don't have sufficient privileges to create or save {{data-sources}}. The create control is unavailable.
* You need data already indexed into {{es}}. Some workflows create a {{data-source}} for you automatically instead. Refer to [How data views are created](../data-views.md#data-views-how-you-get-one).

## Create the data view [create-data-view-steps]

1. Open the create form:

   * In **Discover** or **Lens**, open the data view menu, then select **Create a {{data-source}}**.
   * Go to the **Data Views** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Create data view**.

   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: Data view menu in Discover, with the current data view selected
   :screenshot:
   :width: 50%
   :::

2. In the **Name** field, enter a name for the {{data-source}}.
3. In the **Index pattern** field, enter a pattern. {{kib}} looks for the names of indices, data streams, and aliases that match your input. You can view all available sources or only the sources that the data view targets.

   ![Create data view](/explore-analyze/images/kibana-create-data-view.png "")

    * To match multiple sources, use a wildcard (`*`). `filebeat-*` matches `filebeat-apache-a`, `filebeat-apache-b`, and so on.
    * To match several individual sources, enter their names, separated by a comma, with no space after the comma. `filebeat-a,filebeat-b` matches two indices.
    * To exclude a source, use a minus sign (`-`), for example `-test3`.
    * To search across clusters or projects, or to point to a rollup index, refer to [Data view search syntax](data-view-search-syntax.md).

4. Open the **Timestamp field** menu, then select the default field for filtering your data by time.

    * If you don't set a default time field, you can't use global time filters on your dashboards. Skip a default time field when you have multiple time fields and want to combine visualizations that use different timestamps.
    * If your index doesn't have time-based data, select **I don't want to use the time filter**.

5. Select **Show advanced settings** to:

    * Allow hidden and system indices.
    * Set a **Custom data view ID**. By default, {{kib}} assigns a randomly generated ID to the {{data-source}} saved object. A custom, human-readable ID (for example, `logs-prod`) makes the {{data-source}} easier to recreate with the same ID across spaces, deployments, or environments. Dashboards and visualizations that reference that ID keep working. Refer to [Manage dashboards as code](/explore-analyze/dashboards/manage-dashboards-as-code.md).

6. $$$reload-fields$$$ Select **Save {{data-source}} to {{kib}}**.

You can now select your new {{data-source}} from the data view menu in **Discover**, **Lens**, and other analytics features. Manage it from the **Data Views** management page.

## Create a temporary {{data-source}} [_create_a_temporary_data_source]

To explore data or build a visualization without saving a {{data-source}}, select **Use without saving** in the **Create {{data-source}}** form in **Discover** or **Lens**. With a temporary {{data-source}}, you can add fields and create an {{es}} query alert, the same way you would with a saved {{data-source}}. Your work isn't visible to others in your space.

A temporary {{data-source}} remains in your space until you change apps, or until you save it.

:::{image} /explore-analyze/images/ad-hoc-data-view.gif
:alt: Create a temporary data view in Discover using Use without saving
:screenshot:
:::

::::{note}
Temporary {{data-sources}} aren't available on the **Data Views** management page. **Use without saving** appears only in **Discover** and **Lens**.
::::

## Related pages

* [Data view search syntax](data-view-search-syntax.md)
* [Data views](../data-views.md)
* [Delete a data view](delete-data-view.md)
* [Duplicate a data view](duplicate-data-view.md)

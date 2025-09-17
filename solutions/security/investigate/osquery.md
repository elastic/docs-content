---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/use-osquery.html
  - https://www.elastic.co/guide/en/serverless/current/security-query-operating-systems.html
  - https://www.elastic.co/guide/en/kibana/current/osquery.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
  - id: kibana
---

# Osquery [osquery]

[Osquery](https://osquery.io) is an open source tool that lets you query operating systems like a database, providing you with visibility into your infrastructure and operating systems. Using basic SQL commands, you can ask questions about devices, such as servers, Docker containers, and computers running Linux, macOS, or Windows. The [extensive schema](https://osquery.io/schema) helps with a variety of use cases, including vulnerability detection, compliance monitoring, incident investigations, and more.

With Osquery, you can:

* Run live queries for one or more agents
* Schedule query packs to capture changes to OS state over time
* View a history of past queries and their results
* Save queries and build a library of queries for specific use cases

To use Osquery, you must add the [Osquery manager integration](manage-integration.md) to an {{agent}} policy. After completing that step, you can use the Osquery features that are available in your solution.

% The following Osquery features are available from {{elastic-sec}}:

% * **[Osquery Response Actions](/solutions/security/investigate/add-osquery-response-actions.md)** - Use Osquery Response Actions to add live queries to custom query rules.
% * **[Live queries from investigation guides](/solutions/security/investigate/run-osquery-from-investigation-guides.md)** - Incorporate live queries into investigation guides to enhance your research capabilities while investigating possible security issues.
% * **[Live queries from alerts](/solutions/security/investigate/run-osquery-from-alerts.md)** - Run live queries against an alert’s host to learn more about your infrastructure and operating systems.

## Required privileges [required_osquery-privileges]

To use **Osquery Manager**, you must be assigned to a role with the following privileges:

* {applies_to}`stack: removed 9.2` {applies_to}`serverless: removed` `Read` privileges for the `logs-osquery_manager.result*` index.
* {{kib}} privileges for **Osquery Manager**. The `All` privilege enables you to run, schedule, and save queries. `Read` enables you to view live and scheduled query results, but you cannot run live queries or edit.


## Run live queries [osquery-run-query]

To inspect hosts, run a query against one or more agents or policies, then view the results.

1. Go to **Osquery** using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Live queries** view, click **New live query**.
3. Choose to run a single query or a query pack.
4. Select one or more agents or groups to query. Start typing in the search field, and you’ll get suggestions for agents by name, ID, platform, and policy.
5. Specify the query or pack to run:

    * **Query**: Select a saved query or enter a new one in the text box. After you enter the query, you can expand the **Advanced** section to set a timeout period for the query, and view or set [mapped ECS fields](#osquery-map-fields)  included in the results from the live query (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that require more time to complete. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
        ::::

    * **Pack**: Select from available query packs. After you select a pack, all of the queries in the pack are displayed.

        ::::{tip}
        Refer to [prebuilt packs](#osquery-prebuilt-packs) to learn about using and managing Elastic prebuilt packs.
        ::::


        :::{image} /solutions/images/kibana-enter-query.png
        :alt: Select saved query dropdown name showing query name and description
        :screenshot:
        :::

6. Click **Submit**.

    ::::{tip}
    To save a single query for future use, click **Save for later** and define the ID, description, and other [details](../../../solutions/security/investigate/osquery.md#osquery-manage-query).
    ::::

7. Review the results and do any of the following:

    * Click **View in Discover** (![View in Discover icon](/solutions/images/kibana-discover-button-osquery.png "title =20x20")) to explore the results in **Discover**.
    * Click **View in Lens** (![View in Lens icon](/solutions/images/kibana-lens-button-osquery.png "title =20x20")) to navigate to **Lens**, where you can use the drag-and-drop **Lens** editor to create visualizations.
    * Click **Add to Case** (![Add to Case icon](/solutions/images/kibana-case-button-osquery.png "title =20x20")) to add the query results to a new or existing case.
    * Click the view details icon (![View details icon](/solutions/images/kibana-view-osquery-details.png "title =20x20")) to examine the query ID and statement.

8. To view more information about the request, such as failures, open the **Status** tab.


## View or rerun previous live queries [osquery-view-history]

The **Live queries history** section on the **Live queries** tab shows a log of queries run over the last 30 days. From the Live queries table, you can:

* Click the run icon (![Right-pointing triangle](/solutions/images/kibana-play-icon.png "")) to rerun a single query or a query pack.
* Click the table icon (![Table icon](/solutions/images/kibana-table-icon.png "")) to examine the [results](#osquery-results) for a single query or a query pack. From the results table, you can also find the query [status](#osquery-status).

    :::{image} /solutions/images/kibana-live-query-check-results.png
    :alt: Results of OSquery
    :screenshot:
    :::



## Schedule queries with packs [osquery-schedule-query]

A pack is a set of grouped queries that perform similar functions or address common use cases. [Prebuilt Elastic packs](#osquery-prebuilt-packs) are available to download and can help you get started using the Osquery integration.

You can also create a custom pack with one or more queries. For example, when creating custom packs, you might create one pack that checks for IT compliance-type issues, and another pack that monitors for evidence of malware.

You can run packs as live queries or schedule packs to run for one or more agent policies. When scheduled, queries in the pack are run at the set intervals for all agents in those policies.

1. Click the **Packs** tab.
2. Click **Add pack** to create a new pack, or click the name of an existing pack, then **Edit** to add queries to an existing pack.
3. Provide a name for the pack. The short description is optional.
4. Schedule the pack to be deployed on specified agent policies (**Policy**) or on all agent policies (**Global**).

    ::::{tip}
    Pack deployment details are stored within the [Osquery configuration](/solutions/security/investigate/manage-integration.md#osquery-custom-config). The `shard` field value is the percentage of agents in the policy using the pack.
    ::::


    If you choose the **Policy** option, configure these fields:

    ::::{note}
    When defining pack deployment details, you cannot configure the same policy multiple times. In other words, after specifying a policy, you can either choose to deploy the pack to all of the policy’s agents or only a subset. You cannot choose both.
    ::::


    * **Scheduled {{agent}} policies (optional)**: Allows you to deploy the pack to specific agent policies. By default, the pack is deployed to all {{agents}} that are registered to the policies you define.
    * **Partial deployment (shards)**: Allows you to deploy the pack to a portion of the agents on each specified agent policy. After defining a policy, use the **Shard** slider to set the amount of agents to which the pack is deployed. For example, after specifying a policy, you can choose to deploy the pack to half of the policy’s agents by selecting 50% on the slider.

5. If you’re creating a new pack, add queries to schedule:

    * Click **Add query** and then add a saved query or enter a new query. Each query must include a unique query ID and the interval at which it should run. Optionally, set the minimum Osquery version and platform, specify a timeout period, or [map ECS fields](#osquery-map-fields). When you add a saved query to a pack, this adds a copy of the query. A connection is not maintained between saved queries and packs.

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that require more time to complete. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
        ::::

    * Upload queries from a `.conf` query pack by dragging the pack to the drop zone under the query table. To explore the community packs that Osquery publishes, click **Example packs**.

6. Click **Save pack**. The queries run when the policy receives the update.


## View status of scheduled packs [osquery-schedule-status]

1. Open the **Packs** tab.
2. Click a pack name to view the status.

    Details include the last time each query ran, how many results were returned, and the number of agents the query ran against. If there are errors, expand the row to view the details, including an option to view more information in the Logs.

    :::{image} /solutions/images/kibana-scheduled-pack.png
    :alt: Shows queries in the pack and details about each query
    :screenshot:
    :::

3. View scheduled query results in [**Discover**](../../../explore-analyze/discover.md) or the drag-and-drop [**Lens**](../../../explore-analyze/visualize/lens.md) editor.


## Save queries [osquery-manage-query]

You can save queries in two ways:

* After running a live query, click the **Save for later** link.
* From the **Saved queries** tab, click **Add saved query**.

Once you save a query, you can only edit it from the **Saved queries** tab:

1. Go to **Saved queries**, and then click **Add saved query** or the edit icon.
2. Provide the following fields:

    * The unique identifier (required).
    * A brief description.
    * The SQL query (required). Osquery supports multi-line queries.
    * A timeout period (optional). Increase the query’s default timeout period to support queries that require more time to complete. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
    * The [ECS fields](#osquery-map-fields) to populate when the query is run (optional). These fields are also copied in when you add this query to a pack.
    * The defaults to set when you add the query to a pack.

        * The frequency to run the query.
        * The minimum [version of Osquery](https://github.com/osquery/osquery/releases)) required to run the query.
        * The operating system required to run the query. For information about supported platforms per table, refer to the [Osquery schema](https://osquery.io/schema).

3. Click **Test configuration** to test the query and any mapped fields:

    * From the **Test query** panel, select agents or groups to test the query, then click **Submit** to run a live query. Result columns with the ![mapping](/solutions/images/kibana-mapped-icon.png "") icon are mapped. Hover over the icon to see the mapped ECS field.

4. Click **Save** or **Update**.


## Prebuilt Elastic packs and queries [osquery-prebuilt-packs-queries]

The prebuilt Osquery packs are included with the integration. Once you add a pack, you can activate and schedule it.


### Prebuilt packs [osquery-prebuilt-packs]

The prebuilt Osquery packs are included with the integration and can be optionally loaded. Once added, you can then activate and schedule the packs.

You can modify the scheduled agent policies for a prebuilt pack, but you cannot edit queries in the pack. To edit the queries, you must first create a copy of the pack.

For information about the prebuilt packs that are available, refer to [*Prebuilt packs reference*](kibana://reference/osquery-manager-prebuilt-packs.md).


#### Load and activate prebuilt Elastic packs [load-prebuilt-packs]

Follow these steps to load and turn on new or updated prebuilt packs:

1. Go to **Packs**, and then click **Load Elastic prebuilt packs**.
2. For each pack that you want to activate and schedule:

    * Turn on the **Active** toggle to ensure the pack runs continuously.

        ::::{note}
        You must manually run inactive packs.
        ::::

    * Click the pack name, then **Edit**.
    * Update the **Scheduled agent policies** to specify the policies where this pack should run.

3. Click **Update pack**.


#### Copy prebuilt Elastic packs [copy-prebuilt-packs]

To modify queries in prebuilt packs, you must first make a copy of the pack.

1. Go to **Stack Management** → **Saved Objects**.
2. Search for the Osquery packs you want to modify by name.
3. Select the checkboxes of the packs to export.
4. Click **Export x objects**.
5. Click **Import**.
6. Select the import option **Create new objects with random IDs**, then click **Import** to import the pack. This creates a copy of the pack that you can edit.


### Prebuilt queries [osquery-prebuilt-queries]

A set of saved queries are included with the integration and available to run as a live query. Note the following about the prebuilt queries:

* The queries are not editable.
* Several of the queries include default ECS mappings to standardize the results.
* The prebuilt Elastic queries all follow the same naming convention and identify what type of information is being queried, what operating system it supports if it’s limited to one or more, and that these are Elastic queries. For example, `firewall_rules_windows_elastic`.


## Map result fields to ECS [osquery-map-fields]

When you save queries or add queries to a pack, you can optionally map Osquery results or static values to fields in the [Elastic Common Schema](ecs://reference/index.md) (ECS). This standardizes your Osquery data for use across detections, machine learning, and any other areas that rely on ECS-compliant data. When the query is run, the results include the original `osquery.<fields>` and the mapped ECS fields. For example, if you update a query to map `osquery.name` to `user.name`, the query results include both fields.

1. Edit saved queries or queries in a pack to map fields:

    * For saved queries: Open the **Saved queries** tab, and then click the edit icon for the query that you want to map.
    * For packs: Open the **Packs** tab, edit a pack, and then click the edit icon for the query that you want to map.

2. In the **ECS mapping** section, select an **ECS field** to map.
3. In the **Value** column, use the dropdown on the left to choose what type of value to map to the ECS field:

    * **Osquery value**: Select an Osquery field. The fields available are based on the SQL query entered, and only include fields that the query returns. When the query runs, the ECS field is set dynamically to the value of the Osquery field selected.
    * **Static value**: Enter a static value. When the query runs, the ECS field is set to the value entered. For example, static fields can be used to apply `tags` or your preferred `event.category` to the query results.

4. Map more fields, as needed. To remove any mapped rows, click the delete icon.
5. Save your changes.

::::{note}
* Some ECS fields are restricted and cannot be mapped. These are not available in the ECS dropdown.
* Some ECS fields are restricted to a set of allowed values, like [event.category](ecs://reference/ecs-event.md#field-event-category). Use the [ECS Field Reference](ecs://reference/ecs-field-reference.md) for help when mapping fields.
* Osquery date fields have a variety of data types (including integer, text, or bigint). When mapping an Osquery date field to an ECS date field, you might need to use SQL operators in the query to get an {{es}}-compatible [date](elasticsearch://reference/elasticsearch/mapping-reference/date.md) type.

::::



## Extended tables for Kubernetes queries [osquery-extended-tables]

In addition to the Osquery schema, the Elastic-provided version of Osquery also includes the following tables to support Kubernetes containers. These can be queried with live or scheduled queries.

* `host_users`
* `host_groups`
* `host_processes`

When querying these tables, the expectation is that the `/etc/passwd`, `/etc/group`, and `/proc` are available in the container under `/hostfs` as: `/hostfs/etc/passwd`, `/hostfs/etc/group`, and `/hostfs/proc`. For information about the fields available in these tables, see the [exported fields](https://docs.elastic.co/en/integrations/osquery_manager#exported-fields) reference.


## Osquery status [osquery-status]

A query can have the following status:

|     |     |
| --- | --- |
| Successful | The query successfully completed. |
| Failed | The query encountered a problem, such as an issue with the query or the agent was disconnected, and might have failed. |
| Not yet responded | The query has not been sent to the agent. |
| Expired | The action request timed out. The agent may be offline. |

::::{note}
If an agent is offline, the request status remains **pending** as {{kib}} retries the request. By default, a query request times out after one minute. An action timeout error is returned when the query does not complete within that interval.
::::



## Osquery results [osquery-results]

When you run live or scheduled queries, the results are automatically stored in an {{es}} index, so that you can search, analyze, and visualize this data in {{kib}}. For a list of the Osquery fields that can be returned in query results, refer to [exported fields](https://docs.elastic.co/en/integrations/osquery_manager#exported-fields). Query results can also include ECS fields, if the query has a defined ECS mapping.

Osquery responses include the following information:

* Everything prefaced with `osquery.` is part of the query response. These fields are not mapped to ECS by default.
* Results include some ECS fields by default, such as `host.*` and `agent.*`, which provide information about the host that was queried.
* For live queries, the `action_data.query` is the query that was sent.
* For scheduled queries in a pack, the `action_id` has the format `pack_<pack-name>_<query-ID>`. You can use this information to look up the query that was run.
* By default, all query results are [snapshot logs](https://osquery.readthedocs.io/en/stable/deployment/logging/#snapshot-logs) that represent a point in time with a set of results, with no [differentials](https://osquery.readthedocs.io/en/stable/deployment/logging/#differential-logs).
* Osquery data is stored in the `logs-osquery_manager.result-<namespace>` datastream, and the result row data is under the `osquery` property in the document.





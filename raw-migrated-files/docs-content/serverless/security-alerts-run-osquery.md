# Run Osquery from alerts [security-alerts-run-osquery]

Run live queries on hosts associated with alerts to learn more about your infrastructure and operating systems. For example, with Osquery, you can search your system for indicators of compromise that might have contributed to the alert. You can then use this data to inform your investigation and alert triage efforts.

::::{admonition} Requirements
:class: note

* The [Osquery manager integration](../../../solutions/security/investigate/manage-integration.md) must be installed.
* {{agent}}'s [status](https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html) must be `Healthy`. Refer to [{{fleet}} Troubleshooting](../../../troubleshoot/ingest/fleet/common-problems.md) if it isn’t.
* You must have the appropriate user role to use this feature.

::::


To run Osquery from an alert:

1. Do one of the following from the Alerts table:

    * Click the **View details** button to open the Alert details flyout, then click **Take action → Run Osquery**.
    * Select the **More actions** menu (![Actions menu icon](../../../images/serverless-boxesHorizontal.svg "")), then select **Run Osquery**.

2. Choose to run a single query or a query pack.
3. Select one or more {{agent}}s or groups to query. Start typing in the search field to get suggestions for {{agent}}s by name, ID, platform, and policy.

    ::::{note}
    The host associated with the alert is automatically selected. You can specify additional hosts to query.

    ::::

4. Specify the query or pack to run:

    * **Query**: Select a saved query or enter a new one in the text box. After you enter the query, you can expand the **Advanced** section to set a timeout period for the query, and view or set [mapped ECS fields](../../../solutions/security/investigate/osquery.md#osquery-map-fields) included in the results from the live query (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `900`.

        ::::


        ::::{tip}
        Use [placeholder fields](../../../solutions/security/investigate/use-placeholder-fields-in-osquery-queries.md) to dynamically add existing alert data to your query.

        ::::

    * **Pack**: Select from available query packs. After you select a pack, all of the queries in the pack are displayed.

        ::::{tip}
        Refer to [prebuilt packs](../../../solutions/security/investigate/osquery.md#osquery-prebuilt-packs-queries) to learn about using and managing Elastic prebuilt packs.

        ::::


        ![Shows how to set up a single query](../../../images/serverless--osquery-setup-query.png "")

5. Click **Submit**. Query results will display within the flyout.

    ::::{note}
    Refer to [Examine Osquery results](../../../solutions/security/investigate/examine-osquery-results.md) for more information about query results.

    ::::

6. Click **Save for later** to save the query for future use (optional).

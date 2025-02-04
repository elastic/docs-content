# Run Osquery from investigation guides [security-invest-guide-run-osquery]

Detection rule investigation guides suggest steps for triaging, analyzing, and responding to potential security issues. When you build a custom rule, you can also set up an investigation guide that incorporates Osquery. This allows you to run live queries from a rule’s investigation guide as you analyze alerts produced by the rule.

::::{admonition} Requirements
:class: note

* The [Osquery manager integration](../../../solutions/security/investigate/manage-integration.md) must be installed.
* {{agent}}'s [status](https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html) must be `Healthy`. Refer to [{{fleet}} Troubleshooting](../../../troubleshoot/ingest/fleet/common-problems.md) if it isn’t.
* You must have the appropriate user role to use this feature.

::::


:::{image} ../../../images/serverless--osquery-osquery-investigation-guide.png
:alt: Shows a live query in an investigation guide
:class: screenshot
:::


## Add live queries to an investigation guide [add-live-queries-ig]

::::{note}
You can only add Osquery to investigation guides for custom rules because prebuilt rules cannot be edited.

::::


1. Go to **Rules** → **Detection rules (SIEM)**, select a rule, then click **Edit rule settings** on the rule details page.
2. Select the **About** tab, then expand the rule’s advanced settings.
3. Scroll down to the Investigation guide section. In the toolbar, click the **Osquery** button (![Click the Osquery button](../../../images/serverless--osquery-osquery-button.png "")).

    1. Add a descriptive label for the query; for example, `Search for executables`.
    2. Select a saved query or enter a new one.

        ::::{tip}
        Use [placeholder fields](../../../solutions/security/investigate/use-placeholder-fields-in-osquery-queries.md) to dynamically add existing alert data to your query.

        ::::

    3. Expand the **Advanced** section to set a timeout period for the query, and view or set [mapped ECS fields](../../../solutions/security/investigate/osquery.md#osquery-map-fields) included in the results from the live query (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `900`.

        ::::


        ![ osquery setup osquery investigation guide](../../../images/serverless--osquery-setup-osquery-investigation-guide.png "")[height=70%][Shows results from running a query from an investigation guide]

4. Click **Save changes** to add the query to the rule’s investigation guide.


## Run live queries from an investigation guide [run-live-queries-ig]

1. Go to **Rules** → **Detection rules (SIEM)**, then select a rule to open its details.
2. Go to the About section of the rule details page and click **Investigation guide**.
3. Click the query. The Run Osquery pane displays with the **Query** field autofilled. Do the following:

    1. Select one or more {{agent}}s or groups to query. Start typing in the search field to get suggestions for {{agent}}s by name, ID, platform, and policy.
    2. Expand the **Advanced** section to set a timeout period for the query, and view or set the [mapped ECS fields](../../../solutions/security/investigate/osquery.md#osquery-map-fields) which are included in the live query’s results (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `900`.

        ::::

4. Click **Submit** to run the query. Query results display in the flyout.

    ::::{note}
    Refer to [Examine Osquery results](../../../solutions/security/investigate/examine-osquery-results.md) for more information about query results.

    ::::

5. Click **Save for later** to save the query for future use (optional).

    ![ osquery run query investigation guide](../../../images/serverless--osquery-run-query-investigation-guide.png "")[height=80%][Shows results from running a query from an investigation guide]

---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/invest-guide-run-osquery.html
  - https://www.elastic.co/guide/en/serverless/current/security-invest-guide-run-osquery.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Run Osquery from investigation guides [security-invest-guide-run-osquery]

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/invest-guide-run-osquery.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-invest-guide-run-osquery.md

Detection rule investigation guides suggest steps for triaging, analyzing, and responding to potential security issues. When you build a custom rule, you can also set up an investigation guide that incorporates Osquery. This allows you to run live queries from a rule’s investigation guide as you analyze alerts produced by the rule.

::::{admonition} Requirements
* The [Osquery manager integration](/solutions/security/investigate/manage-integration.md) must be installed.
* {{agent}}'s [status](/reference/fleet/monitor-elastic-agent.md) must be `Healthy`. Refer to [](/troubleshoot/ingest/fleet/common-problems.md) if it isn’t.
* In {{stack}}, your role must have [Osquery feature privileges](/solutions/security/investigate/osquery.md).
* In {{serverless-short}}, you must have the appropriate user role to use this feature.

::::


:::{image} /solutions/images/security-osquery-investigation-guide.png
:alt: Shows a live query in an investigation guide
:screenshot:
:::


## Add live queries to an investigation guide [add-live-queries-ig]

::::{note}
You can only add Osquery to investigation guides for custom rules because prebuilt rules cannot be edited.
::::


1. Go to the **Rules** page. To access it, find **Detection rules (SIEM)** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select a rule to open the its details, then click **Edit rule settings**.
3. Select the **About** tab, then expand the rule’s advanced settings.
4. Scroll down to the Investigation guide section. In the toolbar, click the **Osquery** button (![Click the Osquery button](/solutions/images/security-osquery-button.png "title =20x20")).

    1. Add a descriptive label for the query; for example, `Search for executables`.
    2. Select a saved query or enter a new one.

        ::::{tip}
        Use [placeholder fields](/solutions/security/investigate/use-placeholder-fields-in-osquery-queries.md) to dynamically add existing alert data to your query.
        ::::

    3. Expand the **Advanced** section to set a timeout period for the query, and view or set [mapped ECS fields](/solutions/security/investigate/osquery.md#osquery-map-fields) included in the results from the live query (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
        ::::


        :::{image} /solutions/images/security-setup-osquery-investigation-guide.png
        :alt: Shows results from running a query from an investigation guide
        :screenshot:
        :::

5. Click **Save changes** to add the query to the rule’s investigation guide.


## Run live queries from an investigation guide [run-live-queries-ig]

1. Go to the **Rules** page. To access it, find **Detection rules (SIEM)** in the main menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select a rule to open the its details.
3. Go to **Rules** → **Detection rules (SIEM)**, then select a rule to open its details.
4. Go to the About section of the rule details page and click **Investigation guide**.
5. Click the query. The Run Osquery pane displays with the **Query** field autofilled. Do the following:

    1. Select one or more {{agent}}s or groups to query. Start typing in the search field to get suggestions for {{agent}}s by name, ID, platform, and policy.
    2. Expand the **Advanced** section to set a timeout period for the query, and view or set [mapped ECS fields](/solutions/security/investigate/osquery.md#osquery-map-fields) included in the results from the live query (optional).

        ::::{note}
        Overwriting the query’s default timeout period allows you to support queries that take longer to run. The default and minimum supported value for the **Timeout** field is `60`. The maximum supported value is `86400` (24 hours).
        ::::

6. Click **Submit** to run the query. Query results display in the flyout.

    ::::{note}
    Refer to [Examine Osquery results](/solutions/security/investigate/examine-osquery-results.md) for more information about query results.
    ::::

7. Click **Save for later** to save the query for future use (optional).

    :::{image} /solutions/images/security-run-query-investigation-guide.png
    :alt: Shows results from running a query from an investigation guide
    :screenshot:
    :::

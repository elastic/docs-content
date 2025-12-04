---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create a detection rule [security-rules-create]

To create a new detection rule, follow these steps:

1. Define the [**rule type**](/solutions/security/detect-and-alert/about-detection-rules.md#rule-types). The configuration for this step varies depending on the rule type.
2. Configure basic rule settings.
3. Configure advanced rule settings (optional).
4. Set the rule’s schedule.
5. Set up rule actions (optional).
6. Set up response actions (optional).

::::{admonition} Requirements
To create detection rules, you must have:

* Access to data views, which requires the `Data View Management` [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
* Permissions to enable and view detections, manage rules, manage alerts, and preview rules. These permissions depend on the user role. Refer to [Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md) for more information.

::::


::::{tip}
* At any step, you can [preview the rule](/solutions/security/detect-and-alert/create-detection-rule.md#preview-rules) before saving it to see what kind of results you can expect.
* To ensure rules don’t search cold and frozen data when executing, either configure the `excludedDataTiersForRuleExecution` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#exclude-cold-frozen-data-rule-executions) (which applies to all rules in a space), or add a [Query DSL filter](/solutions/security/detect-and-alert/exclude-cold-frozen-data-from-individual-rules.md) to individual rules. These options are only available if you're on the {{stack}}.

::::


::::{note}
Additional configuration is required for detection rules using cross-cluster search. Refer to [Cross-cluster search and detection rules](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md).
::::

## Create a custom query rule [create-custom-rule]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a KQL or Lucene query, select **Custom query** on the **Create new rule** page, then:

    1. Define which {{es}} indices or data view the rule searches for alerts.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        The following example (based on the prebuilt rule [Volume Shadow Copy Deleted or Resized via VssAdmin](https://www.elastic.co/guide/en/security/8.17/prebuilt-rule-0-14-2-volume-shadow-copy-deleted-or-resized-via-vssadmin.html)) detects when the `vssadmin delete shadows` Windows command is executed:

        * **Index patterns**: `winlogbeat-*`

            Winlogbeat ships Windows event logs to {{elastic-sec}}.

        * **Custom query**: `event.action:"Process Create (rule: ProcessCreate)" and process.name:"vssadmin.exe" and process.args:("delete" and "shadows")`

            Searches the `winlogbeat-*` indices for `vssadmin.exe` executions with the `delete` and `shadow` arguments, which are used to delete a volume’s shadow copies.

            :::{image} /solutions/images/security-rule-query-example.png
            :alt: Rule query example
            :screenshot:
            :::

    3. You can use {{kib}} saved queries (![Saved query menu](/solutions/images/security-saved-query-menu.png "title =20x20")) and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.

        When you use a saved query, the **Load saved query "*query name*" dynamically on each rule execution** check box appears:

        * Select this to use the saved query every time the rule runs. This links the rule to the saved query, and you won’t be able to modify the rule’s **Custom query** field or filters because the rule will only use settings from the saved query. To make changes, modify the saved query itself.
        * Deselect this to load the saved query as a one-time way of populating the rule’s **Custom query** field and filters. This copies the settings from the saved query to the rule, so you can then further adjust the rule’s query and filters as needed. If the saved query is later changed, the rule will not inherit those changes.

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).

## Create a machine learning rule [create-ml-rule]

::::{admonition} Requirements
To create or edit {{ml}} rules, you need:
* The appropriate [{{stack}} subscription](https://www.elastic.co/pricing) or [{{serverless-short}} project feature tier](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
* The [`machine_learning_admin`](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-ml-admin) in {{stack}} or the appropriate [user role](/deploy-manage/users-roles/cloud-organization/user-roles.md) in {{serverless-short}}.
* The selected {{ml}} job to be running for the rule to function correctly.
::::

::::{tip}
For an overview of using {{ml}} with {{elastic-sec}}, refer to [Anomaly detection](/solutions/security/advanced-entity-analytics/anomaly-detection.md).
::::


1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a {{ml}} anomaly threshold, select **Machine Learning** on the **Create new rule** page, then select:

    1. The required {{ml}} jobs.

        ::::{note}
        If a required job isn’t currently running, it will automatically start when you finish configuring and enable the rule.
        ::::

    2. The anomaly score threshold above which alerts are created.

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.

    ::::{note}
    Because {{ml}} rules generate alerts from anomalies, which don’t contain source event fields, you can only use anomaly fields when configuring alert suppression.
    ::::

4. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

5. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).

::::{tip}
To filter noisy {{ml}} rules, use [rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md).
::::

## Create a threshold rule [create-threshold-rule]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a source event field threshold, select **Threshold**, then:

    1. Define which {{es}} indices the rule analyzes for alerts.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        ::::{note}
        You can use {{kib}} saved queries (![Saved query menu](/solutions/images/security-saved-query-menu.png "title =20x20")) and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.
        ::::

    3. Use the **Group by** and **Threshold** fields to determine which source event field is used as a threshold and the threshold’s value.

        ::::{note}
        Consider the following when using the **Group by** field:
        - Nested fields are not supported.
        - High cardinality in the fields or a high number of matching documents can result in a rule timeout or a circuit breaker error from {{es}}.
        ::::

    4. Use the **Count** field to limit alerts by cardinality of a certain field.

        For example, if **Group by** is `source.ip, destination.ip` and its **Threshold** is `10`, an alert is generated for every pair of source and destination IP addresses that appear in at least 10 of the rule’s search results.

        You can also leave the **Group by** field undefined. The rule then creates an alert when the number of search results is equal to or greater than the threshold value. If you set **Count** to limit the results by `process.name` >= 2, an alert will only be generated for source/destination IP pairs that appear with at least 2 unique process names across all events.

        ::::{important}
        Alerts created by threshold rules are synthetic alerts that do not resemble the source documents:
        
          - The alert itself only contains data about the fields that were aggregated over (the **Group by** fields specified in the rule).
          - All other fields are omitted and aren't available in the alert. This is because these fields can vary across all source documents that were counted toward the threshold. 
          - You can reference the actual count of documents that exceeded the threshold from the `kibana.alert.threshold_result.count` field. 
          - `context.alerts.kibana.alert.threshold_result.terms` contains fields and values from any **Group by** fields specified in the rule. For example:
        ```
          {{#context.alerts}}
            {{#kibana.alert.threshold_result.terms}}
              {{field}}: {{value}}
            {{/kibana.alert.threshold_result.terms}}
         {{/context.alerts}}
       ```
        ::::

3. (Optional) Select **Suppress alerts** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


## Create an event correlation rule [create-eql-rule]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create an event correlation rule using EQL, select **Event Correlation** on the **Create new rule** page, then:

    1. Define which {{es}} indices or data view the rule searches when querying for events.
    2. Write an [EQL query](elasticsearch://reference/query-languages/eql/eql-syntax.md) that searches for matching events or a series of matching events.

        ::::{tip}
        To find events that are missing in a sequence, use the [missing events](elasticsearch://reference/query-languages/eql/eql-syntax.md#eql-missing-events) syntax.
        ::::


        For example, the following rule detects when `msxsl.exe` makes an outbound network connection:

        * **Index patterns**: `winlogbeat-*`

            Winlogbeat ships Windows events to {{elastic-sec}}.

        * **EQL query**:

            ```eql
            sequence by process.entity_id
              [process
                where event.type in ("start", "process_started")
                and process.name == "msxsl.exe"]
              [network
                where event.type == "connection"
                and process.name == "msxsl.exe"
                and network.direction == "outgoing"]
            ```

            Searches the `winlogbeat-*` indices for sequences of a `msxsl.exe` process start event followed by an outbound network connection event that was started by the `msxsl.exe` process.

            :::{image} /solutions/images/security-eql-rule-query-example.png
            :alt: eql rule query example
            :screenshot:
            :::

            ::::{note}
            For sequence events, the {{security-app}} generates a single alert when all events listed in the sequence are detected. To see the matched sequence events in more detail, you can view the alert in the Timeline, and, if all events came from the same process, open the alert in Analyze Event view.
            ::::

3. (Optional) Click the EQL settings icon (![EQL settings icon](/solutions/images/security-eql-settings-icon.png "title =20x20")) to configure additional fields used by [EQL search](/explore-analyze/query-filter/languages/eql.md#specify-a-timestamp-or-event-category-field):

    * **Event category field**: Contains the event classification, such as `process`, `file`, or `network`. This field is typically mapped as a field type in the [keyword family](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md). Defaults to the `event.category` ECS field.
    * **Tiebreaker field**: Sets a secondary field for sorting events (in ascending, lexicographic order) if they have the same timestamp.
    * **Timestamp field**: Contains the event timestamp used for sorting a sequence of events. This is different from the **Timestamp override** advanced setting, which is used for querying events within a range. Defaults to the `@timestamp` ECS field.

4. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
5. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

6. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

7. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


## Create an indicator match rule [create-indicator-rule]

::::{note}
{{elastic-sec}} provides [limited support](/solutions/security/detect-and-alert.md#support-indicator-rules) for indicator match rules.
::::

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.

2. To create a rule that continually compares your security source events with threat indicators and generates alerts when they meet the rule criteria that you specify, select **Indicator Match**, then configure the following:

    1. **Source**: The index patterns or data view that store your source event documents. The **Index patterns** field is prepopulated with indices that are set in the [default {{elastic-sec}} indices](/solutions/security/get-started/configure-advanced-settings.md#update-sec-indices). If you choose to use a **Data View**, you must specify one from the drop-down.  
    
    2. **Custom query**: The query and filters used to retrieve documents from your source event indices. Field values in these documents are compared against indicator values, according to the threat mapping conditions that you set.
    
        The default KQL query `*:*` retrieves every document in the specified event indices. You can modify the query as needed. For example, if you only want to retrieve documents that contain a `destination.ip` address field, enter `destination.ip : *`.

        ::::{tip}
        You can use saved queries and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.
        ::::

    3. **Indicator index patterns**: The index patterns that store your threat indicator documents. This field is prepopulated with indices specified in the [`securitySolution:defaultThreatIndex`](/solutions/security/get-started/configure-advanced-settings.md#update-threat-intel-indices) advanced setting.

        ::::{important}
        Data in threat indicator indices must be [ECS compatible](/reference/security/fields-and-object-schemas/siem-field-reference.md), and must contain a `@timestamp` field.
        ::::

    4. **Indicator index query**: The query used to retrieve documents from your threat indicator indices. Field values in these documents are compared against source event values, according to the threat mapping conditions that you set. 
    
        The default KQL query `@timestamp > "now-30d/d"` searches the threat indicator indices for threat intelligence indicators that were ingested during the past 30 days. The start time is rounded down to the nearest day (resolves to UTC `00:00:00`).

    5. **Indicator mapping**: Set threat mapping conditions that compare values in source event fields with values in threat indicator fields. Alerts are generated if the conditions are met.

        ::::{note}
        Only single-value fields are supported.
        ::::

        To specify fields to compare from your specified source event and threat indicator indices, create a threat mapping entry and configure the following:

        * **Field**: Select a field from your source event indices for comparison. 
        * {applies_to}`stack: ga 9.2` **MATCHES/DOES NOT MATCH**: Choose whether the source event field value should match or not match the threat indicator field value that it's being compared to.

            ::::{note}
            Define matching (`MATCHES`) conditions first, then narrow down your results even more by adding `DOES NOT MATCH` conditions to exclude field values that you want to ignore. Mapping entries that _only_ use the `DOES NOT MATCH` condition are not supported. When configuring your threat mappings, at least one entry must have a `MATCHES` condition. 
            ::::

        * **Indicator index field**: Select a field from your threat indicator index for comparison. 

    6. (Optional) Add more threat mapping entries and combine them with `AND` and `OR` clauses.

        For example, to create a rule that generates alerts when `host.name` **and** `destination.ip` field values in the `logs-*` or `packetbeat-*` {{elastic-sec}} indices are identical to the corresponding field values in the `logs-ti_*` indicator index, enter the rule parameters seen in the following image:

        :::{image} /solutions/images/security-indicator-rule-example.png
        :alt: Indicator match rule settings
        :screenshot:
        :::

        ::::{tip}
        Before you create rules, create [Timeline templates](/solutions/security/investigate/timeline.md) so you can select them under **Timeline template** at the end of the **Define rule** section. When alerts generated by the rule are investigated in the Timeline, Timeline query values are replaced with their corresponding alert field values.
        ::::

3. (Optional) Select **Suppress alerts** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


### Use value lists with indicator match rules [indicator-value-lists]

While there are numerous ways you can add data into indicator indices, you can use value lists as the indicator match index in an indicator match rule. Take the following scenario, for example:

You uploaded a value list of known ransomware domains, and you want to be notified if any of those domains matches a value contained in a domain field in your security event index pattern.

1. Upload a value list of indicators.
2. Create an indicator match rule and fill in the following fields:

    1. **Index patterns**: The Elastic Security event indices on which the rule runs.
    2. **Custom query**: The query and filters used to retrieve the required results from the Elastic Security event indices (e.g., `host.domain :*`).
    3. **Indicator index patterns**: Value lists are stored in a hidden index called `.items-<Kibana space>`. Enter the name of the {{kib}} space in which this rule will run in this field.
    4. **Indicator index query**: Enter the value `list_id :`, followed by the name of the value list you want to use as your indicator index (uploaded in Step 1 above).
    5. **Indicator mapping**

        * **Field**: Enter the field from the Elastic Security event indices to be used for comparing values.
        * **Indicator index field**: Enter the type of value list you created (i.e., `keyword`, `text`, or `IP`).

            ::::{tip}
            If you don’t remember this information, refer to the appropriate [value list](/solutions/security/detect-and-alert/create-manage-value-lists.md) and find the list’s type in the **Type** column (for example, the type can be `Keywords`, `Text`, or `IP`).
            ::::


:::{image} /solutions/images/security-indicator_value_list.png
:alt: indicator value list
:screenshot:
:::


## Create a new terms rule [create-new-terms-rule]

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule that searches for each new term detected in source documents, select **New Terms** on the **Create new rule** page, then:

    1. Specify what data to search by entering individual {{es}} index patterns or selecting an existing data view.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        ::::{note}
        You can use saved queries and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.
        ::::

    3. Use the **Fields** menu to select a field to check for new terms. You can also select up to three fields to detect a combination of new terms (for example, a `host.ip` and `host.id` that have never been observed together before).

        ::::{important}
        When checking multiple fields, each unique combination of values from those fields is evaluated separately. For example, a document with `host.name: ["host-1", "host-2", "host-3"]` and `user.name: ["user-1", "user-2", "user-3"]` has 9 (3x3) unique combinations of `host.name` and `user.name`. A document with 11 values in `host.name` and 10 values in `user.name` has 110 (11x10) unique combinations. The new terms rule only evaluates 100 unique combinations per document, so selecting fields with large arrays of values might cause incorrect results.
        ::::

    4. Use the **History Window Size** menu to specify the time range to search in minutes, hours, or days to determine if a term is new. The history window size must be larger than the rule interval plus additional look-back time, because the rule will look for terms where the only time(s) the term appears within the history window is *also* within the rule interval and additional look-back time.

        For example, if a rule has an interval of 5 minutes, no additional look-back time, and a history window size of 7 days, a term will be considered new only if the time it appears within the last 7 days is also within the last 5 minutes. Configure the rule interval and additional look-back time when you [set the rule’s schedule](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule).

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


## Create an {{esql}} rule [create-esql-rule]

Use [{{esql}}](elasticsearch://reference/query-languages/esql.md) to query your source events and aggregate event data. Query results are returned in a table with rows and columns. Each row becomes an alert.

To create an {{esql}} rule:

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. Select **{{esql}}**, then write a query.

    ::::{note}
    Refer to the sections below to learn more about [{{esql}} query types](/solutions/security/detect-and-alert/create-detection-rule.md#esql-rule-query-types), [query design considerations](/solutions/security/detect-and-alert/create-detection-rule.md#esql-query-design), and [rule limitations](/solutions/security/detect-and-alert/create-detection-rule.md#esql-rule-limitations).
    ::::


    ::::{tip}
    Click the help icon (![Click the ES|QL help icon](/solutions/images/security-esql-help-ref-button.png "title =20x20")) to open the in-product reference documentation for all {{esql}} commands and functions.
    ::::

3. (Optional) Use **Suppress alerts by** to reduce the number of repeated or duplicate alerts created by the rule. Refer to [Suppress detection alerts](/solutions/security/detect-and-alert/suppress-detection-alerts.md) for more information.
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn’t affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field’s name to find it faster, or type in an entirely new custom field.
    2. Enter the field’s data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule’s dependency on specific integrations and the data they generate, and allows users to confirm each integration’s [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration’s name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


### {{esql}} query types [esql-rule-query-types]

{{esql}} rule queries are loosely categorized into two types: aggregating and non-aggregating.


#### Aggregating query [esql-agg-query]

Aggregating queries use [`STATS...BY`](elasticsearch://reference/query-languages/esql/functions-operators/aggregation-functions.md) functions to aggregate source event data. Alerts generated by a rule with an aggregating query only contain the fields that the {{esql}} query returns and any new fields that the query creates.

::::{note}
A *new field* is a field that doesn’t exist in the query’s source index and is instead created when the rule runs. You can access new fields in the details of any alerts that are generated by the rule. For example, if you use the `STATS...BY` function to create a column with aggregated values, the column is created when the rule runs and is added as a new field to any alerts that are generated by the rule.
::::


Here is an example aggregating query:

```esql
FROM logs-*
| STATS host_count = COUNT(host.name) BY host.name
| SORT host_count DESC
| WHERE host_count > 20
```

* This query starts by searching logs from indices that match the pattern `logs-*`.
* The query then aggregates the count of events by `host.name`.
* Next, it sorts the result by `host_count` in descending order.
* Then, it filters for events where the `host_count` field appears more than 20 times during the specified rule interval.

::::{note}
Rules that use aggregating queries might create duplicate alerts. This can happen  when events that occur in the additional look-back time are aggregated both in the current rule execution and in a previous rule execution.
::::



#### Non-aggregating query [esql-non-agg-query]

Non-aggregating queries don’t use `STATS...BY` functions and don’t aggregate source event data. Alerts generated by a non-aggregating query contain source event fields that the query returns, new fields the query creates, and all other fields in the source event document.

::::{note}
A *new field* is a field that doesn’t exist in the query’s source index and is instead created when the rule runs. You can access new fields in the details of any alerts that are generated by the rule. For example, if you use the [`EVAL`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-eval) command to append new columns with calculated values, the columns are created when the rule runs, and are added as new fields to any alerts generated by the rule.
::::


Here is an example non-aggregating query:

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process"  AND event.id == "8a4f500d"
| LIMIT 10
```

* This query starts by querying logs from indices that match the pattern `logs-*`. The `METADATA _id, _index, _version` operator allows [alert deduplication](/solutions/security/detect-and-alert/create-detection-rule.md#esql-non-agg-query-dedupe).
* Next, the query filters events where the `event.category` is a process and the `event.id` is `8a4f500d`.
* Then, it limits the output to the top 10 results.


#### Turn on alert deduplication for rules using non-aggregating queries [esql-non-agg-query-dedupe]

To deduplicate alerts, a query needs access to the `_id`, `_index`, and `_version` metadata fields of the queried source event documents. You can allow this by adding the `METADATA _id, _index, _version` operator after the `FROM` source command, for example:

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process"  AND event.id == "8a4f500d"
| LIMIT 10
```

When those metadata fields are provided, unique alert IDs are created for each alert generated by the query.

When developing the query, make sure you don’t [`DROP`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-drop) or filter out the `_id`, `_index`, or `_version` metadata fields.

Here is an example of a query that fails to deduplicate alerts. It uses the `DROP` command to omit the `_id` property from the results table:

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process"  AND event.id == "8a4f500d"
| DROP _id
| LIMIT 10
```

Here is another example of an invalid query that uses the `KEEP` command to only return `event.*` fields in the results table:

```esql
FROM logs-* METADATA _id, _index, _version
| WHERE event.category == "process"  AND event.id == "8a4f500d"
| KEEP event.*
| LIMIT 10
```


### Query design considerations [esql-query-design]

When writing your query, consider the following:

* The [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-limit) command specifies the maximum number of rows an {{esql}} query returns and the maximum number of alerts created per rule execution. Similarly, a detection rule’s **Max alerts per run** setting specifies the maximum number of alerts it can create every time it runs.

    If the `LIMIT` value and **Max alerts per run** value are different, the rule uses the lower value to determine the maximum number of alerts the rule generates.

* When writing an aggregating query, use the [`STATS...BY`](elasticsearch://reference/query-languages/esql/commands/processing-commands.md#esql-stats-by) command with fields that you want to search and filter for after alerts are created. For example, using the `host.name`, `user.name`, `process.name` fields with the `BY` operator of the `STATS...BY` command returns these fields in alert documents, and allows you to search and filter for them from the Alerts table.
* When configuring alert suppression on a non-aggregating query, we recommend sorting results by ascending `@timestamp` order. Doing so ensures that alerts are properly suppressed, especially if the number of alerts generated is higher than the **Max alerts per run** value.


### {{esql}} rule limitations [esql-rule-limitations]

If your {{esql}} query creates new fields that aren’t part of the ECS schema, they aren’t mapped to the alerts index, so you can’t search for or filter them in the Alerts table. As a workaround, create [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md).


### Highlight fields returned by the {{esql}} rule query [custom-highlighted-esql-fields]

When configuring an {{esql}} rule’s **[Custom highlighted fields](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params)**, you can specify any fields that the rule’s aggregating or non-aggregating query return. This can help ensure that returned fields are visible in the alert details flyout while you’re investigating alerts.


## Configure basic rule settings [rule-ui-basic-params]

1. In the **About rule** pane, fill in the following fields:

    1. **Name**: The rule’s name.
    2. **Description**: A description of what the rule does.
    3. **Default severity**: Select the severity level of alerts created by the rule:

        * **Low**: Alerts that are of interest but generally are not considered to be security incidents. Sometimes a combination of low severity alerts can indicate suspicious activity.
        * **Medium**: Alerts that require investigation.
        * **High**: Alerts that require an immediate investigation.
        * **Critical**: Alerts that indicate it is highly likely a security incident has occurred.

    4. **Severity override** (optional): Select to use source event values to override the **Default severity** in generated alerts. When selected, a UI component is displayed where you can map the source event field values to severity levels. The following example shows how to map severity levels to `host.name` values:

        :::{image} /solutions/images/security-severity-mapping-ui.png
        :alt: severity mapping ui
        :screenshot:
        :::

        ::::{note}
        For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the `Group by` fields) will contain data. Also note that overrides are not supported for event correlation rules.
        ::::

    5. **Default risk score**: A numerical value between 0 and 100 that indicates the risk of events detected by the rule. This setting changes to a default value when you change the **Severity** level, but you can adjust the risk score as needed. General guidelines are:

        * `0` - `21` represents low severity.
        * `22` - `47` represents medium severity.
        * `48` - `73` represents high severity.
        * `74` - `100` represents critical severity.

    6. **Risk score override** (optional): Select to use a source event value to override the **Default risk score** in generated alerts. When selected, a UI component is displayed to select the source field used for the risk score. For example, if you want to use the source event’s risk score in alerts:

        :::{image} /solutions/images/security-risk-source-field-ui.png
        :alt: risk source field ui
        :screenshot:
        :::

        ::::{note}
        For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the `Group by` fields) will contain data.
        ::::

    7. **Tags** (optional): Words and phrases used to categorize, filter, and search the rule.

2. Continue with **one** of the following:

    * [Configure advanced rule settings (optional)](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params)
    * [Set the rule’s schedule](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule)



## Configure advanced rule settings (optional) [rule-ui-advanced-params]

1. Click **Advanced settings** and fill in the following fields where applicable:

    1. **Reference URLs** (optional): References to information that is relevant to the rule. For example, links to background information.
    2. **False positive examples** (optional): List of common scenarios that may produce false-positive alerts.
    3. **MITRE ATT&CKTM threats** (optional): Add relevant [MITRE](https://attack.mitre.org/) framework tactics, techniques, and subtechniques.
    4. **Custom highlighted fields** (optional): Specify highlighted fields for unique alert investigation flows. You can choose any fields that are available in the indices you selected for the rule’s data source.

        After you create the rule, you can find all custom highlighted fields in the About section of the rule details page. If the rule has alerts, you can find custom highlighted fields in the [Highlighted fields](/solutions/security/detect-and-alert/view-detection-alert-details.md#investigation-section) section of the alert details flyout.

    5. **Setup guide** (optional): Instructions on rule prerequisites such as required integrations, configuration steps, and anything else needed for the rule to work correctly.
    6. **Investigation guide** (optional): Information for analysts investigating alerts created by the rule. You can also add action buttons to [run Osquery](/solutions/security/investigate/run-osquery-from-investigation-guides.md) or [launch Timeline investigations](/solutions/security/detect-and-alert/launch-timeline-from-investigation-guides.md) using alert data.
    7. **Author** (optional): The rule’s authors.
    8. **License** (optional): The rule’s license.
    9. **Elastic endpoint exceptions** (optional): Adds all [{{elastic-endpoint}} exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) to this rule.

        ::::{note}
        If you select this option, you can add {{elastic-endpoint}} exceptions on the Rule details page. Additionally, all future exceptions added to [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) will also affect this rule.
        ::::

    10. **Building block** (optional): Select to create a building-block rule. By default, alerts generated from a building-block rule are not displayed in the UI. See [About building block rules](/solutions/security/detect-and-alert/about-building-block-rules.md) for more information.
    11. **Max alerts per run** (optional): Specify the maximum number of alerts the rule can create each time it runs. Default is 100.

        ::::{note}
        This setting can be superseded by the [{{kib}} configuration setting](kibana://reference/configuration-reference/alerting-settings.md#alert-settings) `xpack.alerting.rules.run.alerts.max`, which determines the maximum alerts generated by *any* rule in the {{kib}} alerting framework. For example, if `xpack.alerting.rules.run.alerts.max` is set to `1000`, the rule can generate no more than 1000 alerts even if **Max alerts per run** is set higher.
        ::::

    12. **Indicator prefix override**: Define the location of indicator data within the structure of indicator documents. When the indicator match rule executes, it queries specified indicator indices and references this setting to locate fields with indicator data. This data is used to enrich indicator match alerts with metadata about matched threat indicators. The default value for this setting is `threat.indicator`.

        ::::{important}
        If your threat indicator data is at a different location, update this setting accordingly to ensure alert enrichment can still be performed.
        ::::

    13. **Rule name override** (optional): Select a source event field to use as the rule name in the UI (Alerts table). This is useful for exposing, at a glance, more information about an alert. For example, if the rule generates alerts from Suricata, selecting `event.action` lets you see what action (Suricata category) caused the event directly in the Alerts table.

        ::::{note}
        For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the `Group by` fields) will contain data.
        ::::

    14. **Timestamp override** (optional): Select a source event timestamp field. When selected, the rule’s query uses the selected field, instead of the default `@timestamp` field, to search for alerts. This can help reduce missing alerts due to network or server outages. Specifically, if your ingest pipeline adds a timestamp when events are sent to {{es}}, this can prevent missing alerts from ingestion delays.

        If the selected field is unavailable, the rule query will use the `@timestamp` field instead. In the case that you don’t want to use the `@timestamp` field because you know your data source has an inaccurate `@timestamp` value, we recommend selecting the **Do not use @timestamp as a fallback timestamp field** option instead. This will ensure that the rule query ignores the `@timestamp` field entirely.

        ::::{tip}
        The [Microsoft](beats://reference/filebeat/filebeat-module-microsoft.md) and [Google Workspace](beats://reference/filebeat/filebeat-module-google_workspace.md) {{filebeat}} modules have an `event.ingested` timestamp field that can be used instead of the default `@timestamp` field.
        ::::

2. Click **Continue**. The **Schedule rule** pane is displayed.

    :::{image} /solutions/images/security-schedule-rule.png
    :alt: schedule rule
    :screenshot:
    :::

3. Continue with [setting the rule’s schedule](/solutions/security/detect-and-alert/create-detection-rule.md#rule-schedule).


## Set the rule’s schedule [rule-schedule]

1. Select how often the rule runs.
2. Optionally, add `Additional look-back time` to the rule. When defined, the rule searches indices with the additional time.

    For example, if you set a rule to run every 5 minutes with an additional look-back time of 1 minute, the rule runs every 5 minutes but analyzes the documents added to indices during the last 6 minutes.

    ::::{important}
    It is recommended to set the `Additional look-back time` to at least 1 minute. This ensures there are no missing alerts when a rule does not run exactly at its scheduled time.

    {{elastic-sec}} prevents duplication. Any duplicate alerts that are discovered during the `Additional look-back time` are *not* created.

    ::::

3. Click **Continue**. The **Rule actions** pane is displayed.
4. Do either of the following:

    * Continue onto [setting up alert notifications](/solutions/security/detect-and-alert/create-detection-rule.md#rule-notifications) and [Response Actions](/solutions/security/detect-and-alert/create-detection-rule.md#rule-response-action) (optional).
    * Create the rule (with or without activation).



## Set up rule actions (optional) [rule-notifications]

Use actions to set up notifications sent via other systems when alerts are generated.

::::{note}
To use actions for alert notifications, you need the [appropriate license](https://www.elastic.co/subscriptions). For more information, see [Cases requirements](/solutions/security/investigate/cases-requirements.md).
::::


1. Select a connector type to determine how notifications are sent. For example, if you select the {{jira}} connector, notifications are sent to your {{jira}} system.

    ::::{note}
    Each action type requires a connector. Connectors store the information required to send the notification from the external system. You can configure connectors while creating the rule or from the **{{connectors-ui}}** page. For more information, refer to [Action and connector types](/deploy-manage/manage-connectors.md).

    Some connectors that perform actions require less configuration. For example, you do not need to set the action frequency or variables for the [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md)

    ::::

2. After you select a connector, set its action frequency to define when notifications are sent:

    * **Summary of alerts**: Select this option to get a report that summarizes generated alerts, which you can review at your convenience. Alert summaries will be sent at the specified time intervals.

        ::::{note}
        When setting a custom notification frequency, do not choose a time that is shorter than the rule’s execution schedule.
        ::::

    * **For each alert**: Select this option to ensure notifications are sent every time new alerts are generated.

3. (Optional) Specify additional conditions that need to be met for notifications to send. Click the toggle to enable a setting, then add the required details:

    * **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
    * **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

4. Complete the required connector type fields. Here is an example with {{jira}}:

    :::{image} /solutions/images/security-selected-action-type.png
    :alt: selected action type
    :screenshot:
    :::

5. Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available [alert notification variables](/solutions/security/detect-and-alert/create-detection-rule.md#rule-action-variables).
6. Create the rule with or without activation.

    ::::{note}
    When you activate a rule, it is queued, and its schedule is determined by its initial run time. For example, if you activate a rule that runs every 5 minutes at 14:03 but it does not run until 14:04, it will run again at 14:09.
    ::::


::::{important}
After you activate a rule, you can check if it is running as expected using the [Monitoring tab](/troubleshoot/security/detection-rules.md) on the Rules page. If you see values in the `Gap` column, you can [Troubleshoot missing alerts](/troubleshoot/security/detection-rules.md#troubleshoot-signals).

When a rule fails to run, the {{security-app}} tries to rerun it at its next scheduled run time.

::::



### Alert notification placeholders [rule-action-variables]

You can use [mustache syntax](http://mustache.github.io/) to add variables to notification messages. The action frequency you choose determines the variables you can select from.

The following variables can be passed for all rules:

::::{note}
Refer to [Action frequency: Summary of alerts](/explore-analyze/alerts-cases/alerts/rule-action-variables.md#alert-summary-action-variables) to learn about additional variables that can be passed if the rule’s action frequency is **Summary of alerts**.
::::


* `{{context.alerts}}`: Array of detected alerts
* `{{{context.results_link}}}`: URL to the alerts in {{kib}}
* `{{context.rule.anomaly_threshold}}`: Anomaly threshold score above which alerts are generated ({{ml}} rules only)
* `{{context.rule.description}}`: Rule description
* `{{context.rule.false_positives}}`: Rule false positives
* `{{context.rule.filters}}`: Rule filters (query rules only)
* `{{context.rule.id}}`: Unique rule ID returned after creating the rule
* `{{context.rule.index}}`: Indices rule runs on (query rules only)
* `{{context.rule.language}}`: Rule query language (query rules only)
* `{{context.rule.machine_learning_job_id}}`: ID of associated {{ml}} job ({{ml}} rules only)
* `{{context.rule.max_signals}}`: Maximum allowed number of alerts per rule execution
* `{{context.rule.name}}`: Rule name
* `{{context.rule.query}}`: Rule query (query rules only)
* `{{context.rule.references}}`: Rule references
* `{{context.rule.risk_score}}`: Default rule risk score

    ::::{note}
    This placeholder contains the rule’s default values even when the **Risk score override** option is used.
    ::::

* `{{context.rule.rule_id}}`: Generated or user-defined rule ID that can be used as an identifier across systems
* `{{context.rule.saved_id}}`: Saved search ID
* `{{context.rule.severity}}`: Default rule severity

    ::::{note}
    This placeholder contains the rule’s default values even when the **Severity override** option is used.
    ::::

* `{{context.rule.threat}}`: Rule threat framework
* `{{context.rule.threshold}}`: Rule threshold values (threshold rules only)
* `{{context.rule.timeline_id}}`: Associated Timeline ID
* `{{context.rule.timeline_title}}`: Associated Timeline name
* `{{context.rule.type}}`: Rule type
* `{{context.rule.version}}`: Rule version
* `{{date}}`: Date the rule scheduled the action
* `{{kibanaBaseUrl}}`: Configured `server.publicBaseUrl` value, or empty string if not configured
* `{{rule.id}}`: ID of the rule
* `{{rule.name}}`: Name of the rule
* `{{rule.spaceId}}`: Space ID of the rule
* `{{rule.tags}}`: Tags of the rule
* `{{rule.type}}`: Type of rule
* `{{state.signals_count}}`: Number of alerts detected

The following variables can only be passed if the rule’s action frequency is for each alert:

* `{{alert.actionGroup}}`: Action group of the alert that scheduled actions for the rule
* `{{alert.actionGroupName}}`: Human-readable name of the action group of the alert that scheduled actions for the rule
* `{{alert.actionSubgroup}}`: Action subgroup of the alert that scheduled actions for the rule
* `{{alert.id}}`: ID of the alert that scheduled actions for the rule
* `{{alert.flapping}}`: A flag on the alert that indicates whether the alert status is changing repeatedly


#### Alert placeholder examples [placeholder-examples]

To understand which fields to parse, see the [Detections API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-detections-api) to view the JSON representation of rules.

Example using `{{context.rule.filters}}` to output a list of filters:

```json
{{#context.rule.filters}}
{{^meta.disabled}}{{meta.key}} {{#meta.negate}}NOT {{/meta.negate}}{{meta.type}} {{^exists}}{{meta.value}}{{meta.params.query}}{{/exists}}{{/meta.disabled}}
{{/context.rule.filters}}
```

Example using `{{context.alerts}}` as an array, which contains each alert generated since the last time the action was executed:

```json
{{#context.alerts}}
Detection alert for user: {{user.name}}
{{/context.alerts}}
```

Example using the mustache "current element" notation `{{.}}` to output all the rule references in the `signal.rule.references` array:

```json
{{#signal.rule.references}} {{.}} {{/signal.rule.references}}
```


### Set up response actions (optional) [rule-response-action]

Use response actions to set up additional functionality that will run whenever a rule executes:

* **Osquery**: Include live Osquery queries with a custom query rule. When an alert is generated, Osquery automatically collects data on the system related to the alert. Refer to [Add Osquery Response Actions](/solutions/security/investigate/add-osquery-response-actions.md) to learn more.
* **{{elastic-defend}}**: Automatically run response actions on an endpoint when rule conditions are met. For example, you can automatically isolate a host or terminate a process when specific activities or events are detected on the host. Refer to [Automated response actions](/solutions/security/endpoint-response-actions/automated-response-actions.md) to learn more.

::::{important}
Host isolation involves quarantining a host from the network to prevent further spread of threats and limit potential damage. Be aware that automatic host isolation can cause unintended consequences, such as disrupting legitimate user activities or blocking critical business processes.
::::



## Preview your rule (optional) [preview-rules]

You can preview any custom or prebuilt rule to find out how noisy it will be. For a custom rule, you can then adjust the rule’s query or other settings.

::::{note}
To preview rules, you must have the appropriate user role. Refer to [Detections requirements](/solutions/security/detect-and-alert/detections-requirements.md) for more information.
::::


Click the **Rule preview** button while creating or editing a rule. The preview opens in a side panel, showing a histogram and table with the alerts you can expect, based on the defined rule settings and past events in your indices.

:::{image} /solutions/images/security-preview-rule.png
:alt: Rule preview
:screenshot:
:::

The preview also includes the effects of rule exceptions and override fields. In the histogram, alerts are stacked by `event.category` (or `host.name` for machine learning rules), and alerts with multiple values are counted more than once.

To interact with the rule preview:

* Use the date and time picker to define the preview’s time range.

    ::::{tip}
    Avoid setting long time ranges with short rule intervals, or the rule preview might time out.
    ::::

* Click **Refresh** to update the preview.

    * When you edit the rule’s settings or the preview’s time range, the button changes from blue (![Blue circular refresh icon](/solutions/images/security-rule-preview-refresh-circle.png "title =20x20")) to green (![Green right-pointing arrow refresh icon](/solutions/images/security-rule-preview-refresh-arrow.png "title =20x20")) to indicate that the rule has been edited since the last preview.
    * For a relative time range (such as `Last 1 hour`), refresh the preview to check for the latest results. (Previews don’t automatically refresh with new incoming data.)

* Click the **View details** icon (![View details icon](/solutions/images/security-view-details-icon.png "title =20x20")) in the alerts table to view the details of a particular alert.
* To resize the preview, hover between the rule settings and preview, then click and drag the border. You can also click the border, then the collapse icon (![Collapse icon](/solutions/images/security-collapse-right-icon.png "title =20x20")) to collapse and expand the preview.
* To close the preview, click the **Rule preview** button again.


### View your rule’s {{es}} queries (optional) [view-rule-es-queries]

::::{note}
This option is offered for all rule types except indicator match rules. 
::::


When previewing a rule, you can also examine the {{es}} queries that are submitted when the rule runs. Use this information to identify and troubleshoot potential rule issues and confirm that your rule is retrieving the expected data.

To learn more about your rule’s {{es}} queries, preview its results and do the following:

1. Select the **Show {{es}} requests, ran during rule executions** option below the preview’s date and time picker. The **Preview logged results** section displays under the histogram and alerts table.
2. Click the **Preview logged results** section to expand it. Within the section, each rule execution is shown on an individual row.
3. Expand each row to learn more about the {{es}} queries that the rule submits each time it executes. The following details are provided:

    * When the rule execution started, and how long it took to complete
    * A brief explanation of what the {{es}} queries do
    * The first two {{es}} queries that the rule submits to indices containing events that are used during the rule execution

        ::::{tip}
        Run the queries in [Console](/explore-analyze/query-filter/tools/console.md) to determine if your rule is retrieving the expected data. For example, to test your rule’s exceptions, run the rule’s {{es}} queries, which will also contain exceptions added to the rule. If your rule’s exceptions are working as intended, the query will not return events that should be ignored.
        ::::

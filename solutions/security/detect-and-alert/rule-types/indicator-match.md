---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-indicator-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-indicator-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create an indicator match rule [create-indicator-rule]

Indicator match rules continually compare your security source events with threat intelligence indicators and generate alerts when matches are found. These rules help detect known threats based on external threat intelligence feeds.

**When to use**: Match events against threat intelligence feeds (e.g., "IP in known bad actor list", "domain matches malicious domain feed", "file hash in malware database").

**Performance**: High resource usage (~500ms-2s per execution). Runs two queries (indicator index + source indices). Limit to 15-minute intervals or longer. Keep indicator count under 10,000 for best performance.

::::{note}
{{elastic-sec}} provides [limited support](/solutions/security/detect-and-alert.md#support-indicator-rules) for indicator match rules.
::::

## Create the rule

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
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn't affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field's name to find it faster, or type in an entirely new custom field.
    2. Enter the field's data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


## Use value lists with indicator match rules [indicator-value-lists]

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
            If you don't remember this information, refer to the appropriate [value list](/solutions/security/detect-and-alert/create-manage-value-lists.md) and find the list's type in the **Type** column (for example, the type can be `Keywords`, `Text`, or `IP`).
            ::::


:::{image} /solutions/images/security-indicator_value_list.png
:alt: indicator value list
:screenshot:
:::


---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-threshold-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-threshold-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create a threshold rule [create-threshold-rule]

Threshold rules create alerts when the number of times a specified field's value appears meets or exceeds a defined threshold during a single rule execution. This is useful for count-based detection.

**When to use**: Detect behavior based on frequency or volume (e.g., 5+ failed logins from same IP, 10+ DNS queries to same domain, repeated attempts to access restricted resources).

**Performance**: Medium resource usage (~200-500ms per execution) due to aggregations. Consider 10-minute intervals for high-cardinality fields.

## Create the rule

1. Find **Detection rules (SIEM)** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create new rule**.
2. To create a rule based on a source event field threshold, select **Threshold**, then:

    1. Define which {{es}} indices the rule analyzes for alerts.
    2. Use the filter and query fields to create the criteria used for detecting alerts.

        ::::{note}
        You can use {{kib}} saved queries (![Saved query menu](/solutions/images/security-saved-query-menu.png "title =20x20")) and queries from saved Timelines (**Import query from saved Timeline**) as rule conditions.
        ::::

    3. Use the **Group by** and **Threshold** fields to determine which source event field is used as a threshold and the threshold's value.

        ::::{note}
        Consider the following when using the **Group by** field:
        - Nested fields are not supported. Nested fields are fields defined with `"type": "nested"` in your {{es}} mapping. Regular object fields like `host.name` or `user.name` ARE supported.
        - High cardinality in the fields or a high number of matching documents can result in a rule timeout or a circuit breaker error from {{es}}.

        **Understanding cardinality limits**:

        Cardinality refers to the number of unique values in a field. {{es}} must track each unique value in memory during aggregation.

        **Risk levels**:
        * **Low risk** (<10,000 unique values): Fields like `user.name`, `host.name` in typical environments
        * **Medium risk** (10,000-100,000 unique values): Fields like `process.name` across large server fleets
        * **High risk** (>100,000 unique values): Fields like `source.ip`, `url.full`, or `user_agent.original` in high-traffic environments

        **Testing cardinality before creating the rule**:

        Run this query in **Dev Tools** to check cardinality:

        ```json
        GET your-index-pattern/_search
        {
          "size": 0,
          "query": {
            "bool": {
              "must": [
                { "range": { "@timestamp": { "gte": "now-1h" } } }
              ]
            }
          },
          "aggs": {
            "cardinality_check": {
              "cardinality": {
                "field": "your-field-name"
              }
            }
          }
        }
        ```

        If the returned `value` exceeds 50,000, consider:
        * Using a different field with lower cardinality
        * Adding more filters to your rule query to reduce the number of matched documents
        * Increasing the {{es}} heap size and circuit breaker limits

        **Circuit breaker error message**:

        If you encounter a circuit breaker error, you'll see: `Data too large, data for [fielddata] would be [X/Xgb], which is larger than the limit of [Y/Ygb]`

        To resolve:
        1. Narrow your rule query to match fewer documents
        2. Choose a field with lower cardinality
        3. Increase the field data circuit breaker limit: Set `indices.breaker.fielddata.limit` to at least 40% of JVM heap in `elasticsearch.yml`
        4. Increase {{es}} JVM heap size if system resources allow
        ::::

    4. Use the **Count** field to limit alerts by cardinality of a certain field.

        For example, if **Group by** is `source.ip, destination.ip` and its **Threshold** is `10`, an alert is generated for every pair of source and destination IP addresses that appear in at least 10 of the rule's search results.

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
4. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn't affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field's name to find it faster, or type in an entirely new custom field.
    2. Enter the field's data type.

5. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

6. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


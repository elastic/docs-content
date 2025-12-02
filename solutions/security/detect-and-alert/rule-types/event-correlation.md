---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/rules-ui-create.html#create-eql-rule
  - https://www.elastic.co/guide/en/serverless/current/security-rules-create.html#create-eql-rule
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Create an event correlation rule [create-eql-rule]

Event correlation rules use EQL (Event Query Language) to detect sequences of related events or correlate events across different data sources. These rules are ideal for detecting attack patterns that involve multiple steps.

**When to use**: Detect sequences or correlations of events (e.g., "process start THEN network connection", "file created AND then deleted within 1 minute").

**Performance**: Medium resource usage (~200-400ms per execution). Sequence queries are efficient, but complex correlations take longer.

## Create the rule

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
5. (Optional) Create a list of **Required fields** that the rule needs to function. This list is informational only, to help users understand the rule; it doesn't affect how the rule actually runs.

    1. Click **Add required field**, then select a field from the index patterns or data view you specified for the rule. You can also start typing a field's name to find it faster, or type in an entirely new custom field.
    2. Enter the field's data type.

6. (Optional) Add **Related integrations** to associate the rule with one or more [Elastic integrations](https://docs.elastic.co/en/integrations). This indicates the rule's dependency on specific integrations and the data they generate, and allows users to confirm each integration's [installation status](/solutions/security/detect-and-alert/manage-detection-rules.md#rule-prerequisites) when viewing the rule.

    1. Click **Add integration**, then select an integration from the list. You can also start typing an integration's name to find it faster.
    2. Enter the version of the integration you want to associate with the rule, using [semantic versioning](https://semver.org/). For version ranges, you must use tilde or caret syntax. For example, `~1.2.3` is from 1.2.3 to any patch version less than 1.3.0, and `^1.2.3` is from 1.2.3 to any minor and patch version less than 2.0.0.

7. Click **Continue** to [configure basic rule settings](/solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-basic-params).


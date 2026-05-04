---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Reference for all detection rule settings including basic, advanced, schedule, actions, and notification variables.
---

# Common rule settings [common-detection-rule-settings]

All detection rules share a common set of settings for describing the rule, controlling its schedule, configuring actions, and setting up response actions. These settings apply regardless of the [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) you select.

For rule-type-specific settings (query definitions, index patterns, {{ml}} jobs, and so on), refer to [](/solutions/security/detect-and-alert/rule-types.md).

## Basic settings [rule-ui-basic-params]

Configure these settings in the **About rule** pane.

**Name**
:   The rule's name.

**Description**
:   A description of what the rule does.

**Default severity**
:   The severity level of alerts created by the rule:

    * **Low**: Alerts that are of interest but generally are not considered to be security incidents. Sometimes a combination of low severity alerts can indicate suspicious activity.
    * **Medium**: Alerts that require investigation.
    * **High**: Alerts that require an immediate investigation.
    * **Critical**: Alerts that indicate it is highly likely a security incident has occurred.

**Severity override** (optional)
:   Select to use source event values to override the **Default severity** in generated alerts. When selected, a UI component is displayed where you can map the source event field values to severity levels.

    :::{image} /solutions/images/security-severity-mapping-ui.png
    :alt: severity mapping ui
    :screenshot:
    :::

    ::::{note}
    For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the **Group by** fields) will contain data. Overrides are not supported for event correlation rules.
    ::::

**Default risk score**
:   A numerical value between 0 and 100 that indicates the risk of events detected by the rule. This setting changes to a default value when you change the **Severity** level, but you can adjust the risk score as needed. General guidelines are:

    * `0` - `21` represents low severity.
    * `22` - `47` represents medium severity.
    * `48` - `73` represents high severity.
    * `74` - `100` represents critical severity.

**Risk score override** (optional)
:   Select to use a source event value to override the **Default risk score** in generated alerts. When selected, a UI component is displayed to select the source field used for the risk score.

    :::{image} /solutions/images/security-risk-source-field-ui.png
    :alt: risk source field ui
    :screenshot:
    :::

    ::::{note}
    For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the **Group by** fields) will contain data.
    ::::

**Tags** (optional)
:   Words and phrases used to categorize, filter, and search the rule.

## Advanced settings [rule-ui-advanced-params]

Configure these settings by clicking **Advanced settings** in the **About rule** pane.

**Author** (optional)
:   The rule's authors.

**Building block** (optional)
:   Select to create a building-block rule. By default, alerts generated from a building-block rule are not displayed in the UI. See [About building block rules](/solutions/security/detect-and-alert/about-building-block-rules.md) for more information.

**Custom highlighted fields** (optional)
:   Specify highlighted fields for unique alert investigation flows. These fields help analysts quickly access key information when triaging alerts, without needing to search through all available fields. You can select any fields that are available in the indices you selected for the rule's data source.

    After you create the rule, you can find all custom highlighted fields in the About section of the rule details page. If the rule has alerts, you can find custom highlighted fields in the [Highlighted fields](/solutions/security/detect-and-alert/view-detection-alert-details.md#investigation-section) section of the alert details flyout.

**Elastic endpoint exceptions** (optional)
:   Adds all [{{elastic-endpoint}} exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md#endpoint-rule-exceptions) to this rule.

    ::::{note}
    If you select this option, you can add {{elastic-endpoint}} exceptions on the Rule details page. Additionally, all future exceptions added to [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) will also affect this rule.
    ::::

**False positive examples** (optional)
:   List of common scenarios that might produce false-positive alerts.

**Investigation guide** (optional)
:   Information for analysts investigating alerts created by the rule. You can also add action buttons to [run Osquery](/solutions/security/investigate/run-osquery-from-investigation-guides.md) or [start Timeline investigations](/solutions/security/detect-and-alert/write-investigation-guides.md) using alert data.

**License** (optional)
:   The rule's license.

**Max alerts per run** (optional)
:   Specify the maximum number of alerts the rule can create each time it executes. Default is 100.

::::{admonition} System-level alert limit
The `xpack.alerting.rules.run.alerts.max` [{{kib}} setting](kibana://reference/configuration-reference/alerting-settings.md#alert-settings) acts as a system-level limit on alerts per rule execution, and can supersede a security rule's **Max alerts per run** setting. If a rule's **Max alerts per run** value exceeds `xpack.alerting.rules.run.alerts.max`, the lower system setting takes precedence and the rule will not generate more alerts than it allows.
::::

**MITRE ATT&CK threats** (optional)
:   Add relevant [MITRE ATT&CK](https://attack.mitre.org/) tactics, techniques, and subtechniques.

**Reference URLs** (optional)
:   References to information that is relevant to the rule. For example, links to background information.

**Related integrations** (optional)
:   Associate the rule with one or more [{{product.integrations}}](https://docs.elastic.co/en/integrations) to indicate data dependencies and allow users to verify each integration's [installation status](/solutions/security/detect-and-alert/prebuilt-rule-components.md#rule-prerequisites).

**Required fields** (optional)
:   An informational list of fields the rule needs to function. This does not affect rule execution. It helps other users understand the rule's data dependencies.

    ::::{note}
    This setting is not available for {{ml}} rules.
    ::::

**Rule name override** (optional)
:   Select a source event field to use as the rule name in the UI (Alerts table). This is useful for exposing, at a glance, more information about an alert. For example, if the rule generates alerts from Suricata, selecting `event.action` lets you see what action (Suricata category) caused the event directly in the Alerts table.

    ::::{note}
    For threshold rules, not all source event values can be used for overrides; only the fields that were aggregated over (the **Group by** fields) will contain data.
    ::::

**Setup guide** (optional)
:   Instructions on rule prerequisites such as required integrations, configuration steps, and anything else needed for the rule to work correctly.

**Timestamp override** (optional)
:   Select a source event timestamp field. When selected, the rule's query uses the selected field, instead of the default `@timestamp` field, to search for alerts. This can help reduce missing alerts due to network or server outages. Specifically, if your ingest pipeline adds a timestamp when events are sent to {{es}}, this can prevent missing alerts from ingestion delays.

    If the selected field is unavailable, the rule query will use the `@timestamp` field instead. If you don't want to use the `@timestamp` field because your data source has an inaccurate `@timestamp` value, select the **Do not use @timestamp as a fallback timestamp field** option instead. This ensures the rule query ignores the `@timestamp` field entirely.

    ::::{tip}
    The [Microsoft](beats://reference/filebeat/filebeat-module-microsoft.md) and [Google Workspace](beats://reference/filebeat/filebeat-module-google_workspace.md) {{filebeat}} modules have an `event.ingested` timestamp field that can be used instead of the default `@timestamp` field.
    ::::

## Schedule settings [rule-schedule]

**Runs every**
:   How often the rule runs.

**Additional look-back time** (optional)
:   When defined, the rule searches indices with the additional time.

    For example, if you set a rule to run every 5 minutes with an additional look-back time of 1 minute, the rule runs every 5 minutes but analyzes the documents added to indices during the last 6 minutes.

::::{important}
It is recommended to set the `Additional look-back time` to at least 1 minute. This ensures there are no missing alerts when a rule does not run exactly at its scheduled time.

{{elastic-sec}} prevents duplication. Any duplicate alerts that are discovered during the `Additional look-back time` are *not* created.
::::

## Rule actions [rule-notifications]

Use rule actions to set up notifications sent through other systems when alerts are generated. Rule actions let you send Slack messages, create {{jira}} tickets, trigger PagerDuty incidents, and more.

::::{note}
To use rule actions for alert notifications, you need the [appropriate license]({{subscriptions}}). For more information, see [Control access to cases](/explore-analyze/cases/control-case-access.md).
::::

:::{admonition} Rule actions versus workflows
:applies_to: `preview 9.3+` :applies_to: `serverless preview`
You can automate alert responses using either rule actions or [workflows](/explore-analyze/workflows.md). Rule actions are simpler to set up and work well for individual rules with specific notification needs. Workflows offer more flexibility for complex, multi-step processes that you want to standardize across multiple rules.

| Use case | Rule actions | Workflows |
|----------|--------------|-----------|
| Respond to alerts from a specific rule | Yes | Yes |
| Apply the same response process to multiple rules | Configure separately on each rule | Define once, trigger from any rule |
| Include complex conditional logic | Basic conditions only | Advanced conditions and branching |
| Chain multiple actions together | Limited | Yes |
| Centralized management | No (per-rule configuration) | Yes |

To set up a workflow as a rule action, refer to [Trigger a workflow from an alert](/explore-analyze/workflows/triggers/alert-triggers.md).
:::

**Connector type**
:   Determines how notifications are sent. For example, if you select the {{jira}} connector, notifications are sent to your {{jira}} system. You can configure connectors while creating the rule or from the **{{connectors-ui}}** page. For available connector types, refer to [Action and connector types](/deploy-manage/manage-connectors.md).

**Action frequency**
:   Defines when notifications are sent:

    * **Summary of alerts**: Sends a report that summarizes generated alerts at the specified time intervals. When setting a custom notification frequency, do not select a time that is shorter than the rule's execution schedule.

    * **For each alert**: Sends notifications every time new alerts are generated.

**Conditional actions** (optional)
:   Specify additional conditions that need to be met for notifications to send:

    * **If alert matches query**: Enter a KQL query that defines field-value pairs or query conditions that must be met for notifications to send. The query only searches alert documents in the indices specified for the rule.
    * **If alert is generated during timeframe**: Set timeframe details. Notifications are only sent if alerts are generated within the timeframe you define.

**Notification message**
:   Use the default notification message or customize it. You can add more context to the message by clicking the icon above the message text box and selecting from a list of available [alert notification variables](#rule-action-variables).

## Response actions [rule-response-action]

Use response actions to set up additional functionality that executes whenever a rule triggers:

* **Osquery**: Include live Osquery queries with a custom query rule. When an alert is generated, Osquery automatically collects data on the system related to the alert. Refer to [Add Osquery Response Actions](/solutions/security/investigate/add-osquery-response-actions.md) to learn more.
* **{{elastic-defend}}**: Automatically execute response actions on an endpoint when rule conditions are met. For example, you can automatically isolate a host or end a process when specific activities or events are detected on the host. Refer to [Automated response actions](/solutions/security/endpoint-response-actions/automated-response-actions.md) to learn more.

::::{important}
Host isolation involves quarantining a host from the network to prevent further proliferation of threats and limit potential damage. Be aware that automatic host isolation can cause unintended consequences, such as disrupting legitimate user activities or blocking critical business processes.
::::

## Alert notification variables [rule-action-variables]

You can use [mustache syntax](http://mustache.github.io/) to add variables to notification messages. The action frequency you select determines the available variables.

::::{note}
Refer to [Action frequency: Summary of alerts](/explore-analyze/alerting/alerts/rule-action-variables.md#alert-summary-action-variables) to learn about additional variables that can be passed if the rule's action frequency is **Summary of alerts**.
::::

### Variables for all rules [all-rule-variables]

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
    This placeholder contains the rule's default values even when the **Risk score override** option is used.
    ::::

* `{{context.rule.rule_id}}`: Generated or user-defined rule ID that can be used as an identifier across systems
* `{{context.rule.saved_id}}`: Saved search ID
* `{{context.rule.severity}}`: Default rule severity

    ::::{note}
    This placeholder contains the rule's default values even when the **Severity override** option is used.
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

### Per-alert variables [per-alert-variables]

The following variables can only be passed if the rule's action frequency is **For each alert**:

* `{{alert.actionGroup}}`: Action group of the alert that scheduled actions for the rule
* `{{alert.actionGroupName}}`: Human-readable name of the action group of the alert that scheduled actions for the rule
* `{{alert.actionSubgroup}}`: Action subgroup of the alert that scheduled actions for the rule
* `{{alert.id}}`: ID of the alert that scheduled actions for the rule
* `{{alert.flapping}}`: A flag on the alert that indicates whether the alert status is changing repeatedly

### Placeholder examples [placeholder-examples]

To understand which fields to parse, see the [Detections API]({{kib-apis}}group/endpoint-security-detections-api) to view the JSON representation of rules.

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

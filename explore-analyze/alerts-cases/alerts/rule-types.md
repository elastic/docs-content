---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/rule-types.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Reference of available rule types for alerting in Kibana, including Stack rules and app-specific rules.
---

# Rule types [rule-types]

Rule types define how conditions are detected and what actions are triggered when those conditions are met. {{kib}} provides Stack rules built into the {{stack}} and app-specific rules registered by {{kib}} apps. You can create most rule types in **{{stack-manage-app}}** > **{{rules-ui}}**, though Security rules must be created in the **Security** app.

::::{note}
Some rule types are subscription features, while others are free features. For a comparison of the Elastic subscription levels, see [the subscription page](https://www.elastic.co/subscriptions).

::::

## Stack rules [stack-rules]

[Stack rules](create-manage-rules.md) are built into {{kib}}. To access the **Stack Rules** feature and create and edit rules, users require the `all` privilege. See [feature privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-feature-privileges) for more information.

|     |     |
| --- | --- |
| [{{es}} query](rule-type-es-query.md) | Run a user-configured {{es}} query, compare the number of matches to a configured threshold, and schedule actions to run when the threshold condition is met. |
| [Index threshold](rule-type-index-threshold.md) | Aggregate field values from documents using {{es}} queries, compare them to threshold values, and schedule actions to run when the thresholds are met. |
| [Transform rules](../../transforms/transform-alerts.md) | {applies_to}`stack: beta` {applies_to}`serverless: beta` Run scheduled checks on a {{ctransform}} to check its health. If a {{ctransform}} meets the conditions, an alert is created and the associated action is triggered. |
| [Tracking containment](geo-alerting.md) | Run an {{es}} query to determine if any documents are currently contained in any boundaries from a specified boundary index and generate alerts when a rule’s conditions are met. |

## {{observability}} rules [observability-rules]

{{observability}} rules detect complex conditions in your observability data and create alerts when a rule’s conditions are met. For example, you can create a rule that detects when the value of a metric exceeds a specified threshold or when an anomaly occurs on a system or service you are monitoring. For more information, refer to [Alerting](../../../solutions/observability/incident-management/alerting.md).

::::{note}
If you create a rule in the {{observability}} app, its alerts are not visible in **{{stack-manage-app}} > {{rules-ui}}**. They are visible only in the {{observability}} app.

::::

## Machine learning rules [ml-rules]
```{applies_to}
stack: beta
serverless: beta
```

[{{ml-cap}} rules](../../machine-learning/anomaly-detection/ml-configuring-alerts.md) run scheduled checks on an {{anomaly-job}} to detect anomalies with certain conditions. If an anomaly meets the conditions, an alert is created and the associated action is triggered.

## Security rules [security-rules]

Security rules detect suspicious source events with pre-built or custom rules and create alerts when a rule’s conditions are met. For more information, refer to [Security rules](detection-rules://index.md).

::::{note}
Alerts associated with security rules are visible only in the {{security-app}}; they are not visible in **{{stack-manage-app}} > {{rules-ui}}**.

::::

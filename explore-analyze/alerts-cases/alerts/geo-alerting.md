---
navigation_title: Tracking containment
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/geo-alerting.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Reference for the Tracking containment rule type for geospatial alerting on entity movements.
---

# Tracking containment rule [geo-alerting]

The **Tracking containment** rule type monitors entity movements and triggers alerts when an entity enters or exits a defined geographical boundary. This rule type is useful for tracking assets, monitoring restricted zones, or detecting location-based events.

In **{{stack-manage-app}}** > **{{rules-ui}}**, click **Create rule**. Select the **Tracking containment** rule type then fill in the name and optional tags.

## Define the conditions [_define_the_conditions_3]

When you create a tracking containment rule, you must define the conditions that it detects. For example:

:::{image} /explore-analyze/images/kibana-alert-types-tracking-containment-conditions.png
:alt: Creating a tracking containment rule in Kibana
:screenshot:
:::

1. Define the entities index, which must contain a `geo_point` or `geo_shape` field, `date` field, and entity identifier. An entity identifier is a `keyword`, `number`, or `ip` field that identifies the entity. Entity data is expected to be updating so that there are entity movements to alert upon.
2. Define the boundaries index, which contains `geo_shape` data. Boundaries data is expected to be static (not updating). Boundaries are collected once when the rule is created and anytime after when boundary configuration is modified.
3. Set the check interval, which defines how often to evaluate the rule conditions.
4. In the advanced options, you can change the number of consecutive runs that must meet the rule conditions before an alert occurs. The default value is `1`.

Entity locations are queried to determine whether they are contained within any monitored boundaries. Entity data should be somewhat "real time", meaning the dates of new documents aren’t older than the current time minus the amount of the interval. If data older than `now - <check interval>` is ingested, it won’t trigger a rule.

## Add actions [_add_actions_2]

You can optionally send notifications when the rule conditions are met. In particular, this rule type supports:

* alert summaries
* actions that run when the containment condition is met
* actions that run when an entity is no longer contained

For each action, you must choose a connector, which provides connection information for a {{kib}} service or third party integration. For more information about all the supported connectors, go to [*Connectors*](../../../deploy-manage/manage-connectors.md).

After you select a connector, you must set the action frequency. You can choose to create a summary of alerts on each check interval or on a custom interval. Alternatively, you can set the action frequency such that actions run for each alert. Choose how often the action runs (at each check interval, only when the alert status changes, or at a custom action interval). You must also choose an action group, which indicates whether the action runs when the containment condition is met or when an entity is no longer contained. Each connector supports a specific set of actions for each action group. For example:

:::{image} /explore-analyze/images/kibana-alert-types-tracking-containment-action-options.png
:alt: Action frequency options for an action
:screenshot:
:::

You can further refine the conditions under which actions run by specifying that actions only run when they match a KQL query or when an alert occurs within a specific time frame.

## Add action variables [_add_action_variables_2]

You can pass rule values to an action to provide contextual details. To view the list of variables available for each action, click the "add rule variable" button. For example:

:::{image} /explore-analyze/images/kibana-alert-types-tracking-containment-rule-action-variables.png
:alt: Passing rule values to an action
:screenshot:
:::

The following action variables are specific to the tracking containment rule. You can also specify [variables common to all rules](rule-action-variables.md).

`context.containingBoundaryId`
:   The identifier for the boundary containing the entity. This value is not set for recovered alerts.

`context.containingBoundaryName`
:   The name of the boundary containing the entity. This value is not set for recovered alerts.

`context.detectionDateTime`
:   The end of the check interval when the alert occurred.

`context.entityDateTime`
:   The date the entity was recorded in the boundary.

`context.entityDocumentId`
:   The identifier for the contained entity document.

`context.entityId`
:   The entity identifier for the document that generated the alert.

`context.entityLocation`
:   The location of the entity.

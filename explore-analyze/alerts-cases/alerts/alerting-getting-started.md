---
applies_to:
  stack: ga
  serverless: ga
navigation_title: Getting started with alerts
products:
  - id: kibana
description: Step-by-step tutorial for creating and configuring your first alerting rule.
---

# Getting started with alerting [alerting-getting-started]

Alerting enables you to define rules that detect complex conditions within different {{kib}} apps and trigger actions when those conditions are met. Alerting is integrated with {{observability}}, **Security**, **Maps**, and the **{{ml-app}}**, can be centrally managed from **{{stack-manage-app}}**, and provides a set of built-in connectors and rules for you to use.

:::{image} /explore-analyze/images/kibana-alerting-overview.png
:alt: {{rules-ui}} UI
:::

::::{important}
To make sure you can access alerting and actions, see the [setup and prerequisites](../../../explore-analyze/alerts-cases/alerts/alerting-setup.md#alerting-prerequisites) section.

::::

Alerting works by running checks on a schedule to detect conditions defined by a rule. When a condition is met, the rule tracks it as an *alert* and responds by triggering one or more *actions*. Actions typically involve interaction with {{kib}} services or third party integrations. *Connectors* enable actions to talk to these services and integrations. This section describes all of these elements and how they operate together.

## Rules [_rules]

A rule specifies a background task that runs on the {{kib}} server to check for specific conditions. {{kib}} provides two types of rules: stack rules that are built into {{kib}} and the rules that are registered by {{kib}} apps. For more information, refer to [*Rule types*](../../../explore-analyze/alerts-cases/alerts/rule-types.md).

A rule consists of three main parts:

* *Conditions*: what needs to be detected?
* *Schedule*: when/how often should detection checks run?
* *Actions*: what happens when a condition is detected?

For example, when monitoring a set of servers, a rule might:

* Check for average CPU usage > 0.9 on each server for the last two minutes (condition).
* Check every minute (schedule).
* Send a warning email message via SMTP with subject `CPU on {{server}} is high` (action).

:::{image} /explore-analyze/images/kibana-what-is-a-rule.svg
:alt: Three components of a rule
:::

The following sections describe each part of the rule in more detail.

### Conditions [alerting-concepts-conditions]

Under the hood, {{kib}} rules detect conditions by running a JavaScript function on the {{kib}} server, which gives it the flexibility to support a wide range of conditions, anything from the results of a simple {{es}} query to heavy computations involving data from multiple sources or external systems.

These conditions are packaged and exposed as *rule types*. A rule type hides the underlying details of the condition, and exposes a set of parameters to control the details of the conditions to detect.

For example, an [index threshold rule type](../../../explore-analyze/alerts-cases/alerts/rule-type-index-threshold.md) lets you specify the index to query, an aggregation field, and a time window, but the details of the underlying {{es}} query are hidden.

See [*Rule types*](../../../explore-analyze/alerts-cases/alerts/rule-types.md) for the rules provided by {{kib}} and how they express their conditions.

### Schedule [alerting-concepts-scheduling]

Rule schedules are defined as an interval between subsequent checks, and can range from a few seconds to months.

::::{important}
The intervals of rule checks in {{kib}} are approximate. Their timing is affected by factors such as the frequency at which tasks are claimed and the task load on the system. Refer to [Alerting production considerations](../../../deploy-manage/production-guidance/kibana-alerting-production-considerations.md) for more information.

::::

### Actions [alerting-concepts-actions]

Actions run as background tasks on the {{kib}} server when rule conditions are met. Recovery actions likewise run when rule conditions are no longer met. They send notifications by connecting with services inside {{kib}} or integrating with third-party systems.

When defining actions in a rule, you specify:

* A connector
* An action frequency
* A mapping of rule values to properties exposed for that type of action

Rather than repeatedly entering connection information and credentials for each action, {{kib}} simplifies action setup using [connectors](../../../deploy-manage/manage-connectors.md). For example if four rules send email notifications via the same SMTP service, they can all reference the same SMTP connector.

The *action frequency* defines when the action runs (for example, only when the alert status changes or at specific time intervals). Each rule type also has a set of the *action groups* that affects when the action runs (for example, when the threshold is met or when the alert is recovered). If you want to reduce the number of notifications you receive without affecting their timeliness, set the action frequency to a summary of alerts. You will receive notifications that summarize the new, ongoing, and recovered alerts at your preferred time intervals.

Some types of rules enable you to further refine the conditions under which actions run. For example, you can specify that actions run only when an alert occurs within a specific time frame or when it matches a KQL query.

Each action definition is therefore a template: all the parameters needed to invoke a service are supplied except for specific values that are only known at the time the rule condition is detected.

In the server monitoring example, the `email` connector type is used, and `server` is mapped to the body of the email, using the template string `CPU on {{server}} is high`.

When the rule detects the condition, it creates an alert containing the details of the condition.

## Alerts [alerting-concepts-alerts]

When checking for a condition, a rule might identify multiple occurrences of the condition. {{kib}} tracks each of these alerts separately. Depending on the action frequency, an action occurs per alert or at the specified alert summary interval.

Using the server monitoring example, each server with average CPU > 0.9 is tracked as an alert. This means a separate email is sent for each server that exceeds the threshold whenever the alert status changes.

:::{image} /explore-analyze/images/kibana-alerts.svg
:alt: {{kib}} tracks each detected condition as an alert and takes action on each alert
:::

## Putting it all together [_putting_it_all_together]

A rule consists of conditions, actions, and a schedule. When conditions are met, alerts are created that render actions and invoke them. To make action setup and update easier, actions use connectors that centralize the information used to connect with {{kib}} services and third-party integrations. The following example ties these concepts together:

:::{image} /explore-analyze/images/kibana-rule-concepts-summary.svg
:alt: Rules
:::

1. Any time a rule’s conditions are met, an alert is created. This example checks for servers with average CPU > 0.9. Three servers meet the condition, so three alerts are created.
2. Alerts create actions according to the action frequency, as long as they are not muted or throttled. When actions are created, its properties are filled with actual values. In this example, three actions are created when the threshold is met, and the template string `{{server}}` is replaced with the appropriate server name for each alert.
3. {{kib}} runs the actions, sending notifications by using a third party integration like an email service.
4. If the third party integration has connection parameters or credentials, {{kib}} fetches these from the appropriate connector.

## Differences from {{watcher}} [alerting-concepts-differences]

[{{watcher}}](../../../explore-analyze/alerts-cases/watcher.md) and the {{kib}} {{alert-features}} are both used to detect conditions and can trigger actions in response, but they are completely independent alerting systems.

This section will clarify some of the important differences in the function and intent of the two systems.

Functionally, the {{alert-features}} differ in that:

* Scheduled checks are run on {{kib}} instead of {{es}}
* {{kib}} [rules hide the details of detecting conditions](../../../explore-analyze/alerts-cases/alerts/alerting-getting-started.md#alerting-concepts-conditions) through rule types, whereas watches provide low-level control over inputs, conditions, and transformations.
* {{kib}} rules track and persist the state of each detected condition through alerts. This makes it possible to mute and throttle individual alerts, and detect changes in state such as resolution.
* Actions are linked to alerts. Actions are fired for each occurrence of a detected condition, rather than for the entire rule.

At a higher level, the {{alert-features}} allow rich integrations across use cases like [**APM**](/solutions/observability/apm/index.md), [**Metrics**](/solutions/observability/infra-and-hosts.md), [**Security**](/solutions/security.md), and [**Uptime**](/solutions/observability/uptime/index.md). Prepackaged rule types simplify setup and hide the details of complex, domain-specific detections, while providing a consistent interface across {{kib}}.

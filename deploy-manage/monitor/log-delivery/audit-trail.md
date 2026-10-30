---
navigation_title: Serverless audit trail
description: Configure and explore audit trail log delivery for Elastic Cloud Serverless, including ignore filters, destinations, data streams, and investigation recipes.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
---

# Serverless audit trail

Audit trail is the first log type available for [log delivery](/deploy-manage/monitor/log-delivery.md) in {{serverless-full}}. Enabling it delivers audit logs to your selected destination project so you can track and investigate activity in the source project.

## What's included

An audit trail includes activity such as the following {{es}} and {{kib}} project events:

<!-- Unhide when org-level audit logs are available.
* **{{ecloud}} and organization administration:** Sign-ins; membership and IAM; and project settings.
-->
* {{kib}} sign-ins
* UI access, such as page navigation and UI requests
* Configuration changes to {{es}} resources, such as indices, templates, pipelines, and transforms
* Data access, including searches, reads, and writes

## Why deliver an audit trail

Delivering an audit trail to a project lets you investigate end-to-end activity in one place. For example, you can:

<!-- Unhide when org-level audit logs are available.
* Trace failed or successful sign-ins for a user
* Review membership, IAM, or project-admin changes
-->
* Detect suspicious sign-in activity
* Observe changes or deletions of {{kib}} saved objects such as detection rules
* Inspect access denied on an index pattern
* Determine who searched a sensitive index
* Follow a user journey across `service.name` values for the same `user.name` and time window

The destination project has several tools to help with your investigation. Refer to [Explore delivered logs](#explore-delivered-logs) for more information.

## Set up delivery for audit trail

Complete the following steps to configure audit trail log delivery in your project.

You must have the **Admin** or **Editor** [role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) on the source project.

::::::{stepper}

:::::{step} Navigate to log delivery

On your {{ecloud}} homepage, find the project that should be the source of your log deliveries and select **Manage**. From the navigation menu, select **Log delivery**.
:::::

:::::{step} Configure audit trail

For **Audit trail**, complete the following fields:

* In the **Destination** column, select an {{sec-serverless}} or {{obs-serverless}} project to receive the logs.
  
    ::::{tip}
    Since audit logs are security data, we recommend selecting a {{sec-serverless}} project as the destination for your audit trail. This lets you create your own detection rules on top of the delivered logs and use the SIEM capabilities of {{sec-serverless}} to alert on suspicious activity.
    ::::
* In the **Ignore filters** column, select filters to exclude certain events before delivery. Leave the list empty only if you want to deliver all events for that log type. 

    For filter details and recommended combinations, refer to [Audit trail ignore filters](#audit-trail-ignore-filters).
* Switch the toggle to **Enabled**.
:::::

:::::{step} Save and open delivered logs

Select **Save**.

When logs are available, you can select **View logs** or **View dashboards** to open the delivered audit trail on the destination project. Continue to [Explore delivered logs](#explore-delivered-logs) for more details.
:::::

:::::::

## Audit trail ignore filters

Apply ignore filters to exclude certain events from being delivered. Refer to [](/deploy-manage/monitor/log-delivery.md#ignore-filters) to learn more about their impact on your delivery volume and bill.

The following table describes which ignore filters are available for the audit trail log type and when to select them.

| Name | When to select |
| --- | --- |
| Ignore data searches and reads | Select to exclude the highest-volume events on search-heavy projects. Do not select if you need evidence of who searched or read data. |
| Ignore data writes | Select when you want configuration and object-change evidence without ingest and bulk write volume. |
| Ignore successful sign-ins | Select for security operations or minimal profiles that focus on failures. Do not select if you need successful sign-in accountability. Applies to authentication events in the audit trail. |
| Ignore routine user and role checks | Select for security operations or minimal profiles that focus on failures. Do not select if you need IAM accountability. Applies to IAM-related events in the audit trail. |
| Ignore UI requests | Select to exclude read-only UI navigation noise. Saved object mutations are still delivered. |

### Ignore filter combinations

In the following table, find the recommended combination of filters to select for typical use cases.

| Typical use | Ignore filters to select |
| --- | --- |
| General production | • Ignore data searches and reads<br>• Ignore UI requests |
| Change accountability without search noise | • Ignore data searches and reads |
| Failure-oriented monitoring | • Ignore data searches and reads<br>• Ignore UI requests<br>• Ignore successful sign-ins |
| Change management | • Ignore data searches and reads<br>• Ignore UI requests<br>• Ignore data writes |
| Dev or sandbox | All |
| Maximum end-to-end evidence | None |

## Explore delivered logs

After delivery is enabled, explore your audit trail on the destination project with the provided [dashboards](#dashboards), [alerting rules](#alerting-rules), [Discover or {{esql}}](#discover-or-esql), and [AutoOps](#autoops).

### Dashboards

When you enable an audit trail, the destination project creates dashboards to help you explore and investigate audit activity. Select **View dashboards** after you save your log delivery configuration, or open the destination project and find the audit trail dashboards in {{kib}}. 

The following dashboards are available:

* **Command Center**: Overview of audit activity, including volume, key indicators, higher-risk identities, and a live feed of recent events.
* **Identity 360**: Full activity trail for one user. Select a person to filter every panel to their events.
* **Identity & Access**: Sign-ins and access attempts by method, source, and outcome, with user identifiers resolved to real identities where available.
* **{{kib}} Object Forensics**: {{kib}} saved objects that were created, edited, deleted, or opened, grouped by type, name, space, and actor.
* **{{es}} Data Access**: Which indices each identity used, request types, denied requests, and access to system or hidden indices.
* **Security & Anomalies**: Risk signals for sensitive and privileged actions, operation failures, and newly seen identities.
* **Geo & Network**: Activity by geographic location, routed from each identity's real address, including unusual location patterns.

### Alerting rules

Set up alerting rules on the destination project to run continuously and notify you when sign-in or location patterns look suspicious, even when you're not watching the dashboards. These alerts link to the relevant dashboards for context, so you can use them together to enhance the security of your projects.

The destination project includes the following as templates. [Create a rule from each template](/reference/fleet/alerting-rule-templates.md) to receive alerts.

| Alerting rule | What triggers it |
| --- | --- |
| Password guessing | One identity fails to sign in at least 15 times in 10 minutes |
| Password spray | One client IP fails against at least 10 identities in 15 minutes |
| Credential stuffing | At least 30 failures, across 10 identities and 5 public IPs, in 10 minutes |
| Successful sign-in after repeated failures | At least 5 failures followed by a success, in the same 30 minutes |
| Impossible travel | Two sign-ins at least 500 km apart, at the same moment or faster than 800 km/h, within 6 hours |
| Sign-in from a new country | A known identity appears in a country it has not used in the last 7 days |
| Credential used from many places | Two countries in one hour, or an API key seen from 3 public IPs |
| First-seen identity | The first sign-in in 7 days<br> Stays quiet until the audit stream is at least 24 hours old, because it needs history to compare against. |

### Discover or {{esql}}

Select **View logs** after you save, or use Discover or {{esql}} on the destination project to explore delivered audit trail logs in the following locations:

| Data stream or index pattern | Contents |
| --- | --- |
| `logs-*_audit.otel-*` | All audit logs |
| `logs-elastic_cloud.serverless_audit.otel-default` | Project-level audit logs ({{es}} and {{kib}}) |

<!-- Unhide when org-level audit logs are available.
| `logs-elastic_cloud.org_audit.otel-default` | Organization-level audit logs (administration, configuration, billing, and similar) |
-->

:::{warning}
Restrict who can access these data streams in your destination project, because logs might include user identifiers and client IPs.
:::

#### Example queries

Explore the following examples of what you can investigate with your delivered audit logs. Run each query against `logs-*_audit.otel-*` in Discover.

##### Failed or denied activity

```esql
FROM logs-*_audit.otel-*
| WHERE event.outcome == "failure" OR event.action IN ("access_denied", "authentication_failed")
| KEEP @timestamp, user.name, user.id, event.action, event.outcome, source.ip, project.id, service.name
| SORT @timestamp DESC
| LIMIT 100
```

##### {{kib}} and saved-object changes

```esql
FROM logs-*_audit.otel-*
| WHERE event.action IN (
    "rule_create", "rule_delete", "rule_update",
    "saved_object_create", "saved_object_delete", "saved_object_update",
    "connector_create", "connector_delete", "connector_update",
    "space_update"
  )
| KEEP @timestamp, user.name, event.action, elastic_cloud.serverless_audit.space.id, elastic_cloud.serverless_audit.saved_object.type, elastic_cloud.serverless_audit.saved_object.id, service.name
| SORT @timestamp DESC
| LIMIT 100
```

##### Access denied on indices

```esql
FROM logs-*_audit.otel-*
| WHERE event.action == "access_denied"
| KEEP @timestamp, user.name, elastic_cloud.serverless_audit.action, elastic_cloud.serverless_audit.indices, source.ip, service.name
| SORT @timestamp DESC
| LIMIT 100
```

##### Who is changing configuration and objects

```esql
FROM logs-*_audit.otel-*
| WHERE event.type IN ("creation", "change", "deletion")
| STATS events = COUNT(*) BY user.name, event.action, service.name
| SORT events DESC
| LIMIT 20
```

##### Who searched a sensitive index

Do not select the **Ignore data searches and reads** filter for this query. Replace `<INDEX_PATTERN>` with the index or pattern to watch.

```esql
FROM logs-*_audit.otel-*
| WHERE event.action == "access_granted"
  AND elastic_cloud.serverless_audit.indices LIKE "<INDEX_PATTERN>"
| KEEP @timestamp, user.name, user.id, elastic_cloud.serverless_audit.action, elastic_cloud.serverless_audit.indices, source.ip, service.name
| SORT @timestamp DESC
| LIMIT 100
```

### AutoOps

Use the AutoOps [Storage Tier](/deploy-manage/monitor/autoops/storage-tier-view-autoops-serverless.md) view on the destination project to monitor your ingest rate and storage retained.

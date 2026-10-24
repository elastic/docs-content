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

An audit trail includes the following {{es}} and {{kib}} project events:

<!-- Unhide when org-level audit logs are available.
* **{{ecloud}} and organization administration:** Sign-ins; membership and IAM; and project settings.
-->
* Configuration changes for index, template, and pipeline changes
* Data access, including searches, reads, and writes
* UI access

Audit trail delivery is applicable to {{serverless-short}} projects, so {{ech}} fields like `node.*` and `host.*` are not included.

### Why deliver an audit trail

Delivering an audit trail into a project lets you investigate end-to-end activity in one place. For example, you can:

<!-- Unhide when org-level audit logs are available.
* Trace failed or successful sign-ins for a user
* Review membership, IAM, or project-admin changes
-->
* Investigate access denied on an index pattern
* Track create, update, or delete actions on indices, templates, or pipelines
* Detect changes or deletions of {{kib}} saved objects such as detection rules
* Determine who searched a sensitive index
* Follow a user journey across `service.name` values for the same `user.name` and time window

## Set up delivery for audit trail

Complete the following steps to configure audit trail log delivery in your project.

:::{note}
You must have the **Admin** or **Editor** [role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) on the source project.
:::

::::::{stepper}

:::::{step} Navigate to log delivery

On your {{ecloud}} homepage, find the project that should be the source of your log deliveries and select **Manage**. From the navigation menu, select **Log delivery**.
:::::

:::::{step} Configure audit trail

For **Audit trail**, complete the following fields:

* In the **Destination** column, select an {{sec-serverless}} or {{obs-serverless}} project to receive the logs.
  
    ::::{tip}
    Since audit logs are security data, we recommend selecting a {{sec-serverless}} project as the destination for your audit trail.
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

After delivery is enabled, explore your audit trail on the destination project with the provided [dashboards](#dashboards), [Discover or {{esql}}](#discover-or-esql), and [AutoOps](#autoops).

### Dashboards

Select **View dashboards** after you save, or open the destination project and find the audit trail dashboards in {{kib}}. The following dashboards are available:

* **Command Center**: Overview of audit activity, including volume, key indicators, higher-risk actors, and a live feed of recent events.
* **Actor 360**: Full trail for individual users. Select a person to filter every panel to their activity.
* **Identity & Access**: Sign-ins and access attempts, including method, source, and failures.
* **{{kib}} Object Forensics**: Insights on which {{kib}} saved objects were created, edited, deleted or opened. View this information grouped by type, name, space, and actor.
* **{{es}} Data Access**: Which indices each user accessed, the kinds of requests they made, and which requests were denied.
* **Security & Anomalies**: Risk rating for sensitive and privileged actions, along with operation failures and newly seen identities.
* **Geo & Network**: Observe activity by geographic location, routed from each user's real address.

### Discover or {{esql}}

Select **View logs** after you save, or use Discover or {{esql}} on the destination project to explore delivered audit trail logs in the following locations:

| Data stream or index pattern | Contents |
| --- | --- |
| `logs-*audit.otel-*` | All audit logs |
| `logs-elastic_cloud.serverless_audit.otel-default` | Project-level audit logs ({{es}}, {{kib}}, and {{ecloud}} project signals) |

<!-- Unhide when org-level audit logs are available.
| `logs-elastic_cloud.org_audit.otel-default` | Organization-level audit logs (administration, configuration, billing, and similar) |
-->

:::{warning}
Restrict who can access these locations in your destination project, because logs might include user identifiers and client IPs.
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
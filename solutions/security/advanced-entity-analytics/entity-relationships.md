---
navigation_title: Entity relationships
description: Learn how the entity store derives entity relationships such as access patterns and communication links from your ingested integration data.
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Entity relationships [entity-relationships]

Entity relationships represent the connections between entities — for example, `user-1 communicates_with host-1`. The [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) stores these connections as a fixed set of relationship keys on each entity record, under the schema `entity.relationships.<key>.ids`. Relationships feed entity analytics views, including the [entity graph](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) in the entity details flyout. Relationships are populated only when the entity store is enabled and populated in the active space.

The relationship model represents how entities interact across your environment. A clear mapping between integrations, fields, and relationship keys helps you understand:

* Which relationships exist and how they are populated.
* Which fields a third-party integration must emit for its data to participate in a given relationship.

## How relationships are produced [entity-relationships-maintainers]

Entity relationships are produced by *maintainers* — background tasks that scan ingested events from supported integrations and write the result into the entity store.

Each maintainer runs through the following steps:
1. Scans a specific integration's index pattern for events that match an {{esql}} filter
2. Identifies an actor (a user) and a target (a user, host, or service)
3. Computes the target entity's unique identifier (EUID)
4. Writes the relationship onto the actor entity under `entity.relationships.<key>.ids`.

## Requirements for an event to participate [entity-relationships-requirements]

For an event to be picked up by a maintainer, it must meet the following conditions:

* Land in the integration's index pattern (`logs-<integration>-<namespace>`).
* Carry the actor identity field used by the maintainer (typically `user.name`, `user.email`, or an integration-specific principal field).
* Match the maintainer's {{esql}} `WHERE` clause for that integration.
* Carry a resolvable target identity (for example, `host.id`, `host.target.entity.id`, or `user.target.email`).

## Supported relationships [entity-relationships-supported]

The following sections describe each supported relationship key, the integrations that populate it, and the criteria an event must match. To populate a relationship, ingest events into one of the listed integration indices with the required actor and target identity fields.

### `accesses_frequently` / `accesses_infrequently` relationships [entity-relationships-accesses]

These relationships are recalculated daily. Each run buckets an actor's accesses to a given target entity by event count over the previous 30 days: a `COUNT(*) >= 4` results in `accesses_frequently`; otherwise, the relationship is `accesses_infrequently`.

:::{table}
:widths: 2-3-1-6

| Integration | {{ipm-cap}} | Target type | {{esql}} filter applied |
| --- | --- | --- | --- |
| {{elastic-defend}} | `logs-endpoint.events.security-<ns>` | host | `event.action == "log_on" AND process.Ext.session_info.logon_type IN ("RemoteInteractive","Interactive","Network") AND event.outcome == "success"` |
| {{aws}} CloudTrail | `logs-aws.cloudtrail-<ns>` | host | `event.module == "aws" AND event.action IN ("StartSession","SendSSHPublicKey") AND event.outcome == "success"` |
| System Auth | `logs-system.auth-<ns>` | host | `event.category IN ("authentication","session") AND event.action == "ssh_login" AND event.outcome == "success"` |
| System Security | `logs-system.security-<ns>` | host | `event.action IN ("logged-in","logged-in-explicit") AND event.code IN ("4624","4648") AND winlog.logon.type IN ("Interactive","RemoteInteractive","CachedInteractive") AND event.outcome == "success"` (excludes built-in system accounts) |

:::

To populate `entity.relationships.accesses_frequently.ids` or `entity.relationships.accesses_infrequently.ids` for a user, ingest events into one of the supported integration indices with the actor identity (`user.name`, `user.id`, or `user.email`) and a target host identity (`host.id`, `host.name`, or `host.hostname`), and ensure they match the {{esql}} filter.

### The `communicates_with` relationship [entity-relationships-communicates-with]

This relationship captures when a user interacts with a target user or host — based on activity such as identity provider events, cloud API calls, and device management logs from the supported integrations.

:::{table}
:widths: 2-2-1-2-2-3

| Integration | {{ipm-cap}} | Target type | Actor field | Target field | {{esql}} filter applied |
| --- | --- | --- | --- | --- | --- |
| Okta | `logs-okta.system-<ns>` | user | `user.name` | `user.target.email` (→ `user:<email>@okta`) | `event.action IN (<Okta user/group/app lifecycle actions>) AND user.target.email IS NOT NULL` |
| Jamf Pro | `logs-jamf_pro.events-<ns>` | host | `user.name` | standard host EUID | `user.name IS NOT NULL` |
| {{aws}} CloudTrail | `logs-aws.cloudtrail-<ns>` | host | `user.name` | `host.target.entity.id` (→ `host:<id>`) | `aws.cloudtrail.user_identity.type IN ("IAMUser","AssumedRole","Root","FederatedUser","IdentityCenterUser") AND host.target.entity.id IS NOT NULL` |
| Azure Audit Logs | `logs-azure.auditlogs-<ns>` | user / host | `azure.auditlogs.properties.initiated_by.user.userPrincipalName` (→ `user:<upn>@entra_id`) | `target_resources.0.user_principal_name` (User) or `target_resources.0.display_name` (Device) | actor UPN present AND target is a User with UPN or a Device with display name |
:::

To populate `entity.relationships.communicates_with.ids` for a user, ingest events into one of the supported integration indices that match the filter and carry both actor and target identity fields.

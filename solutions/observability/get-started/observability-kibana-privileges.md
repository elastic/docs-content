---
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
description: Lists Kibana privileges in the Observability group of Assign role to spaces, with privilege levels and links to sub-feature catalogs.
---

# Observability {{kib}} privileges

Roles control what users can access and what actions they can perform. When you create or edit a role, you grant it [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), which give access to individual features within one or more spaces.

When you add {{kib}} privileges to a role, the **Assign role to spaces** flyout opens. Access to {{observability}} features is controlled by the privileges in the **Observability** group, described on this page.

For more details on creating a role, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for {{stack}}, or to [](/deploy-manage/users-roles/serverless-custom-roles.md) for {{serverless-short}}.

{{kib}} feature privileges do not grant {{es}} cluster or index privileges. Users still need the matching index privileges for the data they query.

## Access levels

For each of the feature privileges, select the type of access you want to allow:

:::{include} /deploy-manage/_snippets/feature-privilege-access-levels.md
:::

:::{note}
Some features don't have a **Read** privilege.
:::

## Privileges in the Observability group

Each of the following privileges controls access to a different part of {{observability}}.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Logs** | Access [Logs](/solutions/observability/logs.md) and related apps, including Logs Explorer. Create and manage logs alert rules and alerts. |
| **Infrastructure** | Access [Infrastructure](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and related metrics apps. Create and manage infrastructure alert rules and alerts. |
| **APM and User Experience** | Access [Applications (APM)](/solutions/observability/apm/index.md) and [User Experience](/solutions/observability/applications/user-experience.md). Create and manage APM alert rules and alerts. Turn on **Customize sub-feature privileges** to grant individual privileges. Refer to [APM and User Experience sub-feature privileges](#apm-and-user-experience-sub-feature-privileges).<br> {applies_to}`serverless: ga` In {{serverless-short}}, this privilege is called **Applications**. |
| **Synthetics and Uptime** | Access [Synthetics](/solutions/observability/synthetics/index.md) and [Uptime](/solutions/observability/uptime/index.md). Create and manage monitors, settings, and Synthetics and Uptime alert rules and alerts. Turn on **Customize sub-feature privileges** to grant individual privileges. Refer to [Synthetics and Uptime sub-feature privileges](#synthetics-and-uptime-sub-feature-privileges).<br> {applies_to}`serverless: ga` In {{serverless-short}}, this privilege is called **Synthetics**. |
| **Cases** | Access [cases](/explore-analyze/cases.md). Turn on **Customize sub-feature privileges** to grant individual case privileges. For the full list, refer to [Customize sub-feature privileges for cases](/explore-analyze/cases/control-case-access.md#cases-sub-feature-privileges). |
| **SLOs** | Access [service-level objectives (SLOs)](/solutions/observability/incident-management/service-level-objectives-slos.md). Create and manage SLOs and burn rate rules and alerts. For the matching {{es}} index privileges, refer to [Configure SLO access](/solutions/observability/incident-management/configure-service-level-objective-slo-access.md). |
| **Universal Profiling** | Access [Universal Profiling](/solutions/observability/infra-and-hosts/universal-profiling.md). **All** and **Read** grant the same Universal Profiling access. |
| **Observability Alerts** {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Read Observability alerts and perform per-alert actions such as snooze, unsnooze, and acknowledge, without managing rules. For details, refer to [Give access to triage alerts without managing rules](/explore-analyze/alerting/alerts/alerting-setup.md#_give_access_to_triage_alerts_without_managing_rules). |
| **Observability AI Assistant** | Access the [Observability AI Assistant](/solutions/observability/ai/observability-ai-assistant.md). This privilege has no **Read** level. |
| **Streams** {applies_to}`stack: ga =9.1, removed 9.2+` | Access [Streams](/solutions/observability/streams/streams.md).<br> {applies_to}`stack: ga 9.2+` This privilege is in the [**Management** group](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-management). |
| **Inventory** {applies_to}`stack: ga =9.0, removed 9.1+` | Access Inventory. Roles that use this privilege keep working only on 9.0. |
:::

:::{note}
:applies_to: {"serverless": "ga"}

In {{serverless-short}}, the **Observability** group also includes privileges that belong to the [**Analytics** group](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-analytics) or [**Management** group](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#kibana-privileges-management) in {{stack}}, such as Dashboards, Discover, Machine Learning, Workflows Management, Agent Builder, and Context Engine. Which ones appear depends on your [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
:::

## APM and User Experience sub-feature privileges

These privileges control specific Applications (APM) settings. Selecting **All** for **APM and User Experience** (or **Applications** in {{serverless-short}}) includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Ability to modify settings** | Change Applications (APM) settings. |
:::

## Synthetics and Uptime sub-feature privileges

These privileges control specific Synthetics actions. Selecting **All** for **Synthetics and Uptime** (or **Synthetics** in {{serverless-short}}) includes **Enabled** and **Can manage**. The other privileges in this table are opt-in: grant them separately even when the feature privilege is **All**.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Can run tests manually** {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | Trigger a manual test run of an existing monitor without creating, editing, or deleting monitors. |
| **Enabled** | Under **Elastic managed locations**, create monitors that run from Elastic managed locations. There is an additional charge to use Elastic managed testing locations. |
| **Can manage** | Under **Private locations**, add and delete private locations. |
| **Can read global parameter values** {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga` | View unredacted [global parameter](/solutions/observability/synthetics/work-with-params-secrets.md) values. |
| **Can manage rules** {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | Create, update, delete, enable, disable, run, and backfill Synthetics and Uptime alert rules, including the default status and TLS rules, without granting permission to create or edit monitors. |
:::

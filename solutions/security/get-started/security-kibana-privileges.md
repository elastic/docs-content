---
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Lists Kibana privileges in the Security group of Assign role to spaces, with privilege levels and links to sub-feature catalogs.
---

# Security {{kib}} privileges

Roles control what users can access and what actions they can perform. When you create or edit a role, you grant it [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), which give access to individual features within one or more spaces.

To create or edit a role, find **Roles** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Adding {{kib}} privileges opens the **Assign role to spaces** flyout, where features are grouped by solution. Access to {{elastic-sec}} features is controlled by the **Security** group privileges, described on this page.

For more details on using this UI, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md) for {{stack}}, or to [Custom roles](/deploy-manage/users-roles/cloud-organization/user-roles.md) for {{serverless-short}}.

## Access levels

For each of the feature privileges, select the type of access you want to allow:

:::{include} /deploy-manage/_snippets/feature-privilege-access-levels.md
:::

:::{note}
Some features don't have a **Read** privilege.
:::

## Privileges in the Security group

Each of the following privileges controls access to a different part of {{elastic-sec}}.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Security** | Access the {{elastic-sec}} features that don't have a privilege of their own. Turn on **Customize sub-feature privileges** to grant individual privileges. Refer to [Security sub-feature privileges](#security-sub-feature-privileges).<br> {applies_to}`stack: ga 9.0-9.2` **Security** also allows access to detection rules, alerts, and exceptions.  |
| **Cases** | Access cases. Turn on **Customize sub-feature privileges** to grant individual case privileges. For the full list, refer to [Customize sub-feature privileges for cases](/explore-analyze/cases/control-case-access.md#cases-sub-feature-privileges). |
| **Timeline** | Access [Timeline](/solutions/security/investigate/timeline.md). |
| **Notes** | Access [Notes](/solutions/security/investigate/notes.md). |
| **Rules and Exceptions** {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | Access detection rules and exceptions, including the {{rules-ui}} table, rule details, and rule monitoring. Turn on **Customize sub-feature privileges** to grant individual rule and exception privileges. For the full list, refer to [Rules and Exceptions sub-feature privileges](#rules-and-exceptions-sub-feature-privileges). |
| **Alerts** {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` | Access [detection alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md). |
| **Rules, Alerts, and Exceptions** {applies_to}`stack: ga =9.3, deprecated 9.4+` {applies_to}`serverless: deprecated` |  Access detection rules, alerts, and exceptions. Roles that use this privilege keep working, but the privilege is no longer available. Use **Rules and Exceptions** and **Alerts** instead. |
| **Elastic AI Assistant** | Access [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md). Turn on **Customize sub-feature privileges** to grant individual AI Assistant privileges. For the full list, refer to [Elastic AI Assistant sub-feature privileges](#elastic-ai-assistant-sub-feature-privileges). |
| **Attack discovery** | Access [Attack Discovery](/solutions/security/ai/attack-discovery/index.md).<br> {applies_to}`stack: ga 9.1+` {applies_to}`serverless: ga` Turn on **Customize sub-feature privileges** to grant individual Attack discovery privileges. For details, refer to [Attack discovery sub-feature privileges](#attack-discovery-sub-feature-privileges). |
| **Automatic Migration** | Access [Automatic Migration](/solutions/security/get-started/automatic-migration.md). <br> {applies_to}`stack: ga 9.0-9.2` This privilege is called **SIEM migrations**. |
:::

## Security sub-feature privileges

Unlike the other features in this group, selecting **All** for **Security** doesn't include its sub-feature privileges. You grant each one separately.

Most of the **Security** privileges control {{elastic-defend}} features. For the full list, refer to [{{elastic-defend}} sub-feature privileges](/solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md). The following table lists the rest.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **SOC Management** {applies_to}`stack: ga 9.3+` {applies_to}`serverless: ga` | Access the [Value report](/solutions/security/ai/ease/ease-value-report.md) page. |
:::

## Rules and Exceptions sub-feature privileges
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

These privileges control specific actions on detection rules and exceptions. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Exceptions** | Create and manage exceptions for rules and shared exception lists. If this privilege is cleared, users with **Read** for **Rules and Exceptions** can still view exception lists and exception items. |
| **Investigation guides** | Create and edit [investigation guides](/solutions/security/detect-and-alert/write-investigation-guides.md) on custom rules. |
| **Custom highlighted fields** | Add and edit [custom highlighted fields](/solutions/security/detect-and-alert/common-rule-settings.md#rule-ui-advanced-params) on rules. |
| **Enable or Disable** | Enable and disable detection rules. |
| **Manual rule run** | [Manually run rules](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) for a selected time range. |
| **Rule management settings** | Change **Settings** above the Rules table, including options that affect gap monitoring. |
:::

## Elastic AI Assistant sub-feature privileges

These privileges control changes to AI Assistant settings. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Field Selection and Anonymization** | Change which alert fields [Elastic AI Assistant](/solutions/security/ai/ai-assistant.md) and [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) can use, and anonymize the content of those fields. |
| **Knowledge Base** | Change global [Knowledge Base](/solutions/security/ai/ai-assistant-knowledge-base.md) entries, which apply to everyone in the space, including entries that other users created. |
:::

## Attack discovery sub-feature privileges
```yaml {applies_to}
stack: ga 9.1+
serverless: ga
```

These privileges control specific Attack Discovery actions. Selecting **All** includes everything in the following table.

:::{table}
:widths: description

| Privilege | What it allows |
| --- | --- |
| **Schedules** | Create, edit, enable, disable, and delete [Attack Discovery schedules](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md). |
:::

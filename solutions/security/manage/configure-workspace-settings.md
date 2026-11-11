---
description: Configure Kibana spaces, data views, and runtime fields for the Elastic Security app.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure workspace settings

Decide how your teams share the {{security-app}} and which data it shows them. You can give each team its own set of rules and alerts, add custom indices to the data that {{elastic-sec}} pages show, and add fields that you calculate from your existing data.

These settings affect every user who works in the same {{kib}} space, so change them when your teams, data sources, or investigation needs change.

## What each setting does

Use the following settings to organize your workspace:

- **Spaces**: Separate your security operations into independent workspaces. Detection rules, rule exceptions, value lists, alerts, Timelines, cases, and {{kib}} advanced settings in a space are only available to users who have access to that space.
- **{{data-sources-cap}}**: Decide which indices, data streams, and aliases appear on {{elastic-sec}} pages that show events or alerts. The first time a user opens {{elastic-sec}} in a space, the default {{data-source}} for that space generates. The default {{data-source}} doesn't include custom indices, so to show them, change the default {{data-source}} or create a new one. The **Alerts** page always reads from the alert index of the current space, whichever {{data-source}} is active.
- **Runtime fields**: Add calculated fields to the active {{data-source}}, such as two fields combined into one. {{es}} evaluates runtime fields each time a query runs, so they can affect performance.

## Where to start

| Your goal | Start here |
|---|---|
| Give teams separate rules, alerts, and cases | [Spaces and {{elastic-sec}}](/solutions/security/get-started/spaces-elastic-security.md) |
| {applies_to}`stack: preview 9.1` Understand how spaces scope {{elastic-defend}} policies, artifacts, and response actions | [Spaces and {{elastic-defend}} FAQ](/solutions/security/get-started/spaces-defend-faq.md) |
| Show data from custom indices, or switch the data that a page shows | [{{data-sources-cap}} and {{elastic-sec}}](/solutions/security/get-started/data-views-elastic-security.md) |
| Add a calculated field to your alerts and events | [Create runtime fields in {{elastic-sec}}](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md) |

## Next steps

After you configure your workspace, you can:

- [Give users access](/solutions/security/manage/access-control.md) to the features they need in each space.
- [Set data sources for detection rules](/solutions/security/detect-and-alert/set-rule-data-sources.md) to control which indices your rules search.

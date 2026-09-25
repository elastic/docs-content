---
navigation_title: Workspace settings
description: Configure the Elastic Security workspace, including spaces, data views that control which data appears, and runtime fields.
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Configure the {{elastic-sec}} workspace [security-workspace-settings]

These settings shape the {{elastic-sec}} workspace your analysts work in: how security operations are separated, which data appears on {{elastic-sec}} pages, and which additional fields are available in alerts and events.

| Setting | What it controls |
|---|---|
| [Spaces and {{elastic-sec}}](/solutions/security/workspace-settings/spaces-elastic-security.md) | Organize security operations into separate logical instances, each with its own detection rules, exceptions, alerts, Timelines, cases, and advanced settings. |
| [{{data-sources-cap}} and {{elastic-sec}}](/solutions/security/workspace-settings/data-views-elastic-security.md) | Control which indices, data streams, and aliases supply the data that appears on {{elastic-sec}} pages. |
| [Create runtime fields in {{elastic-sec}}](/solutions/security/workspace-settings/create-runtime-fields-in-elastic-security.md) | Add fields to alerts and events after ingest, for example by combining fields or calculating values at query time. |

To control which {{elastic-defend}} policies and artifacts are available in each space, refer to [Spaces and {{elastic-defend}} FAQ](/solutions/security/manage-elastic-defend/spaces-defend-faq.md).

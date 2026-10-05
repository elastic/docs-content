---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/ingest-data.html
  - https://www.elastic.co/guide/en/serverless/current/security-ingest-data.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Bring security data into Elastic Security. Start with an integration, use Automatic Import when none exists, or send data with Beats, Logstash, or a third-party collector.
---

# Ingest data to {{elastic-sec}} [security-ingest-data]

Detection rules, Attack Discovery, and the rest of {{elastic-sec}} work on the data you bring in. Most security data comes in through integrations, so start there.

## Start with an integration [security-ingest-integrations]

Elastic has hundreds of integrations that collect data from security tools, cloud services, identity providers, and operating systems. To find one, go to the **Integrations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Security** category. For the full catalog and each integration's documentation, refer to [Elastic integrations](integration-docs://reference/index.md).

Integrations collect data in one of two ways:

- {applies_to}`stack: ga 9.5+, preview 9.0-9.4` {applies_to}`serverless: ga` **{{managed-integrations}}:** Elastic runs the collector for you, so there's nothing to install or maintain. You configure the connection to the source, for example with an API key or cloud credentials. {{managed-integrations}} are available on {{serverless-full}} projects and {{ech}} deployments. To learn more, refer to [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md).
- **Integrations that use {{agent}}:** You install [{{agent}}](/reference/fleet/index.md) on the hosts you want to collect data from, and manage it with {{fleet}}.

## What integrations bring in [security-ingest-data-types]

Where data appears in {{elastic-sec}} depends on its type:

| Data | Where it appears in {{elastic-sec}} |
|---|---|
| Logs and events | Detection rules, [Timeline](/solutions/security/investigate/timeline.md), and [Discover](/solutions/security/investigate/discover-security.md) |
| Alerts from other security tools | The **Alerts** page, alongside alerts from your detection rules |
| Posture and vulnerability findings | The **Findings** page, and the entity and alert details flyouts |
| Threat intelligence | The [Indicators](/solutions/security/investigate/indicators-of-compromise.md) page and [indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) |

Integrations also install assets such as dashboards and saved searches. Some, such as [behavioral detection integrations](/solutions/security/advanced-entity-analytics/behavioral-detection-use-cases.md#ml-integrations), also install detection rules and {{ml}} jobs.

For the integrations that send alerts and findings to these pages, refer to [Integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md). For threat intelligence, refer to [Threat intel integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md).

## When no integration exists [security-ingest-no-integration]

If no integration exists for your data source, use [Automatic Import](/solutions/security/get-started/automatic-import.md) to create a custom integration from a sample of your data.

## Other ways to send data [security-ingest-other-methods]

You can also send data with:

* [{{beats}}](beats://reference/index.md) shippers installed on each system you want to monitor.
* **{{ls}}**, which ingests, transforms, and ships data in any format.
* Third-party collectors configured to ship data that conforms to the Elastic Common Schema (ECS). [](/reference/security/fields-and-object-schemas/siem-field-reference.md) lists the ECS fields that {{elastic-sec}} uses.

::::{important}
If you ship data with a third-party collector, or with {{ls}} plugins that don't use {{agent}} or {{beats}}, you must map its fields to [ECS](ecs://reference/index.md). You must also add its index to the {{elastic-sec}} indices by updating the `securitySolution:defaultIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings).

{{elastic-sec}} uses the [`host.name`](ecs://reference/ecs-host.md) ECS field as the primary key for identifying hosts.
::::

## Endpoint data [security-ingest-endpoint-data]

{{elastic-defend}} collects endpoint data as part of endpoint protection. To learn what it collects and how to deploy it, refer to [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md#elastic-defend-data).

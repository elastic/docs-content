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

Bring your security data into {{elastic-sec}} so detection rules, Attack Discovery, and other features can analyze it. Most security data comes in through integrations. If you're new to {{elastic-sec}}, start with {{elastic-defend}} to protect your hosts and collect endpoint data, or with an integration for a security tool you already use.

## Select your ingestion method [security-ingest-select-method]

The method you use depends on what you want to protect or monitor, and on where your data comes from. Find your goal in the following table:

| Your goal | Start here |
|---|---|
| Protect your hosts and collect endpoint data | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| Collect logs from your cloud, network, or identity tools | [Ingest data with an integration](#security-ingest-integrations) |
| Bring in findings and alerts from the security tools you already use | [Integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md) |
| Add threat intelligence | [Threat intel integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md) |
| Ingest data from a source that has no integration | [Automatic Import](/explore-analyze/ai-features/automatic-import.md) |
| Move rules and dashboards from Splunk, Microsoft Sentinel, or QRadar | [Automatic Migration](/solutions/security/get-started/automatic-migration.md), which also identifies the data sources your migrated rules need |
| Send data with {{beats}}, {{ls}}, or a third-party collector | [Send data with {{beats}}, {{ls}}, or third-party collectors](#security-ingest-other-methods) |

## Collect endpoint data with {{elastic-defend}} [security-ingest-endpoint-data]

If you want to protect your hosts, start with {{elastic-defend}}. It can block threats on each host, and it collects endpoint data, such as process, network, and file events. When you deploy it, you select a preset that sets which threats it prevents and which events it collects. To learn what it collects and how to deploy it, refer to [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md#elastic-defend-data).

## Ingest data with an integration [security-ingest-integrations]

Most of the other methods in the [ingestion method table](#security-ingest-select-method) use an integration, including third-party security tools and threat intelligence. Elastic has hundreds of integrations that collect data from security tools, cloud services, identity providers, and operating systems.

### Decide between managed and {{agent}} integrations [security-ingest-collection-methods]

Before you add an integration, decide how it collects data. Integrations collect data in one of two ways:

- {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` **{{managed-integrations}}:** Elastic runs the collector for you, so there's nothing to install or maintain. You connect to the source with credentials such as an API key. They're available on {{serverless-full}} projects and {{ech}} deployments. To learn more, refer to [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md).
- **Integrations that use {{agent}}:** You install [{{agent}}](/reference/fleet/index.md) on the hosts you want to collect data from, and manage it with {{fleet}}. On self-managed deployments, you also deploy a [{{fleet-server}}](/reference/fleet/fleet-server.md) to connect {{agent}} to {{fleet}}.

### Find and add an integration [security-ingest-add-integration]

After you decide how to collect the data, add the integration:

1. Go to the **Get started** page in {{elastic-sec}}, and select **Set up Security**.
2. In the **Ingest your data** section, select **Add data with integrations**.
3. Select an integration, or browse by category.

To browse the full catalog instead, go to the **Integrations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Security** category. For each integration's documentation, refer to [Elastic integrations](integration-docs://reference/index.md).

## What you can do with each type of data [security-ingest-data-types]

Each type of data that your integrations collect supports different tasks:

| Data type | What you can do with it |
|---|---|
| Logs and events | Detect threats with detection rules, and investigate events in [Timeline](/solutions/security/investigate/timeline.md) and [Discover](/solutions/security/investigate/discover-security.md). Monitor them with the dashboards and saved searches that integrations install. To find unusual activity, add [behavioral detection integrations](/solutions/security/advanced-entity-analytics/behavioral-detection-use-cases.md#ml-integrations), which install detection rules and {{ml}} jobs. |
| Posture and vulnerability findings | Review them on the [Findings](/solutions/security/cloud/findings-page.md) page, and see them as context in the entity and alert details flyouts. To find integrations that send findings, refer to [Integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md). |
| Threat intelligence | Match your events against known threat indicators with [indicator match rules](/solutions/security/detect-and-alert/indicator-match.md), and review indicators on the [Indicators](/solutions/security/investigate/indicators-of-compromise.md) page. To add threat intelligence sources, refer to [Threat intel integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md). |

<!--
Removed until verified: Integrations that power Findings and Alerts lists only Sysdig Falco as a source of alerts on the Alerts page. Confirm with the Security team whether alerts from other tools, such as CrowdStrike or SentinelOne, also appear there before restoring this row.

| Alerts from other security tools | Triage them on the [Alerts](/solutions/security/detect-and-alert/manage-detection-alerts.md) page, next to alerts from your detection rules. To find integrations that send alerts, refer to [Integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md). |
-->

## Ingest data from a source without an integration [security-ingest-no-integration]

If you can't find an integration for your data source, such as an in-house application or a less common tool, you can create one with [Automatic Import](/explore-analyze/ai-features/automatic-import.md). It uses a large language model (LLM) to analyze a sample of your data and create a custom integration. The custom integration maps your data to the [Elastic Common Schema (ECS)](ecs://reference/index.md), so you can use it in {{elastic-sec}} like data from any other integration.

## Send data with {{beats}}, {{ls}}, or third-party collectors [security-ingest-other-methods]

If you already use other tools to collect and ship data, you can send it to {{elastic-sec}} with:

* [{{beats}}](beats://reference/index.md) shippers installed on each system you want to monitor.
* [{{ls}}](logstash://reference/index.md), which ingests, transforms, and ships data in any format.
* Third-party collectors configured to ship data that conforms to ECS. [](/reference/security/fields-and-object-schemas/siem-field-reference.md) lists the ECS fields that {{elastic-sec}} uses.

{{elastic-sec}} reads data from a default set of index patterns, including `logs-*`, `filebeat-*`, and `winlogbeat-*`. Integrations write their logs to `logs-*` indices, and {{beats}} write to indices such as `filebeat-*`, so their data appears in {{elastic-sec}} without extra setup.

::::{important}
If you ship data with a third-party collector, or with {{ls}} plugins that don't use {{agent}} or {{beats}}, you must map its fields to [ECS](ecs://reference/index.md). You must also add its index to the {{elastic-sec}} indices by updating the `securitySolution:defaultIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings).

{{elastic-sec}} identifies hosts by the [`host.name`](ecs://reference/ecs-host.md) ECS field. If the same host sends data with different `host.name` values, it appears as more than one host.
::::

## Verify that your data reaches {{elastic-sec}} [security-ingest-verify]

Whichever method you use, confirm that your data reaches {{elastic-sec}}:

- Search for the data in [Discover](/solutions/security/investigate/discover-security.md).
- If you used an integration, open a dashboard that it installed. To find one, go to **Dashboards** and search for the integration's name.
- Check that the data's fields map correctly to ECS on the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md).

If the data appears in Discover but not on {{elastic-sec}} pages, check that its indices are part of your [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md).

## Next steps

After your data arrives, you can:

- [Install prebuilt detection rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that match the data you ingest.
- Read [Before you begin](/solutions/security/detect-and-alert/before-you-begin.md) to turn on detections and learn how rules work.
- Follow a [quickstart](/solutions/security/get-started/quickstarts.md) to complete a core task for your use case.

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

Bring your security data into {{elastic-sec}} so its analytics, including detection, investigation, and threat hunting, can work across all of it. {{elastic-sec}} can ingest data from anywhere, using native Elastic ingest tools as well as [third-party tools](#security-ingest-other-methods) such as Cribl and Kafka. The most common way to get data in is with integrations, which connect to hundreds of common security tools. Integrations handle both ingesting your events and normalizing them to the [Elastic Common Schema (ECS)](ecs://reference/index.md).

## Select your ingestion method [security-ingest-select-method]

The method you use depends on what you want to protect or monitor, and on where your data comes from. Find your goal in the following table:

| Your goal | Start here |
|---|---|
| Collect logs from your cloud, network, or identity tools | [Ingest data with an integration](#security-ingest-integrations) |
| Bring in findings from the security tools you already use | [Integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md) |
| Add threat intelligence | [Threat intel integrations](/solutions/security/get-started/enable-threat-intelligence-integrations.md) |
| Protect your hosts and collect endpoint data | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| Ingest data from a source that has no integration | [Automatic Import](/explore-analyze/ai-features/automatic-import.md) |
| Move rules and dashboards from Splunk, Microsoft Sentinel, or QRadar | [Automatic Migration](/solutions/security/get-started/automatic-migration.md), which also identifies the data sources your migrated rules need |
| Send data with {{beats}}, {{ls}}, or a third-party collector | [Send data with {{beats}}, {{ls}}, or third-party collectors](#security-ingest-other-methods) |

## Ingest data with an integration [security-ingest-integrations]

Elastic has hundreds of integrations that collect data from security tools, cloud services, identity providers, and operating systems. Integrations collect data in different ways, including APIs, syslog, cloud storage such as Amazon S3, and log files. Many include dashboards, so you can explore and visualize the data right away. Many also have related detection rules in {{elastic-sec}}, so you can start detecting threats as soon as the data arrives.

Each integration has its own documentation with setup steps and configuration options. To find the one for your source, refer to [Elastic integrations](integration-docs://reference/index.md). Most goals in the [ingestion method table](#security-ingest-select-method) start with an integration, including findings from third-party security tools and threat intelligence.

### Decide between managed and {{agent}} integrations [security-ingest-collection-methods]

On {{serverless-full}} projects and {{ech}} deployments, use an {{managed-integration}} whenever one is available for your source. It's the easiest way to get data in, because Elastic runs the collector for you and you only provide credentials. Not every integration is available as an {{managed-integration}}, so check the [{{managed-integrations}} quick reference](integration-docs://reference/managed_integrations.md) first. For other sources, and on self-managed deployments, use an integration that runs on {{agent}}.

The following table compares the two types of integration:

| Integration type | Who runs the collector | Data sources | To get started |
|---|---|---|---|
| {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md) | Elastic, on {{serverless-full}} projects and {{ech}} deployments. You only provide credentials, such as an API key. | Cloud services, through an API | Check whether your source has an {{managed-integration}} in the [{{managed-integrations}} quick reference](integration-docs://reference/managed_integrations.md). |
| Integrations that use [{{agent}}](/reference/fleet/index.md) | You. You install, update, and scale {{agent}} with {{fleet}}. | The host where {{agent}} runs, or remote sources such as syslog, cloud storage, or an API | [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md). |

### What you can do with each type of data [security-ingest-data-types]

You don't need every type of data to get started. Start with the data for the tasks that matter most to you, and add more later:

| Data type | What you can do with it | How to get it |
|---|---|---|
| Logs and events | Give the analytics and AI features in {{elastic-sec}} the context to detect threats and work out what happened across your environment. [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) groups related alerts into attack narratives, and [AI Assistant](/solutions/security/ai/triage-alerts.md) helps you interpret and prioritize alerts. Detection rules, {{ml}}, and dashboards turn the data into signals right away. You can also investigate events yourself in [Timeline](/solutions/security/investigate/timeline.md) and [Discover](/solutions/security/investigate/discover-security.md). | Add the integration for each tool or service that produces the logs. Many integrations come with related detection rules, so you can start detecting threats as soon as the data arrives. To also find unusual activity with {{ml}}, add [behavioral detection integrations](/solutions/security/advanced-entity-analytics/behavioral-detection-use-cases.md#ml-integrations). |
| Posture and vulnerability findings | Find the cloud resources that fail security guidelines and the hosts with known vulnerabilities, so you can decide what to fix first. When you investigate an alert, the same findings show whether the host or user involved has misconfigurations or vulnerabilities. Review them on the [Findings](/solutions/security/cloud/findings-page.md) page. | Add one of the [integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md). |
| Threat intelligence | Find out when activity in your environment involves known malicious IP addresses, domains, or files. [Indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) create an alert when your events match an indicator, and you can review each indicator on the [Indicators](/solutions/security/investigate/indicators-of-compromise.md) page. | Add a [threat intel integration](/solutions/security/get-started/enable-threat-intelligence-integrations.md). |
| Endpoint protection with {{elastic-defend}} | Prevent threats on your hosts and find out how an attack unfolded. {{elastic-defend}} is Elastic's endpoint protection. It blocks malware, ransomware, and other malicious behavior, and it collects endpoint data for investigation. When {{elastic-defend}} detects or blocks a threat, its [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) create an alert for you to triage. To see the processes that led to the alert, open it in the [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md). | [Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md). To also review process sessions in [Session View](/solutions/security/investigate/session-view.md), select **Collect session data** in the [integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection). |
| Endpoint data from other tools | Bring alerts and telemetry from the endpoint security tools you already use, such as CrowdStrike, Microsoft Defender for Endpoint, and SentinelOne, into the same place as the rest of your security data. The analytics and AI features in {{elastic-sec}} can then correlate endpoint activity with identity, cloud, and network data. | Add the integration for your endpoint tool. To find it, refer to [Elastic integrations](integration-docs://reference/index.md). |

### Find and add an integration [security-ingest-add-integration]

After you decide how to collect your data and which data you need, add the integration:

1. Go to the **Get started** page in {{elastic-sec}}, and select **Set up Security**.
2. In the **Ingest your data** section, select **Add data with integrations**.
3. Select an integration, or browse by category. To add {{elastic-defend}}, search for **{{elastic-defend}}** on the **Integrations** page instead.

   :::{tip}
   To browse the full catalog, go to the **Integrations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Security** category.
   :::

4. On the integration's page, select **Add** followed by the integration's name, such as **Add Okta**. Then follow the prompts to configure the integration.

   When you add {{elastic-defend}}, you select a preset and an {{agent}} policy, then install {{agent}} on each host you want to protect. For the full procedure, refer to [Install the {{elastic-defend}} integration](/solutions/security/configure-elastic-defend/install-elastic-defend.md).

## Ingest data from a source without an integration [security-ingest-no-integration]

If you can't find an integration for your data source, such as an in-house application or a less common tool, you can create one with [Automatic Import](/explore-analyze/ai-features/automatic-import.md). It uses a large language model (LLM) to analyze a sample of your data and create a custom integration. The custom integration maps your data to the [Elastic Common Schema (ECS)](ecs://reference/index.md), so you can use it in {{elastic-sec}} like data from any other integration.

## Send data with {{beats}}, {{ls}}, or third-party collectors [security-ingest-other-methods]

If you already use other tools to collect and ship data, you can send it to {{elastic-sec}} with:

* [{{beats}}](beats://reference/index.md) shippers installed on each system you want to monitor.
* [{{ls}}](logstash://reference/index.md), which ingests, transforms, and ships data in any format.
* Third-party collectors and shippers.

{{elastic-sec}} relies on data that conforms to ECS. Most integrations map their data to ECS with ingest pipelines. If you ship data another way, map it to ECS wherever you can. When all your sources use the same fields, detection rules, dashboards, and other {{elastic-sec}} features work with all your data. For the ECS fields that {{elastic-sec}} uses, refer to [](/reference/security/fields-and-object-schemas/siem-field-reference.md).

{{elastic-sec}} reads data from a default set of index patterns, including `logs-*`, `filebeat-*`, and `winlogbeat-*`. Integrations write their logs to `logs-*` indices, and {{beats}} write to indices such as `filebeat-*`, so their data appears in {{elastic-sec}} without extra setup.

::::{important}
If you ship data with a third-party collector, or with {{ls}} plugins that don't use {{agent}} or {{beats}}, you must add its index to the [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md) that {{elastic-sec}} uses. The default {{data-source}} reads the index patterns in the `securitySolution:defaultIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings), so add your index there. If you use a custom {{data-source}}, add your index to that {{data-source}} instead.
::::

## Verify that your data reaches {{elastic-sec}} [security-ingest-verify]

Whichever method you use, confirm that your data reaches {{elastic-sec}}:

- In [Discover](/solutions/security/investigate/discover-security.md), filter for documents from your source. For integration data, filter on the `data_stream.dataset` field, for example `data_stream.dataset : "okta.system"`. For data from other methods, filter on the index name, for example `_index : filebeat-*`. If no documents appear, refer to [Common problems with {{fleet}} and {{agent}}](/troubleshoot/ingest/fleet/common-problems.md). For {{managed-integrations}}, refer to the [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md#managed-integrations-faq-health).

  If documents appear in Discover but not on {{elastic-sec}} pages, the [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md) that {{elastic-sec}} uses doesn't include their index. Add the index to the `securitySolution:defaultIndex` advanced setting, or to your custom {{data-source}} if you use one.
- If you used an integration, open a dashboard that it installed. To find one, go to **Dashboards** and search for the integration's name.
- On the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md), select **Check now** for the index that holds your data. If the check fails, the **Incompatible fields** tab lists the fields that don't match ECS, so you know which ones to fix in your mappings or ingest pipeline.
- On the [Hosts](/solutions/security/advanced-entity-analytics/hosts-page.md) page, check that each host appears only once. {{elastic-sec}} identifies hosts by the [`host.name`](ecs://reference/ecs-host.md) field, so a host that sends different `host.name` values appears as more than one host.

## Next steps

After your data arrives, you can:

- Read [Before you begin](/solutions/security/detect-and-alert/before-you-begin.md) to turn on detections and learn how rules work.
- [Install prebuilt detection rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that match the data you ingest.
- Follow a [quickstart](/solutions/security/get-started/quickstarts.md) to complete a core task for your use case.

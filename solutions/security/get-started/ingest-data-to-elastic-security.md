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
description: Bring security data into Elastic Security. Start with an integration, build a custom integration when none exists, or send data with Beats, Logstash, or a third-party collector.
type: overview
---

# Ingest data to {{elastic-sec}} [security-ingest-data]

Bring your security data into {{elastic-sec}} so its analytics, including detection, investigation, and threat hunting, can work across all of it. {{elastic-sec}} can ingest data from anywhere, using native Elastic ingest tools as well as [third-party tools](#security-ingest-other-methods) such as Cribl and Kafka. The most common way to get data in is with integrations, which connect to hundreds of common security tools. Integrations handle both ingesting your events and normalizing them to the [Elastic Common Schema (ECS)](ecs://reference/index.md).

Use this page to find the right way to bring in each data source, add it, and confirm that the data reaches {{elastic-sec}}.

## Select your ingestion method [security-ingest-select-method]

The method you use depends on what you want to protect or monitor, and on where your data comes from. Find your goal in the following table:

| Your goal | Start here |
|---|---|
| Bring in logs, findings, threat intelligence, or alerts from the tools you already use, such as your cloud services, identity provider, or endpoint security tool | [Ingest data with an integration](#security-ingest-integrations) |
| Protect your hosts with Elastic's own endpoint protection | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| Ingest data from a source that has no integration | [Build a custom integration](#security-ingest-no-integration) with Automatic Import or Elastic integration skills |
| Move rules and dashboards from Splunk, Microsoft Sentinel, or QRadar | [Automatic Migration](/solutions/security/get-started/automatic-migration.md), which also identifies the data sources your migrated rules need |
| Send data with {{beats}}, {{ls}}, or a third-party collector | [Send data with {{beats}}, {{ls}}, or third-party collectors](#security-ingest-other-methods) |

## Ingest data with an integration [security-ingest-integrations]

Elastic has hundreds of integrations that collect data from security tools, cloud services, identity providers, and operating systems. Integrations collect data in different ways, including APIs, syslog, cloud storage such as Amazon S3, and log files. Many of them include dashboards for exploring your data and have related prebuilt detection rules that you can install and turn on.

Each integration has its own documentation with setup steps and configuration options. To find the one for your source, refer to [Elastic integrations](integration-docs://reference/index.md).

Before you add an integration, decide which data you need and how the integration collects it.

### Decide which data you need [security-ingest-data-types]

You don't need every type of data to get started. Start with the data for the tasks that matter most to you, and add more later:

| Data type | What you can do with it | How to get it |
|---|---|---|
| Logs and events | Detect threats and find out what happened across your environment. Detection rules create alerts from suspicious events, and [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) groups related alerts into attack narratives. To investigate, [AI Assistant](/solutions/security/ai/triage-alerts.md) helps you interpret and prioritize alerts, and you can explore events yourself in [Timeline](/solutions/security/investigate/timeline.md) and [Discover](/solutions/security/investigate/discover-security.md). | Add the integration for each tool or service that produces the logs. Then [install the prebuilt detection rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that match your data, and turn them on. To also find unusual activity with {{ml}}, add [behavioral detection integrations](/solutions/security/advanced-entity-analytics/behavioral-detection-use-cases.md#ml-integrations). |
| Posture and vulnerability findings | Find the cloud resources that fail security guidelines and the hosts with known vulnerabilities, so you can decide what to fix first. When you investigate an alert, the same findings show whether the host or user involved has misconfigurations or vulnerabilities. Review them on the [Findings](/solutions/security/cloud/findings-page.md) page. | To check your own cloud accounts and Kubernetes clusters against security guidelines, add Elastic's [cloud security posture management (CSPM)](/solutions/security/cloud/cloud-security-posture-management.md) or [Kubernetes security posture management (KSPM)](/solutions/security/cloud/kubernetes-security-posture-management.md) integration. To find known vulnerabilities in your cloud workloads, add [cloud native vulnerability management (CNVM)](/solutions/security/cloud/cloud-native-vulnerability-management.md). To bring in findings from other tools, add one of the [integrations that power Findings and Alerts](/solutions/security/integrations/ingest-third-party-security-data.md). |
| Threat intelligence | Find out when activity in your environment involves known malicious IP addresses, domains, or files. [Indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) create an alert when your events match an indicator, and you can review each indicator on the [Indicators](/solutions/security/investigate/indicators-of-compromise.md) page. | Add a [threat intel integration](/solutions/security/get-started/enable-threat-intelligence-integrations.md). |
| Endpoint data and alerts from {{elastic-defend}} | Prevent threats on your hosts and find out how an attack unfolded. {{elastic-defend}} blocks malware, ransomware, and other malicious behavior, and it collects endpoint data for investigation. When it detects or blocks a threat, its [endpoint protection rules](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) create an alert for you to triage. To see the processes that led to the alert, open it in the [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md). | [Install {{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md). To also review process sessions in [Session View](/solutions/security/investigate/session-view.md), select **Collect session data** in the [integration policy](/solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md#event-collection). |
| Alerts and data from other endpoint tools | Triage alerts from the endpoint security tools you already use, such as CrowdStrike, Microsoft Defender for Endpoint, and SentinelOne, on the same Alerts page as the rest of your alerts. The analytics and AI features in {{elastic-sec}} can then correlate endpoint activity with identity, cloud, and network data. | Add the integration for your endpoint tool. To find it, refer to [Elastic integrations](integration-docs://reference/index.md). To turn the tool's alerts into {{elastic-sec}} alerts, install and turn on its prebuilt promotion rule, such as [CrowdStrike External Alerts](detection-rules://rules/promotions/crowdstrike_external_alerts.md), or the general [External Alerts](detection-rules://rules/promotions/external_alerts.md) rule. |

### Decide between managed and {{agent}} integrations [security-ingest-collection-methods]

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` On {{serverless-full}} projects and {{ech}} deployments, use an {{managed-integration}} whenever one is available for your source. It's the easiest way to get data in, because Elastic runs and maintains the collector for you. Not every integration is available as an {{managed-integration}}, so check the [{{managed-integrations}} quick reference](integration-docs://reference/managed_integrations.md) first.

For other sources, and on self-managed deployments, use an integration that runs on {{agent}}. The following table compares the two types of integration:

| Integration type | Who runs the collector | Data sources | To get started |
|---|---|---|---|
| {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md) | Elastic. You only provide credentials, such as an API key. | Cloud services, through an API | [Enable an {{managed-integration}}](/manage-data/ingest/managed-integrations/enable-managed-integration.md). |
| Integrations that use [{{agent}}](/reference/fleet/index.md) | You. You install, update, and scale {{agent}} with {{fleet}}. | The host where {{agent}} runs, or remote sources such as syslog, cloud storage, or an API | [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md). |

### Find and add an integration [security-ingest-add-integration]

After you decide which data you need and how to collect it, add the integration:

1. Go to the **Get started** page in {{elastic-sec}}, and select **Set up Security**.
2. In the **Ingest your data** section, select **Add data with integrations**.
3. Select an integration, or browse by category.

   :::{tip}
   To browse the full catalog, go to the **Integrations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select the **Security** category.
   :::

4. On the integration's page, select **Add** followed by the integration's name, such as **Add Okta**.
5. Follow the prompts to configure the integration. If you're adding an {{managed-integration}}, also select it as the deployment mode:

   - {applies_to}`{serverless: ga, stack: ga 9.5+}` In the **Deployment** section, select **Elastic Managed Integration**.
   - {applies_to}`{stack: preview 9.0-9.4}` In the **Deployment options** section, select **Agentless**.

6. Select **Save and continue**.

When you're done, [verify that your data reaches {{elastic-sec}}](#security-ingest-verify).

## Ingest data from a source without an integration [security-ingest-no-integration]

If you can't find an integration for your data source, such as an in-house application or a less common tool, you can create a custom integration. Elastic offers two ways to build one, and both use a large language model (LLM). Either way, the custom integration maps your data to the [Elastic Common Schema (ECS)](ecs://reference/index.md), so you can use it in {{elastic-sec}} like data from any other integration.

| Option | Use it when | How you build the integration | What you need |
|---|---|---|---|
| [Automatic Import](/explore-analyze/ai-features/automatic-import.md) | You want a working integration quickly, and the integration can collect your data through a method that Automatic Import supports, such as files, cloud storage, Kafka, TCP, or UDP. | In {{kib}}, without writing code. You provide a sample of your data, and the LLM maps it to ECS and creates the integration. | An [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md), and an Enterprise subscription or the Security Analytics Complete project feature tier. For details, refer to the [Automatic Import requirements](/explore-analyze/ai-features/automatic-import.md#automatic-import-requirements). |
| [Elastic integration skills](https://github.com/elastic/integration-skills) | The integration must collect data from an HTTP API, or you want full control over the package, including its ingest pipelines, field mappings, dashboards, and tests. | In the AI coding environment you already use, such as Cursor, Claude Code, or Codex. AI agent workflows research your data source, then build and test the integration package. To use the finished package, [upload it to {{kib}}](integrations://extend/upload-new-integration.md). The skills are in beta, so expect them to change. | Experience building integration packages, and the tools that the skills run, such as Docker and the `elastic-package` CLI. |

## Send data with {{beats}}, {{ls}}, or third-party collectors [security-ingest-other-methods]

If you already use other tools to collect and ship data, you can send it to {{elastic-sec}} with:

* [{{beats}}](beats://reference/index.md), lightweight shippers that you install on each system you want to monitor.
* [{{ls}}](logstash://reference/index.md), a pipeline that ingests, transforms, and ships data in any format.
* Third-party collectors and pipelines, such as Cribl, and message queues, such as [Kafka](/manage-data/ingest/ingest-reference-architectures/agent-kafka-es.md).

{{elastic-sec}} relies on data that conforms to ECS. Most integrations map their data to ECS with ingest pipelines. If you ship data another way, map as much of it to ECS as you can. To learn how, refer to [Map custom data to ECS](ecs://reference/ecs-converting.md). When all your sources use the same fields, detection rules, dashboards, and other {{elastic-sec}} features work with all your data. For the ECS fields that {{elastic-sec}} uses, refer to [](/reference/security/fields-and-object-schemas/siem-field-reference.md).

{{elastic-sec}} reads data from a default set of index patterns, including `logs-*`, `filebeat-*`, and `winlogbeat-*`. Integrations write their logs to `logs-*` indices, and {{beats}} write to indices such as `filebeat-*`, so their data appears in {{elastic-sec}} without extra setup.

::::{important}
If your data goes to an index that doesn't match the default index patterns, such as a custom index that {{ls}} or a third-party collector writes to, add the index to the [{{data-source}}](/solutions/security/get-started/data-views-elastic-security.md) that {{elastic-sec}} uses. The default {{data-source}} reads the index patterns in the `securitySolution:defaultIndex` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings), so add your index there. If you use a custom {{data-source}}, add your index to that {{data-source}} instead.
::::

## Verify that your data reaches {{elastic-sec}} [security-ingest-verify]

Whichever method you use, confirm that your data reaches {{elastic-sec}}:

- In [Discover](/solutions/security/investigate/discover-security.md), select or create a {{data-source}} that includes your index, then filter for documents from your source. For integration data, filter on the `data_stream.dataset` field, for example `data_stream.dataset : "okta.system"`. For data from other methods, filter on the index name, for example `_index : filebeat-*`.

  - If no documents appear, refer to [Common problems with {{fleet}} and {{agent}}](/troubleshoot/ingest/fleet/common-problems.md). For {{managed-integrations}}, refer to the [{{managed-integrations}} FAQ](/manage-data/ingest/managed-integrations/managed-integrations-faq.md#managed-integrations-faq-health).
  - If documents appear in Discover but not on {{elastic-sec}} pages, the {{data-source}} that {{elastic-sec}} uses doesn't include their index. To fix this, [add the index to that {{data-source}}](#security-ingest-other-methods).

- If you used an integration, open a dashboard that it installed. To find one, go to **Dashboards** and search for the integration's name.
- On the [Data Quality dashboard](/solutions/security/dashboards/data-quality-dashboard.md), select **Check now** for the index that holds your data. If the check fails, the **Incompatible fields** tab lists the fields that don't match ECS, so you know which ones to fix in your mappings or ingest pipeline.
- On the [Hosts](/solutions/security/advanced-entity-analytics/hosts-page.md) page, check that each host appears only once. {{elastic-sec}} identifies hosts by the [`host.name`](ecs://reference/ecs-host.md) field, so a host that sends different `host.name` values appears as more than one host.

## Next steps

After your data arrives, you can:

- Read [Before you begin](/solutions/security/detect-and-alert/before-you-begin.md) to turn on detections and learn how rules work.
- [Install prebuilt detection rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that match the data you ingest.
- Follow a [quickstart](/solutions/security/get-started/quickstarts.md) to complete a core task for your use case.

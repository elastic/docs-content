---
navigation_title: Security solution
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/index.html
  - https://www.elastic.co/guide/en/security/current/es-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-overview.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-siem.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
  - id: kibana
description: Elastic Security brings SIEM, endpoint protection, and cloud security together, with AI features that help you detect, investigate, and respond to threats.
---

# {{elastic-sec}} solution overview [es-overview]

{{elastic-sec}} helps you detect, investigate, and respond to threats across your hosts, cloud services, and networks. It's built on {{es}} and {{kib}}, so you can search, correlate, and visualize your security data in one place. AI features can also translate rules from another SIEM and group related alerts into attacks.

## {{elastic-sec}} capabilities [elastic-security-capabilities]

{{elastic-sec}} has four main capabilities. You can use them together or start with one.

SIEM
:   Brings in security data from across your environment through hundreds of [integrations](/solutions/security/get-started/ingest-data-to-elastic-security.md), and detects threats with [prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) that Elastic maintains, your own rules, and {{ml}}. You can also investigate alerts and hunt for threats in [Timeline](/solutions/security/investigate/timeline.md) and the [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md), and track incidents in [cases](/solutions/security/investigate/security-cases.md). To try it, follow the [SIEM quickstart](/solutions/security/get-started/get-started-detect-with-siem.md).

Endpoint security
:   Detects and prevents malware, ransomware, in-memory threats, and malicious behavior on Windows, macOS, and Linux hosts with [{{elastic-defend}}](/solutions/security/configure-elastic-defend/install-elastic-defend.md), which runs on the same [{{agent}}](/reference/fleet/index.md) that collects your host data. You can also isolate hosts and take other [response actions](/solutions/security/respond-and-contain.md), including on hosts that run supported third-party EDR tools. To try it, follow the [endpoint security quickstart](/solutions/security/get-started/get-started-endpoint-security.md).

Cloud posture and vulnerability management
:   Finds misconfigurations in your cloud accounts and Kubernetes clusters by checking them against security benchmarks, with [cloud security posture management (CSPM) and Kubernetes security posture management (KSPM)](/solutions/security/cloud/security-posture-management-overview.md). A separate feature, [cloud native vulnerability management (CNVM)](/solutions/security/cloud/cloud-native-vulnerability-management.md), scans your Linux VMs in AWS for known vulnerabilities. To try posture management, follow the [cloud security posture quickstart](/solutions/security/get-started/get-started-cloud-security.md).

Cloud workload protection
:   Detects threats on your running Linux VMs, and can block some of them. {applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` It also protects Kubernetes containers. To learn how it works, refer to [Manage cloud workload protection](/solutions/security/manage/manage-cloud-workload-protection.md).

## AI in {{elastic-sec}} [ai-in-elastic-security]

{{elastic-sec}} also includes [AI features](/solutions/security/ai.md) that use large language models (LLMs). Depending on your deployment and license, you can use Elastic Managed LLMs through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) or an LLM from another provider. For details, refer to [Configure access to LLMs](/explore-analyze/ai-features/llm-guides/llm-connectors.md).

With AI features, you can:

* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+, preview =9.0` **Migrate from another SIEM:** [Automatic Migration](/solutions/security/get-started/automatic-migration.md) translates rules and dashboards from your existing SIEM into {{elastic-sec}} rules and dashboards, and identifies the data sources the translated rules need. Supported SIEMs and asset types vary by deployment type and {{stack}} version.
* **Onboard data sources without an integration:** [Automatic Import](/explore-analyze/ai-features/automatic-import.md) builds a custom integration from a sample of your data.
* **Triage high alert volumes:** [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) correlates related alerts into attacks, shows the hosts and users involved, maps the activity to MITRE ATT&CK, and suggests which threat actor might be responsible.
* **Investigate alerts and hunt for threats:** [AI chat](/solutions/security/ai.md#ai-chat-overview) answers questions about your alerts and data, and writes {{esql}} queries. You can use [AI Assistant](/solutions/security/ai/ai-assistant.md) or {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+, preview 9.3` [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md).
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+, preview 9.3` **Automate response:** Combine custom [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) agents with [Workflows](/explore-analyze/workflows.md) to isolate hosts, create cases, and send notifications.
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+, preview 9.0-9.1` **Keep endpoint protection working:** [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) finds issues that stop {{elastic-defend}} from working as intended, such as policy response failures and conflicts with third-party antivirus software.
* {applies_to}`serverless: preview` **Add AI to your current security tools:** In an [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) project, you can run Attack Discovery, AI Assistant, and cases on alerts from your existing SIEM or EDR/XDR platform, without replacing it.

## Start using {{elastic-sec}} [start-using-elastic-security]

To try {{elastic-sec}}, [start a free trial](https://cloud.elastic.co/serverless-registration). Which features you can use depends on how you run it. In {{sec-serverless}}, the Security Analytics [feature tiers](/solutions/security/security-serverless-feature-tiers.md) include SIEM, with add-ons for endpoint and cloud protection. In {{stack}} deployments, features depend on your [subscription](https://www.elastic.co/pricing).

To set up your deployment, follow [Get started with {{elastic-sec}}](/solutions/security/get-started.md). For a guided walkthrough of one area, use a [quickstart](/solutions/security/get-started/quickstarts.md).

## Related reference

* [{{elastic-sec}} reference documentation](/reference/security/index.md)
* [{{elastic-sec}} API documentation](/solutions/security/apis.md)
* [Fleet and Elastic Agent](/reference/fleet/index.md)
* [{{elastic-sec}} release notes](/release-notes/elastic-security/index.md)

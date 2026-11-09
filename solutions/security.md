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

{{elastic-sec}} helps you detect, investigate, and respond to threats across your hosts, cloud services, and networks. It's built on {{es}} and {{kib}}, so you can search, correlate, and visualize your security data in one place. AI features help you get through alert volume, tune noisy rules, and migrate your detection content from another SIEM.

## {{elastic-sec}} capabilities [elastic-security-capabilities]

{{elastic-sec}} has four main capabilities. You can use them together or start with one.

### SIEM [security-siem]

{{elastic-sec}} collects security data from across your environment through hundreds of [integrations](/solutions/security/get-started/ingest-data-to-elastic-security.md). It detects threats with Elastic-maintained prebuilt rules, your own rules, and {{ml}}.

When alerts come in, you can triage and investigate them, and hunt for threats in Timeline and the visual event analyzer. Cases keep a record of each investigation, from the first alert to resolution.

[Get started with SIEM →](/solutions/security/get-started/get-started-detect-with-siem.md)

### Endpoint security [security-endpoint-security]

{{elastic-defend}} detects and prevents malware, ransomware, in-memory threats, and malicious behavior on Windows, macOS, and Linux hosts. It runs on the same {{agent}} that collects your host data, so you deploy one agent for both.

When you confirm an attack, you can contain it by isolating hosts and taking other response actions. You can also take response actions on hosts that run supported third-party EDR tools.

[Get started with endpoint security →](/solutions/security/get-started/get-started-endpoint-security.md)

### Cloud posture and vulnerability management [security-cloud-posture]

Cloud security posture management (CSPM) and Kubernetes security posture management (KSPM) find misconfigurations in your cloud accounts and Kubernetes clusters by checking them against security benchmarks.

A separate feature, cloud native vulnerability management (CNVM), scans your Linux VMs in AWS for known vulnerabilities.

[Get started with cloud security posture management →](/solutions/security/get-started/get-started-cloud-security.md)

### Cloud workload protection [security-cloud-workload-protection]

{{elastic-defend}} also protects your Linux VMs while they run. It's the same integration that protects your other hosts, and it detects and prevents malware, memory threats, and malicious behavior.

It also sends process, file, and network activity to {{elastic-sec}}, where prebuilt rules and {{ml}} can find threats in it.

{applies_to}`serverless: beta` {applies_to}`stack: beta 9.3` For Kubernetes containers, Defend for Containers alerts on drift and can block process and file operations that match your policy.

[Learn more about cloud workload protection →](/solutions/security/manage/manage-cloud-workload-protection.md)

## AI in {{elastic-sec}} [ai-in-elastic-security]

{{elastic-sec}} also includes AI features that use large language models (LLMs). Depending on your deployment and license, you can use Elastic Managed LLMs through the [Elastic {{infer-cap}} Service (EIS)](/explore-analyze/elastic-inference/eis.md) or an LLM from another provider.

With AI features, you can:

* **Migrate from another SIEM:** [Automatic Migration](/solutions/security/get-started/automatic-migration.md) translates your existing detection rules and dashboards into {{elastic-sec}}, so you don't rebuild your detection content by hand. Supported SIEMs and asset types vary by deployment type and version. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+, preview =9.0`
* **Bring in data that has no integration:** [Automatic Import](/explore-analyze/ai-features/automatic-import.md) builds a custom integration from a sample of your logs.
* **Write and tune detection rules:** [Security skills](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#security-skills) in {{agent-builder}} draft {{esql}} rules from a plain-language description of what you want to detect. Depending on your version, they also suggest prebuilt rules for the integrations you already have, and find out why a rule is noisy. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+`
* **Get through alert volume:** [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) groups related alerts into attacks and maps them to MITRE ATT&CK®, so you triage one attack instead of each alert in it.
* **Investigate and respond:** [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) answers questions about your alerts and data, and writes {{esql}} queries for you. With [Workflows](/explore-analyze/workflows.md), custom agents can also isolate hosts, create cases, and send notifications, so you can automate routine response steps. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+, preview 9.3`
* **Keep endpoint protection working:** [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md) finds issues that stop {{elastic-defend}} from protecting your hosts, such as conflicts with third-party antivirus software. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.2+, preview 9.0-9.1`

:::{note}
:applies_to: {serverless: preview, stack: unavailable}
To add AI triage without replacing your current SIEM or EDR/XDR platform, use an [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md) project. It runs Attack Discovery, {{agent-builder}}, and cases on the alerts from that platform.
:::

[Learn more about AI in {{elastic-sec}} →](/solutions/security/ai.md)

## Start using {{elastic-sec}} [start-using-elastic-security]

To try {{elastic-sec}}, [start a free trial](https://cloud.elastic.co/serverless-registration). The features available to your team depend on how you run it. In {{sec-serverless}}, the Security Analytics [feature tiers](/solutions/security/security-serverless-feature-tiers.md) include SIEM, with add-ons for endpoint and cloud protection. In {{stack}} deployments, features depend on your [subscription](https://www.elastic.co/pricing).

If you run {{elastic-sec}} for several customers or teams, you can keep each one's rules, alerts, and cases separate in its own [space](/solutions/security/get-started/spaces-elastic-security.md). To detect threats in data stored elsewhere, detection rules can query other clusters with [{{ccs}}](/solutions/security/detect-and-alert/cross-cluster-search-detection-rules.md) in {{stack}} deployments, or other projects with [{{cps}}](/solutions/security/detect-and-alert/cross-project-search-detection-rules.md) in {{serverless-short}}.

For a guided walkthrough of one area, use a [quickstart](/solutions/security/get-started/quickstarts.md).

[Get started with {{elastic-sec}} →](/solutions/security/get-started.md)

## Related reference

* [{{elastic-sec}} reference documentation](/reference/security/index.md)
* [{{elastic-sec}} API documentation](/solutions/security/apis.md)
* [Fleet and Elastic Agent](/reference/fleet/index.md)
* [{{elastic-sec}} release notes](/release-notes/elastic-security/index.md)

{{elastic-sec}} brings SIEM (Security Information and Event Management), XDR (Extended Detection and Response), endpoint security, and cloud security into a single platform. Use it to detect, prevent, and respond to threats across your environment in near real time. It's built on {{es}} for search and analytics, and on {{kib}} for visualization and collaboration.

## What {{elastic-sec}} protects [security-what-it-protects]

{{elastic-sec}} covers four areas. You can use them together or start with one:

| Area | What it does | Start here |
|---|---|---|
| SIEM detection and response | Collects security data from across your environment, detects threats with rules and {{ml}}, and helps you investigate and respond. | [Detect and respond to threats with SIEM](/solutions/security/get-started/get-started-detect-with-siem.md) |
| Endpoint protection | Prevents and detects malware, ransomware, and malicious behavior on Windows, macOS, and Linux hosts with {{elastic-defend}}. | [Protect your hosts with endpoint security](/solutions/security/get-started/get-started-endpoint-security.md) |
| Cloud posture | Checks your cloud and Kubernetes configurations against security benchmarks, and scans cloud workloads for vulnerabilities. | [Secure your cloud assets with cloud security posture management](/solutions/security/get-started/get-started-cloud-security.md) |
| Cloud workload protection | Detects and blocks threats on cloud VMs and Kubernetes containers while they run. | [Cloud workload protection for VMs](/solutions/security/cloud/cloud-workload-protection-for-vms.md) |

Across these areas, [AI-assisted operations](/solutions/security/ai.md) help you automate alert triage, investigate threats, and streamline SOC work.

Which areas you can use depends on your deployment and license:

- {applies_to}`serverless: ga` In {{sec-serverless}}, the Security Analytics feature tiers include SIEM detection and response, with optional add-ons for endpoint protection and cloud protection. The Elastic AI SOC Engine (EASE) tier adds AI-powered threat hunting and alert triage to a third-party SIEM. Refer to [Serverless feature tiers](/solutions/security/security-serverless-feature-tiers.md).
- {applies_to}`stack: ga` In {{stack}} deployments, the features you can use depend on your [subscription](https://www.elastic.co/pricing).

## SIEM components in {{elastic-sec}} [security-siem-pieces]

In {{elastic-sec}}, SIEM detection and response relies on three components that you set up separately:

1. **Data collection:** [{{agent}}](/reference/fleet/index.md), centrally managed with {{fleet}}, collects data from your hosts. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+, preview 9.0-9.4` On {{ecloud}}, [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md) can also collect data from cloud sources without an agent.
2. **Integrations:** Hundreds of integrations bring in logs, alerts, findings, and threat intelligence from your security tools, cloud services, and identity providers, and normalize them to the [Elastic Common Schema (ECS)](ecs://reference/index.md). Refer to [Ingest data to {{elastic-sec}}](/solutions/security/get-started/ingest-data-to-elastic-security.md).
3. **Detection rules:** Elastic maintains prebuilt rules mapped to MITRE ATT&CK. You can also write your own in KQL, EQL, or {{esql}}, or use threshold, indicator match, new terms, and {{ml}} rules. {applies_to}`stack: preview =9.0, ga 9.1+` {applies_to}`serverless: ga` To bring over rules from Splunk, QRadar, or Microsoft Sentinel, use [Automatic Migration](/solutions/security/get-started/automatic-migration.md). Refer to [Detections and alerts](/solutions/security/detect-and-alert.md).

To set up each component, follow the steps in [Get started with {{elastic-sec}}](/solutions/security/get-started.md#security-get-started-steps).

## Core concepts [security-concepts]

These {{elastic-sec}} terms appear throughout the UI and the documentation.

:::{dropdown} Concepts
:open: 

* [**{{agent}}:**](/reference/fleet/index.md#elastic-agent) A single, unified way to collect logs, metrics, and other types of data from a host. {{agent}} can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware. 
* [**{{elastic-defend}}:**](/solutions/security/configure-elastic-defend/install-elastic-defend.md) {{elastic-sec}}'s Endpoint Detection and Response (EDR) tool that protects endpoints from malicious activity. {{elastic-defend}} uses a combination of techniques like machine learning, behavioral analysis, and prebuilt rules to detect, prevent, and respond to threats in real-time.
* [**{{elastic-endpoint}}:**](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md) The security component, enabled by {{agent}}, that performs {{elastic-defend}}'s threat monitoring and prevention capabilities. 
* [**Alerts:**](/solutions/security/detect-and-alert/manage-detection-alerts.md) Notifications that are generated when rule conditions are met. Alerts include a wide range of information about potential threats, including host, user, network, and other contextual data to assist your investigation.  
* [**Machine learning and anomaly detection:**](/solutions/security/advanced-entity-analytics/anomaly-detection.md) Anomaly detection jobs identify anomalous events or patterns in your data. Use these with machine learning detection rules to generate alerts when behavior deviates from normal activity.
* [**Entity analytics:**](/solutions/security/advanced-entity-analytics/monitor-entity-risk.md) A threat detection feature that combines the power of Elastic’s detection engine and machine learning capabilities to identify unusual behavior for hosts, users, and services. 
* [**Cases:**](/solutions/security/investigate/security-cases.md) Allows you to collect and share information about security issues. Opening a case lets you track key investigation details and collect alerts in a central location. You can also send cases to external systems.
* [**Timeline:**](/solutions/security/investigate/timeline.md) Investigate security events so you can gather and analyze data related to alerts or suspicious activity. You can add events to Timeline from various sources, build custom queries, and import/export a Timeline to collaborate and share. 
* [**Agent Builder:**](/solutions/security/ai/agent-builder/agent-builder.md) Elastic's AI agent platform with a natural language chat interface, built-in agents and tools for security use cases, and the ability to create custom agents and tools. Starting in 9.4, Agent Builder is the default chat experience in {{elastic-sec}}.
* [**AI Assistant:**](/solutions/security/ai/ai-assistant.md) Helps with tasks like alert investigation, incident response, and query generation. It utilizes natural language processing and knowledge retrieval to provide context-aware assistance, summarize threats, suggest next steps, and automate workflows. Use AI Assistant to better understand and respond to security incidents.
* [**Attack Discovery:**](/solutions/security/ai/attack-discovery/index.md) Uses large language models (LLMs) to analyze security alerts, identify coordinated attack patterns, and provide actionable intelligence to security operations teams. It improves alert triage efficiency by automatically correlating related alerts into comprehensive, simplified threat summaries, allowing you to quickly understand and respond to the most impactful attacks.
* [**Elastic AI SOC Engine (EASE):**](/solutions/security/ai/ease/ease-intro.md) Integrates Elastic's AI-powered security tools into existing SIEM and EDR/XDR platforms to help mitigate alert fatigue, accelerate threat investigations, and improve response efficiency ({{serverless-short}} only).
:::

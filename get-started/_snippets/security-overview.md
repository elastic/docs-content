Depending on your subscription and project type, {{elastic-sec}} provides security information and event management (SIEM), extended detection and response (XDR), endpoint protection, and cloud security. It uses {{es}} search and analytics with {{kib}} visualization and collaboration features.

Use {{elastic-sec}} in an {{ech}} deployment, a {{serverless-short}} Security project, or a self-managed deployment.
Refer to each linked feature page for its subscription and deployment requirements.

## Use cases [security-use-cases]

Use {{elastic-sec}} to protect your systems from security threats.

:::{dropdown} Use cases
:open:

* [**SIEM:**](https://www.elastic.co/security/siem): {{elastic-sec}} provides a centralized platform for ingesting, analyzing, and managing security data from various sources.
* [**Third-party integration support**](/solutions/security/get-started/ingest-data-to-elastic-security.md): Ingest data from third-party tools and data sources to centralize your security data.
* [**Threat detection and analytics:**](/solutions/security/detect-and-alert.md): Identify threats by using [prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md), custom detection rules, built-in machine learning jobs, and [threat hunting and interactive visualization tools](/solutions/security/investigate.md).
* [**Automatic migration**](/solutions/security/get-started/automatic-migration.md): Migrate SIEM rules from Splunk, IBM QRadar, and Microsoft Sentinel to Elastic detection rules.
* [**Endpoint protection and threat prevention**](/solutions/security/configure-elastic-defend.md): Configure malware, ransomware, memory-threat, and malicious-behavior protections to detect and block supported threats.
* [**AI-powered features**](/solutions/security/ai.md): Leverage generative AI to help enhance threat detection, assist with incident response, and improve day-to-day security operations.
* [**Custom dashboards and visualizations**](/solutions/security/dashboards.md): Create custom dashboards and visualizations to gain insights into security events.
* [**Cloud Security**](/solutions/security/cloud.md): {{elastic-sec}} provides the following cloud features:
  * **Cloud Security Posture Management (CSPM) and Kubernetes Security Posture Management (KSPM):** Check cloud service configurations against security benchmarks to identify and resolve misconfigurations that can be exploited.
  * **Cloud Workload Protection:** Get visibility and runtime protection for cloud workloads.
  * **Vulnerability Management:** Uncover vulnerabilities within your cloud infrastructure.
:::

If you're new to {{elastic-sec}} and want to try it out, go to [](/solutions/security/get-started.md) and [](/solutions/security/get-started/quickstarts.md).

## Core concepts [security-concepts]

Before diving into setup and configuration, familiarize yourself with the foundational terms and core concepts that power {{elastic-sec}}.

:::{dropdown} Concepts
:open: 

* [**{{agent}}:**](/reference/fleet/index.md#elastic-agent) A single, unified way to collect logs, metrics, and other types of data from a host. {{agent}} can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware. 
* [**{{elastic-defend}}:**](/solutions/security/configure-elastic-defend/install-elastic-defend.md) {{elastic-sec}}'s endpoint detection and response (EDR) tool. It provides machine learning malware protection and ransomware, memory-threat, malicious-behavior, and credential-theft protections. The detection engine separately provides prebuilt and custom detection rules.
* [**{{elastic-endpoint}}:**](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md) The security component, enabled by {{agent}}, that performs {{elastic-defend}}'s threat monitoring and prevention capabilities. 
* [**Detection engine:**](/solutions/security/detect-and-alert.md) The framework that detects threats by using rules to search for suspicious events in your data, and generates alerts when events meet a rule's criteria.
* [**Detection rules:**](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) Sets of conditions that identify potential threats and malicious activities. Rules analyze various data sources, including logs and network traffic, to detect anomalies, suspicious behaviors, or known attack patterns. {{elastic-sec}} ships out-of-the-box prebuilt rules, and you can create your own custom rules. 
* [**Alerts:**](/solutions/security/detect-and-alert/manage-detection-alerts.md) Records generated when rule conditions are met. Alerts include host, user, network, and other contextual data to assist your investigation. Configure optional rule actions to send notifications through connectors.
* [**Machine learning and anomaly detection:**](/solutions/security/advanced-entity-analytics/anomaly-detection.md) Anomaly detection jobs identify anomalous events or patterns in your data. Use these with machine learning detection rules to generate alerts when behavior deviates from normal activity.
* [**Entity analytics:**](/solutions/security/advanced-entity-analytics/monitor-entity-risk.md) A threat detection feature that combines the power of Elastic’s detection engine and machine learning capabilities to identify unusual behavior for hosts, users, and services. 
* [**Cases:**](/solutions/security/investigate/security-cases.md) Allows you to collect and share information about security issues. Opening a case lets you track key investigation details and collect alerts in a central location. You can also send cases to external systems.
* [**Timeline:**](/solutions/security/investigate/timeline.md) Investigate security events so you can gather and analyze data related to alerts or suspicious activity. You can add events to Timeline from various sources, build custom queries, and import/export a Timeline to collaborate and share. 
* [**Security posture management:**](/solutions/security/cloud.md) Includes native cloud security features, such as Cloud Security Posture Management (CSPM) and Cloud Native Vulnerability Management (CNVM), that help you evaluate your cloud infrastructure's configuration against security best practices and identify vulnerabilities. You can use Elastic's native tools or ingest third-party cloud security data and incorporate it into {{elastic-sec}}'s workflows.
* [**Agent Builder:**](/solutions/security/ai/agent-builder/agent-builder.md) Elastic's AI agent platform with a natural language chat interface, a default Elastic AI Agent with security skills and tools, and support for custom agents and tools. Starting in 9.4, Agent Builder is the default chat experience in {{elastic-sec}}.
* [**AI Assistant:**](/solutions/security/ai/ai-assistant.md) Helps with alert investigation, incident response, query generation, threat summaries, and knowledge retrieval.
* [**Attack Discovery:**](/solutions/security/ai/attack-discovery/index.md) From **Detections → Attacks**, use Attack Discovery to correlate related security alerts into attack summaries with large language models (LLMs).
* [**Elastic AI SOC Engine (EASE):**](/solutions/security/ai/ease/ease-intro.md) Integrates Elastic AI-powered security tools with supported third-party SIEM and EDR/XDR platforms. EASE is available only in {{serverless-short}} projects and doesn't include endpoint or cloud-protection add-ons.
:::

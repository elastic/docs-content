---
navigation_title: Security
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
description: Elastic Security combines threat detection analytics, cloud native security, and endpoint protection capabilities in a single solution.
---

# {{elastic-sec}} overview [es-overview]

:::{include} ../get-started/_snippets/security-overview.md
:::

<!--{{elastic-sec}} is a unified security solution that unifies SIEM (Security Information and Event Management), XDR, (Extended Detection and Response), endpoint security, and cloud security into a single platform so you can detect, prevent, and respond to cyber threats across your entire environment in near real time.
{{elastic-sec}} leverages {{es}}'s powerful search and analytics capabilities, and {{kib}}'s visualization and collaboration features.
By combining prevention, detection, and response capabilities, {{elastic-sec}} helps your organization reduce its security risk.

{{elastic-sec}} provides:

* A detection engine that identifies a wide range of threats
* A workspace for event triage, investigation, and case management
* Interactive data visualization tools
* Integrations for collecting data from various sources

Install {{elastic-sec}} on one of our {{ecloud}} deployments or your own self-managed infrastructure.  

## Use cases [security-use-cases]

Use {{elastic-sec}} to protect your systems from security threats.

:::{dropdown} Use cases

* **SIEM:** {{elastic-sec}}'s modern SIEM provides a centralized platform for ingesting, analyzing, and managing security data from various sources. 
* **Third-party integration support:** Ingest data from a various tools and data sources so you can centralize your security data.
* **Threat detection and analytics:** Identify threats by using prebuilt rules with the ability to customize or create custom detection rules, automatically detect anomalous activity with built-in machine learning jobs, or proactively search for threats using our powerful threat hunting and interactive visualization tools. 
* **Automatic migration:** Migrate SIEM rules from other platforms to {{elastic-sec}}. 
* **Endpoint protection and threat prevention:** Automatically stop cybersecurity attacks—such as malware and ransomware—before damage and loss can occur.
* **AI-powered features:** Leverage generative AI to help enhance threat detection, assist with incident response, and improve day-to-day security operations.
* **Custom dashboards and visualizations:** Create custom dashboards and visualizations to gain insights into security events.
* **Cloud Security:** {{elastic-sec}} provides the following cloud features:
  * **Cloud Security Posture Management (CSPM) and Kubernetes Security Posture Management (KSPM):** Check cloud service configurations against security benchmarks to identify and resolve misconfigurations that can be exploited.
  * **Cloud Workload Protection:** Get visibility and runtime protection for cloud workloads.
  * **Vulnerability Management:** Uncover vulnerabilities within your cloud infrastructure.
::: 

If you're new to {{elastic-sec}} and want to try it out, go to [](/solutions/security/get-started.md) and [](/solutions/security/get-started/quickstarts.md). 

## Core concepts [security-concepts]

Before diving into setup and configuration, familiarize yourself with the foundational terms and core concepts that power {{elastic-sec}}.

:::{dropdown} Concepts 

* [**{{agent}}:**](/reference/fleet/index.md#elastic-agent) A single, unified way to collect logs, metrics, and other types of data from a host. {{agent}} can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware. 
* [**{{elastic-defend}}:**](/solutions/security/configure-elastic-defend/install-elastic-defend.md) {{elastic-sec}}'s Endpoint Detection and Response (EDR) tool that protects endpoints from malicious activity. {{elastic-defend}} uses a combination of techniques like machine learning, behavioral analysis, and prebuilt rules to detect, prevent, and respond to threats in real-time.
* [**{{elastic-endpoint}}:**](/solutions/security/manage-elastic-defend/elastic-endpoint-self-protection-features.md) The security component, enabled by {{agent}}, that performs {{elastic-defend}}'s threat monitoring and prevention capabilities. 
* [**Detection engine:**](/solutions/security/detect-and-alert.md) The framework that detects threats by using rules to search for suspicious events in your data, and generates alerts when events meet a rule's criteria.
* [**Detection rules:**](/solutions/security/detect-and-alert/about-detection-rules.md) Sets of conditions that identify potential threats and malicious activities. Rules analyze various data sources, including logs and network traffic, to detect anomalies, suspicious behaviors, or known attack patterns. {{elastic-sec}} ships out-of-the-box prebuilt rules, and you can create your own custom rules. 
* [**Alerts:**](/solutions/security/detect-and-alert/manage-detection-alerts.md) Notifications that are generated when rule conditions are met. Alerts include a wide range of information about potential threats, including host, user, network, and other contextual data to assist your investigation.  
* [**Machine learning and anomaly detection:**](/solutions/security/advanced-entity-analytics/anomaly-detection.md) Anomaly detection jobs identify anomalous events or patterns in your data. Use these with machine learning detection rules to generate alerts when behavior deviates from normal activity.
* [**Entity analytics:**](/solutions/security/advanced-entity-analytics/overview.md) A threat detection feature that combines the power of Elastic’s detection engine and machine learning capabilities to identify unusual behavior for hosts, users, and services. 
* [**Cases:**](/solutions/security/investigate/cases.md) Allows you to collect and share information about security issues. Opening a case lets you track key investigation details and collect alerts in a central location. You can also send cases to external systems.
* [**Timeline:**](/solutions/security/investigate/timeline.md) Investigate security events so you can gather and analyze data related to alerts or suspicious activity. You can add events to Timeline from various sources, build custom queries, and import/export a Timeline to collaborate and share. 
* [**Security posture management:**](/solutions/security/cloud.md) Includes native cloud security features, such as Cloud Security Posture Management (CSPM) and Cloud Native Vulnerability Management (CNVM), that help you evaluate your cloud infrastructure's configuration against security best practices and identify vulnerabilities. You can use Elastic's native tools or ingest third-party cloud security data and incorporate it into {{elastic-sec}}'s workflows.
* [**AI Assistant:**](/solutions/security/ai/ai-assistant.md) Helps with tasks like alert investigation, incident response, and query generation. It utilizes natural language processing and knowledge retrieval to provide context-aware assistance, summarize threats, suggest next steps, and automate workflows. Use AI Assistant to better understand and respond to security incidents.
* [**Attack Discovery:**](/solutions/security/ai/attack-discovery.md) Uses large language models (LLMs) to analyze security alerts, identify coordinated attack patterns, and provide actionable intelligence to security operations teams. It improves alert triage efficiency by automatically correlating related alerts into comprehensive, simplified threat summaries, allowing you to quickly understand and respond to the most impactful attacks.
* [**Elastic AI SOC Engine (EASE):**](/solutions/security/ai/ease/ease-intro.md) Integrates Elastic's AI-powered security tools into existing SIEM and EDR/XDR platforms to help mitigate alert fatigue, accelerate threat investigations, and improve response efficiency ({{serverless-short}} only). 
:::
-->

## Learn more [siem-integration]

* [Get started](security/get-started.md): Learn about system requirements, workspaces, configuration, and data ingestion.
* [{{elastic-sec}} UI overview](security/get-started/elastic-security-ui.md): Navigate {{elastic-sec}}'s various tools and interfaces.
* [Detection rules](security/detect-and-alert/about-detection-rules.md): Use {{elastic-sec}}'s detection engine with custom and prebuilt rules.
* [Cloud security](security/cloud.md): Enable cloud native security capabilities such as Cloud and Kubernetes security posture management, cloud native vulnerability management, and cloud workload protection for Kubernetes and VMs.
* [Install {{elastic-defend}}](security/configure-elastic-defend/install-elastic-defend.md): Enable key endpoint protection capabilities like event collection and malicious activity prevention.
* [{{ml-cap}}](https://www.elastic.co/products/stack/machine-learning): Enable built-in {{ml}} tools to help you identify malicious behavior.
* [Advanced entity analytics](security/advanced-entity-analytics.md): Leverage {{elastic-sec}}'s detection engine and {{ml}} capabilities to generate comprehensive risk analytics for hosts and users.
* [Elastic AI assistant](security/ai/ai-assistant.md): Ask AI Assistant questions about how to use {{elastic-sec}}, how to understand particular alerts and other documents, and how to write {{esql}} queries.
* [{{elastic-sec}} fields and object schemas](/reference/security/fields-and-object-schemas/index.md): Learn how to structure data for use with {{elastic-sec}}.

### {{es}} and {{kib}} [elastic-search-and-kibana]

{{elastic-sec}} uses {{es}} for data storage, management, and search, and {{kib}} is its main user interface. Learn more:

* [{{es}}](https://www.elastic.co/products/elasticsearch): A real-time, distributed storage, search, and analytics engine. {{elastic-sec}} stores your data using {{es}}.
* [{{kib}}](https://www.elastic.co/products/kibana): An open-source analytics and visualization platform designed to work with {{es}} and {{elastic-sec}}. {{kib}} allows you to search, view, analyze and visualize data stored in {{es}} indices.

### {{elastic-endpoint}} self-protection [self-protection]

For information about {{elastic-endpoint}}'s tamper-protection features, refer to [{{elastic-endpoint}} self-protection](security/manage-elastic-defend/elastic-endpoint-self-protection-features.md).
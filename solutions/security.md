---
navigation_title: "Security"
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/es-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-overview.html
---

# {{elastic-sec}} overview [es-overview]

{{elastic-sec}} combines threat detection analytics, cloud native security, and endpoint protection capabilities in a single solution, so you can quickly detect, investigate, and respond to threats and vulnerabilities across your environment.

{{elastic-sec}} provides:

* A detection engine that identifies a wide range of threats
* A workspace for event triage, investigation, and case management
* Interactive data visualization tools
* Integrations for collecting data from various sources


## Learn more [siem-integration] 

* [Get started](security/get-started.md): Learn about system requirements, workspaces, configuration, and data ingestion.
* [{{elastic-sec}} UI overview](security/get-started/elastic-security-ui.md): Navigate {{elastic-sec}}'s various tools and interfaces.
* [Detection rules](security/detect-and-alert/about-detection-rules.md): Use {{elastic-sec}}'s detection engine with custom and prebuilt rules.
* [Cloud security](security/cloud.md): Enable cloud native security capabilities such as Cloud and Kubernetes security posture management, cloud native vulnerability management, and cloud workload protection for Kubernetes and VMs.
* [Install {{elastic-defend}}](security/configure-elastic-defend/install-elastic-defend.md): Enable key endpoint protection capabilities like event collection and malicious activity prevention.
* [{{ml-cap}}](https://www.elastic.co/products/stack/machine-learning): Enable built-in {{ml}} tools to help you identify malicious behavior.
* [Advanced entity analytics](security/advanced-entity-analytics.md): Leverage {{elastic-sec}}'s detection engine and {{ml}} capabilities to generate comprehensive risk analytics for hosts and users.
* [Elastic AI assistant](security/ai/ai-assistant.md): Ask AI Assistant questions about how to use {{elastic-sec}}, how to understand particular alerts and other documents, and how to write {{esql}} queries.
* [{{elastic-sec}} fields and object schemas](https://www.elastic.co/guide/en/security/current/security-ref-intro.html): Learn how to structure data for use with {{elastic-sec}}.


## {{es}} and {{kib}} [elastic-search-and-kibana] 

{{elastic-sec}} uses {{es}} for data storage, management, and search, and {{kib}} is its main user interface. Learn more:

* [{{es}}](https://www.elastic.co/products/elasticsearch): A real-time, distributed storage, search, and analytics engine. {{elastic-sec}} stores your data using {{es}}.
* [{{kib}}](https://www.elastic.co/products/kibana): An open-source analytics and visualization platform designed to work with {{es}} and {{elastic-sec}}. {{kib}} allows you to search, view, analyze and visualize data stored in {{es}} indices.


### {{elastic-endpoint}} self-protection [self-protection] 

For information about {{elastic-endpoint}}'s tamper-protection features, refer to [{{elastic-endpoint}} self-protection](security/manage-elastic-defend/elastic-endpoint-self-protection-features.md).


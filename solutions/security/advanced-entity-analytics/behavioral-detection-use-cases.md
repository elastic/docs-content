---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/behavioral-detection-use-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-behavioral-detection-use-cases.html
---

# Behavioral detection use cases

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/behavioral-detection-use-cases.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-behavioral-detection-use-cases.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$ml-integrations$$$

$$$security-behavioral-detection-use-cases-elastic-integrations-for-behavioral-detection-use-cases$$$

Behavioral detection identifies potential internal and external threats based on user and host activity. It uses a threat-centric approach to flag suspicious activity by analyzing patterns, anomalies, and context enrichment.

The behavioral detection feature is built on {{elastic-sec}}'s foundational SIEM detection capabilities, leveraging {{ml}} algorithms to enable proactive threat detection and hunting.


## Elastic {{integrations}} for behavioral detection use cases [ml-integrations]

Behavioral detection integrations provide a convenient way to enable behavioral detection capabilities. They streamline the deployment of components that implement behavioral detection, such as data ingestion, transforms, rules, {{ml}} jobs, and scripts.

::::{admonition} Requirements
* Behavioral detection integrations require a [Platinum subscription](https://www.elastic.co/pricing) or higher.
* To learn more about the requirements for using {{ml}} jobs, refer to [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md).

::::


Here’s a list of integrations for various behavioral detection use cases:

* [Data Exfiltration Detection](https://docs.elastic.co/en/integrations/ded)
* [Domain Generation Algorithm Detection](https://docs.elastic.co/en/integrations/dga)
* [Lateral Movement Detection](https://docs.elastic.co/en/integrations/lmd)
* [Living off the Land Attack Detection](https://docs.elastic.co/en/integrations/problemchild)
* [Network Beaconing Identification](https://docs.elastic.co/en/integrations/beaconing)

To learn more about {{ml}} jobs enabled by these integrations, refer to the [Prebuilt jobs page](https://www.elastic.co/guide/en/security/current/prebuilt-ml-jobs.html).


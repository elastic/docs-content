---
navigation_title: Security projects
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/security-billing.html
applies_to:
  serverless:
    security: ga
products:
  - id: cloud-serverless
sub:
  offering: Security Analytics
  abb-preamble: |
    Elastic Agent Builder enables you to create AI agents that assist with security operations, including alert investigation, threat triage, root cause analysis, and guided response actions. Agent Builder Executions is a billing dimension for Elastic Security Serverless projects on the Security Analytics Complete tier and the Elastic AI SOC Engine (EASE) tier.

    Billing is based on the number of agent executions completed in your project over the course of a month.
  abb-free-executions: 10,000
  pricing-label: Elastic Cloud pricing table
  pricing-url: https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=security
  wfe-preamble: Workflows enable you to automate multi-step processes across your security operations, including alert triage, case management, enrichment, and response actions. Workflow Executions is a billing dimension for Security Serverless projects on the Security Analytics Complete tier and the Elastic AI SOC Engine (EASE) tier.
  wfe-billing-detail: Billing is based on the number of workflow executions completed successfully in your project over the course of a month. Each execution represents one end-to-end run of a workflow. Failed executions are not billed.
  wfe-free-executions: 10,000

---

# {{elastic-sec}} Serverless billing dimensions [security-billing]

[{{elastic-sec}}](/solutions/security.md) serverless projects provide you with all the capabilities of {{elastic-sec}} to perform SIEM, security analytics, endpoint security, and cloud security workflows. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption based. Security Analytics/SIEM is available in two tiers of carefully selected features to enable common security operations:

* **Security Analytics Essentials** — Includes everything you need to operationalize traditional SIEM in most organizations.
* **Security Analytics Complete** — Adds advanced security analytics and AI-driven features that many organizations will require when upgrading or replacing legacy SIEM systems.

Projects that complement a third-party SIEM can use the Elastic AI SOC Engine (EASE) tier instead, which provides AI-powered threat hunting and alert triage capabilities.

Your bill is made up of [project charges](#security-billing-project-charges), [organization charges](#security-billing-organization-charges), and [add-ons](#security-billing-add-ons).

Refer to [](serverless-project-billing-dimensions.md) and the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=security) for more details, or [create a Serverless estimate](https://cloud.elastic.co/pricing/serverless?s=security).

## Project charges [security-billing-project-charges]

Project charges are based on the capabilities you use in your {{sec-serverless}} project, starting with [data volume](#security-billing-data-volume), which also covers [Endpoint Protection](#security-billing-endpoint-protection). Some features also have dedicated billing dimensions, such as [Cloud Protection](#security-billing-cloud-protection), and others are priced differently depending on the project type, such as [Agent Builder](#security-billing-agent-builder-executions) and [{{cps}}](#security-billing-cps). Some of these charges apply only in the [feature tiers](/deploy-manage/deploy/elastic-cloud/project-settings.md) where the related feature is available.

### Data volume [security-billing-data-volume]

Data volume charges have these components:

* **Ingest** — Measured by the number of GB of log/event/info data that you send to your Security project over the course of a month.
* **Retention** — Measured by the total amount of ingested data stored in your Security project.

Volume tier reductions apply at higher usage levels. Each tier's rate applies only to the data in its range.

Volume tier usage resets at the start of each month. As a result, the same usage can cost more at the start of a month than at the end of the previous one. Refer to the [{{pricing-label}}]({{pricing-url}}) for specific rates and tier breakpoints.


:::{include} _snippets/note-data-volumes-ingest-retention.md
:::

### Endpoint Protection [security-billing-endpoint-protection]

**Tiers:** Security Analytics Essentials, Security Analytics Complete

Endpoint Protection is included with Security Analytics with no per-endpoint licensing fees, providing endpoint protection and threat prevention for all your endpoints. Endpoint Protection is available in two tiers of selected features to enable common endpoint security operations:

* **Endpoint Protection Essentials** — Includes robust protection against malware, ransomware, and other malicious behaviors.
* **Endpoint Protection Complete** — Adds endpoint response actions and advanced policy management.

Endpoint Protection is built into all Security Analytics projects without additional per-endpoint license cost. You only pay for the alerts and telemetry generated by your endpoints, billed using the **Ingest** and **Retention** rates. You can customize telemetry collection in your endpoint policy to precisely control your data volume.

### Cloud Protection [security-billing-cloud-protection]

**Tiers:** Security Analytics Essentials, Security Analytics Complete

Cloud Protection is an *optional* add-on to Security Analytics that provides value-added protection capabilities for cloud assets. Cloud Protection is available in two tiers of carefully selected features to enable common cloud security operations:

* **Cloud Protection Essentials** — Protects your cloud workloads, continuously tracks posture of your cloud assets, and helps you manage risks by detecting configuration issues per CIS benchmarks.
* **Cloud Protection Complete** — Adds response capabilities.

Your total cost depends on the number of protected cloud workloads and other billable cloud assets you configure for use with {{ecloud}} Security. Volume tier reductions apply at higher usage levels. Each tier's rate applies only to the assets in its range.

Volume tier usage resets at the start of each month. As a result, the same usage can cost more at the start of a month than at the end of the previous one.

For [CSPM](../../../solutions/security/cloud/cloud-security-posture-management.md), billing is based on how many billable resources (`resource.id` s) you monitor. The following types of assets are considered billable:

* VMs:

    * **AWS:** EC2 instances
    * **Azure:** Virtual machines
    * **GCP:** Compute engine instances

* Storage resources:

    * **AWS:** S3, S3 Glacier, EBS
    * **Azure:** Archive, Blob, Managed disk
    * **GCP:** Cloud storage, Persistent disk, Coldline storage

* SQL databases and servers:

    * **AWS:** RDS, DynamoDB, Redshift
    * **Azure:** SQL database, Cosmos DB, Synapse Analytics
    * **GCP:** Cloud SQL, Firestore, BigQuery


For [KSPM](../../../solutions/security/cloud/kubernetes-security-posture-management.md), billing is based on how many Kubernetes nodes (`agent.id` s) you monitor.

For [CNVM](../../../solutions/security/cloud/cloud-native-vulnerability-management.md), billing is based on how many cloud assets (`cloud.instance.id` s) you monitor.

Logs, events, alerts, and configuration data ingested into your security project are billed using the **Ingest** and **Retention** pricing described above.

For more details about {{elastic-sec}} serverless project rates and billable assets, refer to Cloud Protection in the [{{ecloud}} pricing table](https://cloud.elastic.co/cloud-pricing-table?productType=serverless&project=security).

### Agent Builder executions [security-billing-agent-builder-executions]

**Tiers:** Security Analytics Complete, EASE

:::{include} _snippets/agent-builder-executions-billing.md
:::

### {{cps-cap}} [security-billing-cps]

**Tiers:** Security Analytics Complete

[{{cps-cap}}](/deploy-manage/cross-project-search-config.md) enables you to search across multiple {{serverless-short}} projects from a single origin project.

:::{include} /deploy-manage/_snippets/cps-billing.md
:::

## Organization charges [security-billing-organization-charges]

These charges apply regardless of which project type you use, and include data out and support.

:::{include} _snippets/serverless-organization-charges.md
:::

## Add-ons [security-billing-add-ons]

Add-ons are capabilities that are available across your {{serverless-short}} projects. They're billed based on usage, in addition to the other billing dimensions of your project. Some add-ons apply only in the [feature tiers](/deploy-manage/deploy/elastic-cloud/project-settings.md) where the related feature is available.

### Workflow executions [security-billing-workflow-executions]

**Tiers:** Security Analytics Complete, EASE

:::{include} _snippets/workflow-executions-billing.md
:::

### Elastic {{infer-cap}} Service [security-billing-elastic-managed-llms]

:::{include} _snippets/eis-billing.md
:::

[Elastic Managed LLMs](kibana://reference/connectors-kibana/elastic-managed-llm.md) enable you to use AI-powered features without deploying a model in your project. The models are configured by default to use with Agent Builder, Attack Discovery, and other applicable AI features as a part of the Security Analytics Complete and Elastic AI SOC Engine feature tiers.

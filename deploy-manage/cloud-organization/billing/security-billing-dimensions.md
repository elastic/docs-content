---
navigation_title: Security projects
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/security-billing.html
applies_to:
  serverless: all
products:
  - id: cloud-serverless
---

# {{elastic-sec}} billing dimensions [security-billing]

{{elastic-sec}} serverless projects provide you with all the capabilities of {{elastic-sec}} to perform SIEM, security analytics, endpoint security, and cloud security workflows. Projects are provided using a Software as a Service (SaaS) model, and pricing is entirely consumption based. Security Analytics/SIEM is available in two tiers of carefully selected features to enable common security operations:

* **Security Analytics Essentials** — Includes everything you need to operationalize traditional SIEM in most organizations.
* **Security Analytics Complete** — Adds advanced security analytics and AI-driven features that many organizations will require when upgrading or replacing legacy SIEM systems.

Your monthly bill is based on the capabilities you use. When you use Security Analytics/SIEM, your bill is calculated based on data volume, which has these components:

* **Ingest** — Measured by the number of GB of log/event/info data that you send to your Security project over the course of a month.
* **Retention** — Measured by the total amount of ingested data stored in your Security project.

Data volumes for ingest and retention are based on the fully enriched normalized data size at the end of the ingest pipeline, before {{es}} compression is performed, and will be higher than the volumes traditionally reported by {{es}} index size. In addition, these volumes might be larger than those reported by cloud provider proxy logs for data going into {{es}}. This allows you to have flexibility in choosing your preferred ingest architecture for enrichment, whether it’s through {{agent}}, {{ls}}, OpenTelemetry, or collectors — with no impact on the cost.


## Endpoint Protection [security-billing-endpoint-protection]

Endpoint Protection is an *optional* add-on to Security Analytics that provides endpoint protection and threat prevention. Endpoint Protection is available in two tiers of selected features to enable common endpoint security operations:

* **Endpoint Protection Essentials** — Includes robust protection against malware, ransomware, and other malicious behaviors.
* **Endpoint Protection Complete** — Adds endpoint response actions and advanced policy management.

You pay based on the number of protected endpoints configured with the {{elastic-defend}} integration. Logs, events, and alerts from these endpoints are billed using the **Ingest** and **Retention** pricing. If you're using {{elastic-defend}} solely for data collection (without Endpoint Essentials or Complete add-ons), endpoints do not count towards billing. In this case, you're only billed for data ingestion and retention, and you can configure event collection and telemetry in the policy without enabling protections. 

## Cloud Protection [security-billing-cloud-protection]

Cloud Protection is an *optional* add-on to Security Analytics that provides value-added protection capabilities for cloud assets. Cloud Protection is available in two tiers of carefully selected features to enable common cloud security operations:

* **Cloud Protection Essentials** — Protects your cloud workloads, continuously tracks posture of your cloud assets, and helps you manage risks by detecting configuration issues per CIS benchmarks.
* **Cloud Protection Complete** — Adds response capabilities.

Your total cost depends on the number of protected cloud workloads and other billable cloud assets you configure for use with {{ecloud}} Security.

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


## Elastic Managed LLM

The default [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) enables you to leverage AI-powered search as a service without deploying a model in your serverless project. It's configured by default to use with the Security AI Assistant, Attack Discovery, and other applicable AI features as a part of the "Security Analytics Complete" feature tier. Using the default LLM will use tokens and incur related token-based add-on billing for your serverless project.
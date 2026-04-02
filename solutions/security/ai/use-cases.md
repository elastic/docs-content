---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/assistant-use-cases.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-use-cases.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# AI use cases

The guides in this section describe example workflows for AI Assistant and Attack discovery. Refer to them for examples of each tool’s individual capabilities and how they can work together.

* [Triage alerts](/solutions/security/ai/triage-alerts.md)
* [Identify, investigate, and document threats](/solutions/security/ai/identify-investigate-document-threats.md)
* [Generate, customize, and learn about {{esql}} queries](/solutions/security/ai/generate-customize-learn-about-esorql-queries.md)

For general information, refer to [AI Assistant](/solutions/security/ai/ai-assistant.md) or [Attack discovery](/solutions/security/ai/attack-discovery.md).

## Other AI-powered tools

In addition to AI Assistant and Attack Discovery, {{elastic-sec}} provides several other AI-powered tools for specific use cases. These include:

* [Automatic Import](/solutions/security/get-started/automatic-import.md): Helps you quickly parse, ingest, and create [ECS mappings](https://www.elastic.co/elasticsearch/common-schema) for data from sources that don’t yet have prebuilt Elastic integrations. This can accelerate your migration to {{elastic-sec}}, and help you quickly add new data sources to an existing SIEM solution in {{elastic-sec}}.
* [Automatic Migration](/solutions/security/get-started/automatic-migration.md): Helps you quickly convert SIEM rules from the Splunk Processing Language (SPL) to the Elasticsearch Query Language ({{esql}}). If comparable Elastic-authored rules exist, it simplifies onboarding by mapping your rules to them. Otherwise, it creates custom rules on the fly so you can verify and edit them instead of writing them from scratch.
* [Automatic Troubleshooting](/solutions/security/manage-elastic-defend/automatic-troubleshooting.md): Helps you quickly check whether your endpoints have third-party AV software installed by analyzing file event logs from your hosts to determine whether antivirus software is present. From there, you can address any incompatibilities to make sure your endpoints are protected.

  {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` Helps you detect any issues in {{elastic-defend}} integration policies and suggests remediation steps.



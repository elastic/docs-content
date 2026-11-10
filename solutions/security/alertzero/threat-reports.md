---
navigation_title: Threat reports
description: "How AlertZero builds the threat reports that Continuous Threat Hunt searches for, including the supported threat feeds and the requirements for building reports."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# How {{alertzero}} builds {{az-threat-reports}}

A {{az-threat-report}} is an article about threat activity from a public threat feed, along with the details {{alertzero}} extracts from it, such as indicators of compromise (IOCs). The {{az-continuous-threat-hunt}} {{az-worker}} searches your data for activity that matches each report. {{alertzero}} builds the reports for you, so you don't need to set up the feeds yourself.

## How it works [alertzero-threat-reports]

When you turn on {{az-continuous-threat-hunt}}, {{alertzero}} turns on three threat intelligence supply workflows. **Ingest threat feeds** and **Enrich threat report** each run every 4 hours in the default space. **Attribute alerts to reports** runs every hour in the current space.

**Enrich threat report** works on the reports that **Ingest threat feeds** saves:

1. **Ingest threat feeds** collects new articles from the [supported threat feeds](#alertzero-threat-feeds) and saves each one as a {{az-threat-report}}. It skips articles more than 30 days old and articles it already collected in the last 90 days.
2. **Enrich threat report** checks that each report contains threat intelligence, then extracts details such as IOCs, attacker behaviors, and severity. {{az-continuous-threat-hunt}} ignores reports that fail the check. For the full list of details, refer to [](#alertzero-threat-report-contents).

**Attribute alerts to reports** counts the alerts that match each report.

:::{tip}
After you first turn on {{az-continuous-threat-hunt}}, **Enrich threat report** might need several runs to process all the collected reports. It processes up to 50 reports per run, oldest first. Until then, {{az-continuous-threat-hunt}} hunts with only the reports processed so far.
:::

## What a threat report contains [alertzero-threat-report-contents]

For each {{az-threat-report}} that contains threat intelligence, **Enrich threat report** adds the following details:

* IOCs, including file hashes, IP addresses and ranges, domains, URLs, email addresses, and cryptocurrency wallet addresses.
* A classification of the threat, including its categories, attacker behaviors, affected regions, and severity.
* A description of the adversary, including their capabilities, infrastructure, and victims, if the report has enough detail.
* Links to other reports that share its IOCs.

## Supported threat feeds [alertzero-threat-feeds]

**Ingest threat feeds** checks these public feeds for new articles. You can't add your own feeds. The list is fixed. To reach the feeds, {{kib}} needs outbound HTTPS access to each feed's domain. {{kib}} connects to the feeds directly, not through a proxy.

| Feed | Publisher | Domain |
| --- | --- | --- |
| Elastic Security Labs | Elastic | `www.elastic.co` |
| CISA Alerts and Advisories | U.S. Cybersecurity and Infrastructure Security Agency (CISA) | `www.cisa.gov` |
| UK National Cyber Security Centre | UK National Cyber Security Centre (NCSC) | `www.ncsc.gov.uk` |
| CERT-FR Security Alerts | French national CERT (CERT-FR) | `cert.cyber.gouv.fr` |
| CERT-FR Threats and Incidents | CERT-FR | `cert.cyber.gouv.fr` |
| CERT-EU Security Advisories | CERT for the EU institutions (CERT-EU) | `cert.europa.eu` |
| CERT-EU Threat Intelligence | CERT-EU | `cert.europa.eu` |

## How the threat intelligence workflows apply to spaces [alertzero-threat-reports-spaces]

If you use {{alertzero}} in more than one space, your spaces share some threat intelligence workflows, and others run separately in each space:

* All spaces share **Ingest threat feeds** and **Enrich threat report**. Every space gets the same reports, and turning either workflow on or off affects every space. {{alertzero}} turns them off only after {{az-continuous-threat-hunt}} is off in every space.
* **Attribute alerts to reports** runs separately in each space. It counts only that space's alerts, and it turns off when you turn off {{az-continuous-threat-hunt}} in that space.

## What {{alertzero}} needs to build {{az-threat-reports}} [alertzero-threat-reports-requirements]

To build reports for {{az-continuous-threat-hunt}}, the threat intelligence workflows need network access to the threat feeds and models to process reports. {{alertzero}} also stores the reports with embeddings from your cluster's [default embedding endpoint](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-setup-configuration.md#default-endpoints). If that endpoint isn't available, you can't turn on {{az-continuous-threat-hunt}}.

**Enrich threat report** runs in the default space, so it uses the default space's model settings for every report, even if you hunt in another space. It makes model calls for every new report.

| Workflow | Requirement | Effect if missing |
| --- | --- | --- |
| Ingest threat feeds | Outbound HTTPS access from {{kib}} to the domain of each [supported threat feed](#alertzero-threat-feeds). | The workflow runs, but it collects no reports from the feeds it can't reach. |
| Enrich threat report | Reports from **Ingest threat feeds**. | It has nothing to process, so {{az-continuous-threat-hunt}} has no reports to search for. |
| Enrich threat report | Models for the **{{az-efficient-models}}** and **{{az-frontier-models}}** settings, configured in [**Feature Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings) in the default space. | The workflow can't process reports, so {{az-continuous-threat-hunt}} has no reports to search for. The workflow retries unprocessed reports on its next run. |

## Related pages [alertzero-threat-reports-related]

* [](watches-and-workers.md#alertzero-continuous-threat-hunt)
* [](configure-worker-settings.md#configure-worker-settings-continuous-threat-hunt)
* [](act-on-hunt-finding.md)

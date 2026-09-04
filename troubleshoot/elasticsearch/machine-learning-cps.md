---
navigation_title: CPS {{ml}} {{dfeeds}}
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot cross-project search {{dfeeds}} [cps-ml-datafeed-troubleshooting]

Anomaly detection {{dfeeds}} on {{serverless-full}} can search data across linked projects when {{cps}} is configured. These topics help you diagnose and resolve problems with project scope (`project_routing`), internal cloud credentials, linked-project availability, and field mappings.

Before you troubleshoot, confirm that projects are linked and that users have access. See [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md) and the [{{cps-cap}} overview](/explore-analyze/cross-project-search.md).

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Where to find diagnostics [cps-ml-diagnostics]

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

## Find your issue [cps-ml-symptom-routing]

Start with the symptom that best matches what you see:

| Symptom | Start here | Notes |
| --- | --- | --- |
| The {{dfeed}} returns no results | [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) | — |
| Results come only from the origin project | [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) | If `project_routing` is `_alias:_origin` or the job has no stored routing, this is expected legacy behavior.<br><br>If `authorization.cloud_api_key.id` is missing or job messages report a cleared or never-minted key, refer to [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) instead. |
| Extraction cycles are suddenly slower after you linked projects | [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) | — |
| The {{dfeed}} keeps failing with extraction errors | [Linked project unavailable](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-linked-project-unavailable.md) | Use this page when job messages report a skipped linked project. For authorization failures, refer to [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md). For field type conflicts, refer to [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md). |
| {{es}} or {{kib}} rejected a project scope change | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) | — |
| Some jobs failed during a bulk **Change project scope** update | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) | — |
| Anomaly scores spiked after a scope change | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) | — |
| A field is missing, a project is excluded from a run, or mappings conflict across projects | [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md) | — |
| Authorization errors after the {{dfeed}} had been working | [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) | — |

## Find an error message [cps-ml-message-index]

If you already have an error or audit string from **Job messages**, the API, or {{kib}}, use this index:

% TODO: point the CPS migration row at ml-ad-run-jobs.md#ml-ad-cps-legacy when PR #7814 merges

| Message (substring match) | Page |
| --- | --- |
| `matched no linked project` / `cannot search any project` | [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) |
| `remote clusters out of` / `were skipped when performing datafeed search` | [Linked project unavailable](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-linked-project-unavailable.md) |
| `Cannot update project_routing` / `while its status is started` | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) |
| `Rollback model snapshot` retained before `project_routing` scope change | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) |
| `CPS migration: project_routing defaulted` | [](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) |
| `Datafeed search scope changed` / `Elevated anomaly scores detected after search scope change` | [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md) |
| `Internal cloud API key` / `Datafeed search probe failed` / `User lacks the required permissions` | [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) |
| `Failed to revoke internal cloud API key` | [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) |
| `Cross-project field conflict` / `conflicting types across projects` / `excluded project` from this run | [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md) |
| `Cannot run datafeed` + `required time field` | [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md) |
| `Datafeed has recovered data extraction` / `started retrieving data again` | [Linked project unavailable](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-linked-project-unavailable.md) |

## `project_routing` syntax [cps-ml-routing-reference]

For valid `project_routing` values and wildcard rules, refer to [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

## Related pages [cps-ml-related]

* [](/explore-analyze/cross-project-search.md)
* [](/explore-analyze/cross-project-search/cross-project-search-project-routing.md)
* [](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md)

## When to contact support [cps-ml-contact-support]

Contact [Elastic support](/troubleshoot/index.md#contact-us) when:

* A linked project or region appears unavailable across multiple jobs and you have confirmed project linking in Elastic Cloud.
* The same {{dfeed}} fails repeatedly after you apply the fixes in these topics.
* The origin project reports memory pressure or out-of-memory errors while CPS {{dfeeds}} are running, and narrowing `project_routing` does not relieve the symptoms.

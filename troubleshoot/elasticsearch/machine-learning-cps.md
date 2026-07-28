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

Anomaly detection {{dfeeds}} on {{serverless-full}} can search data across linked projects when {{cps}} is configured. These topics help you diagnose and resolve problems with **Project scope** (`project_routing`), internal cloud credentials, linked-project availability, and field mappings.

Before you troubleshoot, confirm that projects are linked and that users have access. See [Link and manage projects](/deploy-manage/cross-project-search-config/cps-config-link-and-manage.md) and the [{{cps-cap}} overview](/explore-analyze/cross-project-search.md).

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Where to find diagnostics [cps-ml-diagnostics]

:::{include} /troubleshoot/_snippets/cps-ml-diagnostics-sources.md
:::

## Find your issue [cps-ml-symptom-routing]

Start with the symptom that best matches what you see:

* **The {{dfeed}} returns no results**: [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md)
* **Results come only from the origin project**: [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md) when `project_routing` is `_alias:_origin` or the job has no stored routing (legacy default). When `authorization.cloud_api_key.id` is missing from `GET _ml/datafeeds/{datafeed_id}` or **Job messages** report `Internal cloud API key cleared on datafeed update with non-cloud credentials` or lack `Internal cloud API key minted for cross-project datafeed`, start with [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) instead
* **Extraction cycles are suddenly slower after you linked projects**: [Project scope problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-project-scope.md)
* **The {{dfeed}} keeps failing with extraction errors**: [Linked project unavailable](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-linked-project-unavailable.md) when **Job messages** report a skipped linked project. For authorization failures or field type conflicts, start with [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md) or [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md) instead.
* **{{es}} or {{kib}} rejected a project scope change**: [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md)
* **Some jobs failed during a bulk Change project scope update**: [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md)
* **Anomaly scores spiked after a scope change**: [Project scope changes](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-change.md)
* **A field is missing, a project is excluded from a run, or mappings conflict across projects**: [Field mapping conflicts](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mappings.md)
* **Authorization errors after the {{dfeed}} had been working**: [Cloud credential problems](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-credentials.md)

## `project_routing` quick reference [cps-ml-routing-reference]

Every valid `project_routing` value starts with `_alias:`. Bare `_origin` is **not** a routing value.

| `project_routing` value | Effective search scope |
| --- | --- |
| Empty or omitted (`null`) | **Flat world**: searches the origin project and all linked projects |
| `_alias:_origin` | **Origin only**: searches the origin project |
| `_alias:*` | **Same as flat world**: equivalent to an empty or omitted value. Searches the origin project and all linked projects |
| `_alias:production-*` (prefix wildcard) | **Subset**: linked projects whose alias starts with `production-`, plus the origin project when its alias matches |
| `_alias:*-prod` (suffix wildcard) | **Subset**: linked projects whose alias ends with `-prod`, plus the origin project when its alias matches |
| `_alias:*staging*` (contains wildcard) | **Subset**: linked projects whose alias contains `staging`, plus the origin project when its alias matches |
| `_alias:production-us` (exact alias) | **Single linked project**: only the named alias, plus the origin project when its alias matches |

Prefix, suffix, and contains wildcards are supported. Internal wildcards (for example `_alias:prod*eu`) and multiple sequential wildcards are not.

**Index qualifier, not routing.** In `indices`, prefix a pattern with `_origin:` to target the origin project (for example `_origin:logs-*`). That qualifier is separate from `project_routing`.

For syntax details and examples, refer to [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

## Related pages [cps-ml-related]

* [{{cps-cap}}](/explore-analyze/cross-project-search.md): Overview of cross-project search concepts and prerequisites.
* [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md): How to limit CPS queries to specific linked projects.
* [Run a job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md): Create, start, and manage anomaly detection jobs and {{dfeeds}}.

## When to contact support [cps-ml-contact-support]

Contact [Elastic support](/troubleshoot/index.md#contact-us) when:

* A linked project or region appears unavailable across multiple jobs and you have confirmed project linking in Elastic Cloud.
* The same {{dfeed}} fails repeatedly after you apply the fixes in these topics.
* The origin project reports memory pressure or out-of-memory errors while CPS {{dfeeds}} are running, and narrowing `project_routing` does not relieve the symptoms.

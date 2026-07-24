---
navigation_title: Machine learning
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Troubleshoot {{ml}} with {{cps-init}} [ml-cps-troubleshooting]

Use this section to diagnose and resolve common problems with anomaly detection {{dfeeds}} that search across linked projects on {{serverless-full}}. These topics apply when CPS-enabled ML {{dfeeds}} are available for your project.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Where to find diagnostics

Gather context from the following sources before narrowing down a CPS datafeed issue:

* **ML job Messages in {{kib}}** — Open **Machine Learning → Anomaly Detection**, select the job, and review the **Messages** tab for audit entries and warnings about linked projects, credentials, or scope changes.
* **`.ml-notifications-*` and `.ml-annotations-*` indices** — Search these indices for the job or datafeed ID to find historical audit messages and scope-change annotations.
* **`GET _ml/datafeeds/{id}/_stats`** — Inspect `remote_cluster_stats` for per-project availability, skip counts, and cross-project search health over recent extraction cycles.
* **`GET _ml/datafeeds/{id}`** — Confirm the effective `project_routing` expression and whether the datafeed uses qualified index references.

## Common issues

* [Linked project skipped or unavailable](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-linked-project-skipped.md)
* [Search scope changed](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-search-scope-changed.md)
* [`project_routing` matches no project](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-routing-no-match.md)
* [Stale project reference](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-stale-project-reference.md)
* [Cloud token mint failure](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-cloud-token-mint-failure.md)
* [Cloud token runtime failure](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-cloud-token-runtime-failure.md)
* [Field mapping mismatch across projects](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-field-mapping-mismatch.md)
* [Schema drift in a linked project](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-schema-drift.md)
* [Search scope too broad](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-scope-too-broad.md)
* [Bulk migration partial failure](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-bulk-migration-partial.md)
* [Clone inherits unintended `project_routing`](/troubleshoot/elasticsearch/machine-learning/cps-datafeed-clone-project-routing.md)

## `project_routing` quick reference

| `project_routing` value | Effective search scope |
| --- | --- |
| Empty or omitted (`null`) | **Flat world** — searches the origin project and all linked projects |
| `_origin` or `_alias:_origin` | **Local only** — searches the origin project |
| `_alias:prod-*` (or other tag expression) | **Subset** — searches only linked projects whose tags match the expression |
| Qualified index (`project:index`) | **Specific project** — searches the named project and index |

For syntax details and examples, refer to [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

## Related pages

* [{{cps-cap}}](/explore-analyze/cross-project-search.md) — Overview of cross-project search concepts and prerequisites.
* [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md) — How to limit CPS queries to specific linked projects.
* [Run a job](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md) — Create, start, and manage anomaly detection jobs and {{dfeeds}}.

## When to contact support

Contact [Elastic support](/troubleshoot/index.md#contact-us) when:

* A linked project or region appears unavailable across multiple jobs and you have confirmed project linking in Elastic Cloud.
* The same datafeed fails repeatedly after you apply the fixes in these topics.
* The origin project reports memory pressure or out-of-memory errors while CPS datafeeds are running, and narrowing `project_routing` does not relieve the symptoms.

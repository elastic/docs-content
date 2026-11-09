---
navigation_title: Search performance
description: Understand what affects search performance in Observability serverless projects, how to recognize saturated search capacity, and how to reduce load.
applies_to:
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
type: overview
---

# Understand search capacity and alerting performance

% TODO: "Most recent day" is still unverified for Observability projects. It lives in the Elastic Cloud serverless configuration, not in the Kibana or docs repos. Confirm with the serverless team before merging.

In {{obs-serverless}} projects, alerting rules can fail or time out, and dashboards can slow down, when too many searches run at once. This applies to rules in both [{{alerting-v1-system}}](/explore-analyze/alerting/alerts.md) and [{{alerting-v2-system}}](/explore-analyze/alerting/esql/system-overview.md), because both systems use the same search capacity.

{{ecloud}} sizes your project's search capacity to its volume of search-ready data, which includes data from the most recent day. Capacity doesn't scale up when query load increases. Searches on recent data are fastest. Older data stays searchable, but queries on it are slower and use more capacity. Ingest runs separately and doesn't compete with search. To learn what counts as search-ready data, refer to [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

## What uses search capacity [obs-search-capacity-load]

Everything that queries your project shares the same search capacity, including alerting rules, service-level objectives (SLOs), dashboards, Discover, {{esql}} queries, and external clients. These add the most load:

* **Many rules, or rules that run often:** Every rule run searches your data, so load grows with the number of rules and how often they run.
* **Searches over more than the most recent day:** Rules with long time windows, and dashboards or Discover sessions with wide time ranges, read older data from general storage. For example, [SLO burn rate rules](/solutions/observability/incident-management/create-an-slo-burn-rate-rule.md) in {{alerting-v1-system}} check windows of up to 72 hours by default. In {{alerting-v2-system}}, each rule searches its [lookback window](/explore-analyze/alerting/esql/rules/configure-rule-schedule.md), or a time range as long as its schedule if you don't set one.
* **SLOs:** Each SLO continuously queries its source data to keep its status current. By default, a new SLO also backfills up to the last 7 days of data when you create it.

## Recognize saturated search capacity [obs-search-capacity-signs]

Signs that your project is running out of search capacity include:

* Failed rule runs. For {{alerting-v1-system}} rules, look for a **Last response** of `failed` in the rules list, or failed runs on the rule's [**Execution history** tab](/solutions/observability/incident-management/create-manage-rules.md#observability-create-manage-rules-view-rule-details). For {{alerting-v2-system}} rules, look for a **Response** of **Failure** on the [**Execution history** page](/explore-analyze/alerting/esql/rules/review-rule-execution-history.md).
* `Request timed out` errors in {{kib}}.
* Circuit breaker exceptions.
* Slower queries in Discover and on dashboards.

## Reduce search load [obs-search-capacity-reduce]

To reduce load:

* Turn off rules you don't need.
* Stagger rule schedules so fewer rules run at the same time.
* Shorten rule time windows and lookbacks where your detection needs allow.
* Narrow the time range on dashboards and in Discover.
* When you create an SLO and don't need its history, select **Prevent initial backfill of data** in **Advanced settings**. The SLO then starts from the time you create it.

If you need more search capacity, or want more than the most recent day of data to be search-ready, contact Elastic Support.

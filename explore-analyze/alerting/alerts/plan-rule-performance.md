---
navigation_title: Plan for rule performance
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Learn how Kibana Classic Alerting rules use search capacity, which rule settings add the most load, and how to keep rules running on time.
---

# Plan {{alerting-v1-system}} rules for search performance [plan-rule-performance]

Every {{alerting-v1-system}} rule run searches your data. When too many searches run at once, rules slow down or time out, and a rule that times out discards the alerts and actions from that run. Plan rule schedules and time windows with search load in mind, especially before you create many rules.

For {{alerting-v2-system}} rules, refer to [](/explore-analyze/alerting/esql/rules/plan-rule-performance.md).

## How search capacity works [classic-rule-performance-search-capacity]

Rules share search capacity with everything else that queries your project or deployment, including dashboards, Discover, {{esql}} queries, and external clients. Your deployment type determines how much search capacity you have and how you add more.

::::{applies-switch}

:::{applies-item} { "serverless": { "observability": "ga", "security": "ga" } }
% TODO: "Most recent day" is still unverified for Observability and Security projects. It lives in the Elastic Cloud serverless configuration, not in the Kibana or docs repos. Confirm with the serverless team before merging.

{{ecloud}} sizes your project's search capacity to its volume of search-ready data, which includes data from the most recent day. Capacity doesn't scale up when query load increases. Searches on recent data are fastest. Older data stays searchable, but queries on it are slower and use more capacity. Ingest runs separately and doesn't compete with search. To learn what counts as search-ready data, refer to [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

If you need more search capacity, or want more than the most recent day of data to be search-ready, contact Elastic Support.
:::

:::{applies-item} { "serverless": { "elasticsearch": "ga" } }
Your project's [Search Power](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-power-settings) setting controls how many search resources it keeps ready and how far it can scale under load. The [Search Boost Window](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-search-boost-window) setting controls how much time series data is search-ready. Rules that search data outside the boost window are slower and use more capacity.
:::

:::{applies-item} stack: ga
Search capacity depends on the size and number of {{es}} nodes in your deployment. Searches are fastest on the hot tier, which holds your most recent data. Searches on the frozen tier are typically slower, because {{es}} must sometimes fetch that data from a snapshot repository. To learn more, refer to [Data tiers](/manage-data/lifecycle/data-tiers.md).

On {{ech}}, {{ece}}, and {{eck}}, [autoscaling](/deploy-manage/autoscaling.md) adds capacity based on storage and machine learning needs, not query load. To add search capacity, add or resize {{es}} nodes in the tiers that your rules search.

Rules also run as {{kib}} tasks, and each {{kib}} instance runs a limited number of tasks at the same time. If rules run late while {{es}} isn't under load, add {{kib}} instances or tune Task Manager. To learn more, refer to [](/deploy-manage/production-guidance/kibana-alerting-production-considerations.md).
:::

::::

## What adds the most load [classic-rule-performance-load]

Rules add the most search load when:

* You run many rules, or run them often. Each rule searches your data on its **Rule schedule**.
* Rule conditions cover long time windows. Many rule types check a time window that you set in the rule conditions, and some set long windows by default. For example, [service-level objective (SLO) burn rate rules](/solutions/observability/incident-management/create-an-slo-burn-rate-rule.md) check windows of up to 72 hours.
* Rules search broad index patterns or group results by fields with many unique values.

Each rule run also has a time limit. On {{serverless-short}}, a rule run stops after 1 minute. On {{stack}}, it stops after 5 minutes by default, and administrators can change the limit with `xpack.alerting.rules.run.timeout`. By default, when a run stops early, {{kib}} discards its alerts and actions.

## Keep rules running on time [classic-rule-performance-best-practices]

To keep search load manageable:

* Turn off rules you don't need.
* Use longer schedules for conditions that don't need fast detection.
* Keep rule time windows as short as your detection needs allow.
* Target rules at the specific indices or data views they need, instead of broad patterns.

## Check whether rules have enough capacity [classic-rule-performance-monitor]

Signs that you're running out of search capacity include:

* Rules with a **Last response** of `failed`, or rule runs that time out. To check rule status and run history, refer to [](/explore-analyze/alerting/alerts/create-manage-rules.md).
* `Request timed out` errors in {{kib}}.
* Circuit breaker exceptions.
* Slower queries in Discover and on dashboards.

To find out why a specific rule failed, refer to [](/explore-analyze/alerting/alerts/alerting-troubleshooting.md).

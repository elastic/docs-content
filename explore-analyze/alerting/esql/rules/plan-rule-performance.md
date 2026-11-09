---
navigation_title: Plan for rule performance
applies_to:
  stack: ga 9.6+
  serverless:
    observability: ga
products:
  - id: kibana
  - id: cloud-serverless
description: Learn how Kibana Universal Alerting rules use search capacity, which schedule, lookback, and query choices add the most load, and how to keep rules running on time.
---

# Plan {{alerting-v2-system}} rules for search performance [plan-rule-performance]

Every {{alerting-v2-system}} rule run sends an {{esql}} query to {{es}}. When too many searches run at once, rule runs slow down or fail. Plan each rule's schedule, lookback window, and query with search load in mind, especially before you create many rules.

For {{alerting-v1-system}} rules, refer to [](/explore-analyze/alerting/alerts/plan-rule-performance.md).

## How search capacity works [universal-rule-performance-search-capacity]

Rules share search capacity with everything else that queries your project or deployment, including {{alerting-v1-system}} rules, dashboards, Discover, other {{esql}} queries, and external clients. Your deployment type determines how much search capacity you have and how you add more.

::::{applies-switch}

:::{applies-item} { "serverless": { "observability": "ga" } }
% TODO: "Most recent day" is still unverified for Observability projects. It lives in the Elastic Cloud serverless configuration, not in the Kibana or docs repos. Confirm with the serverless team before merging.

{{ecloud}} sizes your project's search capacity to its volume of search-ready data, which includes data from the most recent day. Capacity doesn't scale up when query load increases. Searches on recent data are fastest. Older data stays searchable, but queries on it are slower and use more capacity. Ingest runs separately and doesn't compete with search. To learn what counts as search-ready data, refer to [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

If you need more search capacity, or want more than the most recent day of data to be search-ready, contact Elastic Support.
:::

:::{applies-item} stack: ga 9.6+
Search capacity depends on the size and number of {{es}} nodes in your deployment. Searches are fastest on the hot tier, which holds your most recent data. Searches on the frozen tier are typically slower, because {{es}} must sometimes fetch that data from a snapshot repository. To learn more, refer to [Data tiers](/manage-data/lifecycle/data-tiers.md).

On {{ech}}, {{ece}}, and {{eck}}, [autoscaling](/deploy-manage/autoscaling.md) adds capacity based on storage and machine learning needs, not query load. To add search capacity, add or resize {{es}} nodes in the tiers that your rules search.

Rules also run as {{kib}} tasks, and each {{kib}} instance runs a limited number of tasks at the same time. If rules run late while {{es}} isn't under load, add {{kib}} instances. To learn more, refer to [](/deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md).
:::

::::

## What adds the most load [universal-rule-performance-load]

Rules add the most search load when:

* **The schedule is short:** Each rule runs its query on its **Schedule**. Short schedules on many rules multiply the number of searches.
* **The lookback window is long:** Each run searches the time range in the rule's **Lookback Window**. If you don't set one, the rule searches a time range as long as its schedule. Patterns that use a broad lookback on purpose, such as [no-data detection](/explore-analyze/alerting/esql/rules/esql-no-data-detection.md), search more data on every run.
* **The query is expensive:** Queries over broad index patterns, or that group results by fields with many unique values, take longer and use more capacity.
* **The rule runs extra queries:** A rule that uses a [recovery query](/explore-analyze/alerting/esql/rules/configure-rule-recovery.md) or [no-data handling](/explore-analyze/alerting/esql/rules/configure-no-data-handling.md) can run additional searches on each run while it has active alerts.

## Keep rules running on time [universal-rule-performance-best-practices]

To keep search load manageable:

* Turn off rules you don't need. To learn how, refer to [Disable or snooze a rule](/explore-analyze/alerting/esql/rules/view-manage-rules.md#disable-snooze-rule).
* Use longer schedules for conditions that don't need fast detection. For guidance, refer to [Schedule and lookback](/explore-analyze/alerting/esql/rules/configure-rule-schedule.md#schedule-when-to-use).
* Set a lookback window that covers the schedule without searching much further back.
* Query only the indices the rule needs, and filter early in the query.

## Check whether rules have enough capacity [universal-rule-performance-monitor]

Signs that you're running out of search capacity include:

* Rule runs with a **Response** of **Failure**, or a rising **Duration**, on the [**Execution history** page](/explore-analyze/alerting/esql/rules/review-rule-execution-history.md).
* `Request timed out` errors in {{kib}}.
* Circuit breaker exceptions.
* Slower queries in Discover and on dashboards.

---
navigation_title: Plan for rule performance
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Learn how detection rules use search capacity, which rule settings add the most load, and how to keep rules running on time in Elastic Security.
---

# Plan detection rules for search performance [plan-rule-performance]

Every detection rule run searches your data. When too many searches run at once, rules slow down, time out, or fail, and you can miss alerts. Plan rule schedules and lookback times with search load in mind, especially before you turn on many rules at once.

## How search capacity works [rule-performance-search-capacity]

Detection rules share search capacity with everything else that queries your project or deployment, including dashboards, Discover, {{esql}} queries, and external clients. Your deployment type determines how much search capacity you have and how you add more.

::::{applies-switch}

:::{applies-item} { "serverless": { "security": "ga" } }
% TODO: "Most recent day" is still unverified for Security projects. It lives in the Elastic Cloud serverless configuration, not in the Kibana or docs repos. Confirm with the serverless team before merging.

{{ecloud}} sizes your project's search capacity to its volume of search-ready data, which includes data from the most recent day. Capacity doesn't scale up when query load increases. Searches on recent data are fastest. Older data stays searchable, but queries on it are slower and use more capacity. Ingest runs separately and doesn't compete with search. To learn what counts as search-ready data, refer to [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

If you need more search capacity, or want more than the most recent day of data to be search-ready, contact Elastic Support.
:::

:::{applies-item} stack: ga
Search capacity depends on the size and number of {{es}} nodes in your deployment. Searches are fastest on the hot tier, which holds your most recent data. Searches on the frozen tier are typically slower, because {{es}} must sometimes fetch that data from a snapshot repository. To keep rules fast, keep data in the hot tier for at least 24 hours, and [exclude cold and frozen data](/solutions/security/detect-and-alert/set-rule-data-sources.md#exclude-cold-frozen-tier) from rules that don't need it.

On {{ech}}, {{ece}}, and {{eck}}, [autoscaling](/deploy-manage/autoscaling.md) adds capacity based on storage and machine learning needs, not query load. To add search capacity, add or resize {{es}} nodes in the tiers that your rules search.

Rules also run as {{kib}} tasks, and each {{kib}} instance runs a limited number of tasks at the same time. If rules run late or miss runs while {{es}} isn't under load, add {{kib}} instances. To learn more, refer to [](/deploy-manage/production-guidance/kibana-task-manager-scaling-considerations.md).
:::

::::

## What adds the most load [rule-performance-load]

Rules add the most search load when:

* You run many rules, or run them often. Each rule searches your data on its **Runs every** schedule.
* Rules look back over long time ranges. Some rule types do this by default. For example, [new terms rules](/solutions/security/detect-and-alert/new-terms.md) have a 7-day **History Window Size**, and the **Indicator index query** of [indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) searches the last 30 days of threat indicators.
* Rules miss scheduled runs, which leaves gaps. When you [fill those gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md), the rule runs again over each missed time range.

Each rule run also has a time limit, and the more load your rules add, the more likely rules are to reach it. On {{serverless-short}}, indicator match rules stop after 10 minutes, EQL rules after 5 minutes, and all other detection rules after 1 minute. On {{stack}}, indicator match rules stop after 1 hour and all other detection rules after 5 minutes by default, and administrators can change the limits with `xpack.alerting.rules.run.timeout`. When a run stops early, it can miss alerts for its time range.

## Keep rules running on time [rule-performance-best-practices]

To keep search load manageable:

* Turn on only the rules you need, and turn them on in small batches.
* Stagger rule schedules so fewer rules run at the same time.
* Keep **Additional look-back time** as short as your tolerance for missed detections allows, but no shorter than 1 minute. For details, refer to [Schedule settings](/solutions/security/detect-and-alert/common-rule-settings.md#rule-schedule).
* Narrow the **Indicator index query** of indicator match rules when you don't need 30 days of threat indicators.
* Shorten the **History Window Size** of new terms rules only when you have to. With a shorter history, terms that appeared earlier can count as new, which creates more alerts.
* Narrow the time range on dashboards that run alongside your rules.

## Check whether rules have enough capacity [rule-performance-monitor]

Signs that you're running out of search capacity include rule failures or timeouts on the [**Rule Monitoring** tab](/solutions/security/detect-and-alert/monitor-rule-executions.md#rule-monitoring-tab), `Request timed out` errors in {{kib}}, circuit breaker exceptions, and slower queries in Discover. If rules already fail or time out, refer to [Troubleshoot rule timeouts caused by search load](/troubleshoot/security/detection-rules.md#security-search-capacity).

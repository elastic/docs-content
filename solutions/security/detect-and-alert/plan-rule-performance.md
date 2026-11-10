---
navigation_title: Plan for rule performance
applies_to:
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Learn how detection rules use search capacity in Elastic Security serverless projects, which rule settings add the most load, and how to keep rules running on time.
---

# Plan detection rules for search performance [plan-rule-performance]

Every detection rule run searches your data. When too many searches run at once, rules slow down, time out, or fail, and you can miss alerts. Plan rule schedules and lookback times with search load in mind, especially before you turn on many rules at once.

## How search capacity works [rule-performance-search-capacity]

% TODO: "Most recent day" is still unverified for Security projects. It lives in the Elastic Cloud serverless configuration, not in the Kibana or docs repos. Confirm with the serverless team before merging.

Detection rules share search capacity with everything else that queries your project, including dashboards, Discover, {{esql}} queries, and external clients.

{{ecloud}} sizes your project's search capacity to its volume of search-ready data, which includes data from the most recent day. Capacity doesn't scale up when query load increases. Searches on recent data are fastest. Older data stays searchable, but queries on it are slower and use more capacity. Ingest runs separately and doesn't compete with search. To learn what counts as search-ready data, refer to [Search AI Lake settings](/deploy-manage/deploy/elastic-cloud/project-settings.md#elasticsearch-manage-project-search-ai-lake-settings).

If you need more search capacity, or want more than the most recent day of data to be search-ready, contact Elastic Support.

## What adds the most load [rule-performance-load]

Rules add the most search load when:

* You run many rules, or run them often. Each rule searches your data on its **Runs every** schedule.
* Rules look back over long time ranges. Some rule types do this by default. For example, [new terms rules](/solutions/security/detect-and-alert/new-terms.md) have a 7-day **History Window Size**, and the **Indicator index query** of [indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) searches the last 30 days of threat indicators.
* Rules miss scheduled runs, which leaves gaps. When you [fill those gaps](/solutions/security/detect-and-alert/fill-rule-gaps.md), the rule runs again over each missed time range.

Each rule run also has a time limit, and the more load your rules add, the more likely rules are to reach it. Indicator match rules stop after 10 minutes, EQL rules after 5 minutes, and all other detection rules after 1 minute. When a run stops early, it can miss alerts for its time range.

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

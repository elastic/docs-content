---
navigation_title: Case analytics
applies_to:
  stack: preview 9.2-9.4, ga 9.5+
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Query case analytics indices to track operational metrics like MTTR, case volume, and analyst workload with Discover, Lens, and ES|QL.
---

# Case analytics [case-analytics]

Case analytics helps you report on your cases at scale. Behind the scenes, Elastic mirrors your case data into dedicated analytics indices and keeps them in sync as cases change, so your reports always reflect the latest activity.

Because that data lives in {{es}} indices, you can work with it using the tools you already know. Track case volume and trends, closure rates, mean time to respond (MTTR) and other timings, assignee workload, alert and observable breakdowns, and case field metrics with [Discover](../discover.md), [Lens](../visualize/lens.md), {{esql}}, dashboards, and alerting.

To dive in, [explore and visualize your case data](explore-case-data.md) or [query it with {{esql}}](query-case-data-esql.md). The rest of this section covers where your data lives, the fields you can report on, and how to grant access and administer the feature.

:::{dropdown} Turn on case analytics in 9.2-9.4
:applies_to: stack: preview 9.2-9.4
On {{stack}} 9.2-9.4, you need to turn on case analytics first. To do this, add `xpack.cases.analytics.index.enabled: true` to your [`kibana.yml`](/deploy-manage/stack-settings.md) file.

This feature works best when your deployment has 10 or fewer spaces with cases. In each of those spaces, a background task refreshes the analytics indices every five minutes, so with many spaces the combined work can put too much load on Task Manager. If you have more spaces, hold off on turning it on.
:::

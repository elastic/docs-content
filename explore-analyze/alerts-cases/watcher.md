---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/xpack-alerting.html
  - https://www.elastic.co/guide/en/cloud/current/ec-watcher.html
  - https://www.elastic.co/guide/en/kibana/current/watcher-ui.html
  - https://www.elastic.co/guide/en/serverless/current/elasticsearch-differences.html#elasticsearch-differences-serverless-features-replaced
  - https://www.elastic.co/guide/en/kibana/current/secure-reporting.html#securing-reporting
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: kibana
description: Overview of Watcher for creating custom alerting workflows with advanced scripting and transformations.
---

# {{watcher}} [watcher]

::::{tip}
{{kib}} Alerting provides a set of built-in actions and alerts that are integrated with applications such as APM, Metrics, Security, and Uptime. You can use {{kib}} Alerting to detect complex conditions within different {{kib}} apps and trigger actions when those conditions are met. For more information, refer to [Alerts and Cases](../alerts-cases.md).
::::

{{watcher}} enables you to create sophisticated alerting workflows by watching for changes or anomalies in your data and performing automated actions in response. Using periodic {{product.elasticsearch}} queries, custom conditions, and flexible actions, {{watcher}} supports complex monitoring scenarios that require advanced scripting, data transformations, or custom logic beyond standard alerting rules.

Common use cases:

* Monitor social media as another way to detect failures in user-facing automated systems like ATMs or ticketing systems. When the number of tweets and posts in an area exceeds a threshold of significance, notify a service technician.
* Monitor your infrastructure, tracking disk usage over time. Open a helpdesk ticket when any servers are likely to run out of free space in the next few days.
* Track network activity to detect malicious activity, and proactively change firewall configuration to reject the malicious user.
* Monitor {{product.elasticsearch}}, and send immediate notification to the system administrator if nodes leave the cluster or query throughput exceeds an expected range.
* Track application response times and if page-load time exceeds SLAs for more than 5 minutes, open a helpdesk ticket. If SLAs are exceeded for an hour, page the administrator on duty.

All of these use cases share a few key properties:

* The relevant data or changes in data can be identified with a periodic {{product.elasticsearch}} query.
* The results of the query can be checked against a condition.
* One or more actions are taken if the condition is true — an email is sent, a third party system is notified, or the query results are stored.

## How watches work [_how_watches_work]

The {{alert-features}} provide an API for creating, managing and testing *watches*. A watch describes a single alert and can contain multiple notification actions.

A watch is constructed from four simple building blocks:

Schedule
:   A schedule for running a query and checking the condition.

Query
:   The query to run as input to the condition. Watches support the full {{product.elasticsearch}} query language, including aggregations.

Condition
:   A condition that determines whether or not to execute the actions. You can use simple conditions (always true), or use scripting for more sophisticated scenarios.

Actions
:   One or more actions, such as sending email, pushing data to third party systems through a webhook, or indexing the results of the query.

A full history of all watches is maintained in an {{product.elasticsearch}} index. This history keeps track of each time a watch is triggered and records the results from the query, whether the condition was met, and what actions were taken.

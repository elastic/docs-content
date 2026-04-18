---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/alerting-getting-started.html#alerting-concepts-differences
  - https://www.elastic.co/guide/en/serverless/current/project-settings-alerts.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: elasticsearch
  - id: cloud-hosted
navigation_title: Alerting
description: "Elastic alerting overview. Kibana v1 on stack and serverless, v2 as a serverless tech preview, Watcher on stack only. Rules, connectors, v2 history, and shared notification controls."
---

# Alerting [alerting-overview]

Elastic alerting helps you watch your data and respond when something needs attention, whether that is a metric crossing a limit, an asset leaving an area on a map, or an unusual pattern in your time series. You set the conditions and how people should be notified. Elastic runs the checks for you.

Elastic offers three alerting systems, summarized below. Each has a **Get started** link to the full guide for that option.

## Kibana alerting v1

```{applies_to}
stack: ga
serverless: ga
```

Kibana alerting v1 gives you ready-made rule types that work with applications such as APM, metrics, security, and uptime monitoring. You set conditions on a schedule you choose and send notifications through common channels (email, chat apps, webhooks, on-call tools, and more). Setup uses forms and clear steps, so you do not need to learn a query language first. It is a strong fit when you want broad coverage out of the box.

[Get started with Kibana alerting v1 →](alerting/kibana-alerting-v1.md)

## {{alerting-v2}}

```{applies_to}
serverless: preview
stack: ga
```

{{alerting-v2}} is built on ES|QL. You define what to watch for and what information should travel with each alert, then decide how basic or advanced you want that workflow to be. V2 adds **action policies** for centralized notification control, per-series snooze, alert lifecycle tracking with episodes, and **rules on alerts** for correlation and escalation.

Here is what you get with v2:

* **Flexible paths.** Keep a guided experience when you want it, and adopt deeper options (including setups you can manage like code) without switching to a different alerting style.
* **Visibility over time.** Each time a rule finds a matching condition, the outcome is stored in a searchable history of what happened and when. That supports investigations, reviews, and spotting trends instead of only seeing what is open right now.
* **Connected analysis.** Use the same ES|QL skills in Discover and in rules, refine queries where you already explore data, and add follow-up rules when related conditions should be grouped together.
* **Control over notifications.** Reuse shared settings for who gets notified, and how often, across many rules. You set routing, grouping, and frequency in one place so teams hear what matters with less repeated setup and fewer unnecessary messages.
* **Consistent status from open to closed.** Track alerts from the first time they appear until the problem is gone, with shared stages, a way to mark items as handled, and pauses you can tune per group so everyone agrees on what counts as still active and what counts as finished.

[Get started with {{alerting-v2}} →](alerting/kibana-alerting-v2.md)

:::{note}
{{alerting-v2}} runs next to Kibana alerting v1 on supported deployments. You do not have to move everything at once. Teams can copy or rebuild rules when they are ready. Kibana alerting v1 will remain available.
:::

## Watcher

```{applies_to}
stack: ga
serverless: unavailable
```

Watcher is for unusual or highly tailored setups where you need scripts, chained steps, or close control over {{es}} APIs. It does not use the main {{kib}} rules UI used by {{kib}} alerting. It is available on the {{stack}} only, not in {{serverless-full}}.

:::{tip}
For most teams, Kibana alerting v1 or v2 is easier to adopt: they include more ready-made building blocks and a single place in {{kib}} to work with rules.
:::

[Get started with Watcher →](alerting/watcher.md)

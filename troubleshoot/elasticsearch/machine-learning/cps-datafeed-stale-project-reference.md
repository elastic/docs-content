---
navigation_title: Stale project reference
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Stale project reference [cps-datafeed-stale-project-reference]

A {{cps}} {{ml}} {{dfeeds}} can reference a linked project that was renamed, unlinked, or never connected. Stale references appear in `project_routing` expressions or in qualified index patterns such as `old-alias:logs-*`. The {{dfeeds}} may skip the project, fail searches, or reject updates depending on how the reference is expressed.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose stale project reference [diagnose-cps-datafeed-stale-project-reference]

**Symptoms**

* **Messages** or extraction errors reference a project alias that no longer appears in {{ecloud}} linked-project settings.
* `GET _ml/datafeeds/{datafeed_id}/_stats` shows repeated skips for one linked project while others succeed.
* Updating a {{dfeeds}} with a qualified index (`project:index`) fails immediately if the named project is missing or unauthorized.
* `project_routing` still contains an `_alias:` tag that matched a project before it was renamed.

**Check configuration and topology**

```console
GET _ml/datafeeds/{datafeed_id}
GET _remote/info
```

Compare `project_routing`, index qualifiers, and `_remote/info` linked aliases. A project listed in routing but absent from `_remote/info` is a stale reference.

For skip behavior on still-linked but misrouted projects, see also [Linked project skipped](cps-datafeed-linked-project-skipped.md).

## Resolve stale project reference [resolve-cps-datafeed-stale-project-reference]

**Confirm the link in {{ecloud}}**

In {{ecloud}} project settings, verify the target project is linked and note its current alias. Re-link the project if the connection was removed.

**Update routing after a rename**

If a linked project alias changed, update `project_routing` and any qualified index references to use the new alias:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:new-alias-*",
  "indices": ["new-alias:logs-*"]
}
```

Stop the {{dfeeds}} before changing qualified index patterns if the job is running.

**Handle qualified indices**

Qualified `project:index` references fail on update when the project is missing — fix the project link or remove the qualifier before retrying. Unqualified index patterns with stale routing may still persist until run time; fix routing proactively to avoid extraction failures.

**Verify recovery**

After updating references, confirm `_remote/info` lists the project and that `GET _ml/datafeeds/{datafeed_id}/_stats` no longer reports skips for the old alias.

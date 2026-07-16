---
navigation_title: Routing matches no project
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: machine-learning
---

# Routing matches no project [cps-datafeed-routing-no-match]

A {{cps}} {{ml}} {{dfeeds}} uses `project_routing` to decide which linked projects to search. When routing matches no project, searches fail with a resource-not-found error. Flat-world {{dfeeds}} (empty `project_routing`) may be created successfully but fail at run time if no linked projects exist yet.

:::{tip}
If you can't find your issue here, explore the other [troubleshooting topics](/troubleshoot/index.md) or [contact us](/troubleshoot/index.md#contact-us).
:::

## Diagnose routing matches no project [diagnose-cps-datafeed-routing-no-match]

**Error messages**

During datafeed extraction or preview, the API or job **Messages** may report one of these errors:

```txt
No such project: [alias]
```

```txt
no matching project after applying project routing [expression]
```

Replace `[alias]` and `[expression]` with the values from your error. A qualified index reference such as `missing-project:logs-*` can also produce `No such project: [alias] with project routing [[expression]]` when routing is set.

**When it happens**

| Situation | Typical behavior |
| --- | --- |
| Flat-world {{dfeeds}} (`project_routing` empty) with no linked projects | Create or update may succeed; first run-time search fails |
| `_alias:` expression matches no linked project tags | Fails at search time |
| Typo in alias or routing expression | Fails at search time |
| Qualified `project:index` references a project that does not exist | Often fails on create or update |

**Check configuration**

```console
GET _ml/datafeeds/{datafeed_id}
GET _remote/info
```

Compare `project_routing` with the linked projects returned by `_remote/info`.

## Resolve routing matches no project [resolve-cps-datafeed-routing-no-match]

**Link the missing project**

If routing references a project that should be in scope, establish the link in {{ecloud}} project settings, then restart or wait for the next {{dfeeds}} cycle.

**Fix `project_routing` spelling and syntax**

Correct typos in alias tags or routing expressions. Examples:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_alias:production-*"
}
```

**Narrow to the origin project**

When no linked projects are available yet, or you only need local data, set local-only routing:

```console
POST _ml/datafeeds/{datafeed_id}/_update
{
  "project_routing": "_origin"
}
```

You can also use `_alias:_origin`. See [Project routing in {{cps-init}}](/explore-analyze/cross-project-search/cross-project-search-project-routing.md).

**Verify recovery**

Confirm the error no longer appears in **Messages** and that `GET _ml/datafeeds/{datafeed_id}/_stats` shows successful extraction cycles.

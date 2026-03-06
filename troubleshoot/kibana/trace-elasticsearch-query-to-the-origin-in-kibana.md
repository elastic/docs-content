---
navigation_title: Trace {{es}} query
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kibana-troubleshooting-trace-query.html
applies_to:
  deployment:
    ess: all
    ece: all
    self: all
    eck: all
products:
  - id: kibana
---

# Trace an {{es}} query in {{kib}} [kibana-troubleshooting-trace-query]

Sometimes the {{es}} server might be slowed down by the execution of an expensive query. Such queries are logged to {{es}}'s [search slow log](/deploy-manage/monitor/logging-configuration/slow-logs.md#enable-slow-log) file. But there is a problem: it’s impossible to say what triggered a slow search request—a {{kib}} instance or a user accessing an {{es}} endpoint directly. To simplify the investigation of such cases, the search slow log file includes the `x-opaque-id` header, which might provide additional information about a request if it originated from {{kib}}.

::::{warning}
At the moment, {{kib}} can only highlight cases where a slow query originated from a {{kib}} visualization, **Lens**, **Discover**, **Maps**, or **Alerting**.
::::


For example, if a request to {{es}} was initiated by a Vega visualization on a dashboard, you will see the following in the slow logs:

```json
"source": { "id": "c89d1ab3-b4a7-4920-a64a-22a910a413b0;kibana:application:dashboard:edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b;visualization:Vega:cb099a20-ea66-11eb-9425-113343a037e3" }
```

Take a closer look at the format of the string. The id value starts with  `c89d1ab3-b4a7-4920-a64a-22a910a413b0`, which is a unique identifier of a request set by the {{kib}} server. The part after the `kibana` prefix indicates that the request was triggered by **Dashboard** with id `edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b` and Vega visualization with id `cb099a20-ea66-11eb-9425-113343a037e3`.

If the provided information is not enough to identify a visualization to adjust its parameters, you can configure {{kib}} logs to provide a human-readable description and a link to a source of the request:

```yaml
logging:
  loggers:
    - name: execution_context
      level: debug
      appenders: [console]
```

The `execution_context` debug logs now also include the {{kib}} **space ID** in a `space` field.

Now, you can view the request to {{es}} has been initiated by the `[Logs] Unique Visitor Heatmap` visualization embedded in the `[Logs] Web Traffic` dashboard, and which space it was executed from.

```text
[DEBUG][execution_context] stored the execution context: {
  "space": "default",
  "type": "application",
  "name": "dashboard",
  "id": "edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b",
  "description": "[Logs] Web Traffic",
  "url": "/view/edf84fe0-e1a0-11e7-b6d5-4dc382ef7f5b",
  "child": {
    "type": "visualization",
    "name": "Vega",
    "id": "cb099a20-ea66-11eb-9425-113343a037e3",
    "description": "[Logs] Unique Visitor Heatmap",
    "url": "/app/visualize#/edit/cb099a20-ea66-11eb-9425-113343a037e3"
  },
}
```

## How to find the space for a slow query

Use this flow when you can see a slow query in {{es}} slow logs, and want to identify which {{kib}} space it came from.

1. Enable {{es}} [search slow logs](/deploy-manage/monitor/logging-configuration/slow-logs.md#enable-slow-log).
2. Find the `x-opaque-id` value in the slow log entry (often in `elasticsearch.slowlog.id`).
3. Enable `execution_context` debug logging in {{kib}} (example above).
4. Match the slow log entry to an `execution_context` debug entry by the context chain (`type` / `name` / `id`) first, then narrow it down by time, and finally read the `space` field.

### ES|QL: parse `elasticsearch.slowlog.id` into context columns

If slow logs are shipped into {{es}}, you can use {{esql}} to extract the request ID and the context chain (adjust the index pattern as needed):

```esql
FROM logs-*
| WHERE fileset.name == "slowlog" AND elasticsearch.slowlog.id LIKE "*;kibana:*"
| DISSECT elasticsearch.slowlog.id """%{request_id};kibana:%{root_type}:%{root_name}:%{root_id};%{child_type}:%{child_name}:%{child_id}"""
| KEEP @timestamp, request_id, root_type, root_name, root_id, child_type, child_name, child_id
| SORT @timestamp DESC
```

## Related links

- [Slow query and index logging](/deploy-manage/monitor/logging-configuration/slow-logs.md)
- [{{kib}} logging](/deploy-manage/monitor/logging-configuration/kibana-logging.md)
- [Set global log levels for {{kib}}](/deploy-manage/monitor/logging-configuration/kibana-log-levels.md)


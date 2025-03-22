---
navigation_title: Elasticsearch logfile output
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/audit-log-output.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
  serverless: unavailable
---

# Elasticsearch logfile audit output [audit-log-output]

The `logfile` audit output is the only output for auditing. By default, it writes data to the `<clustername>_audit.json` file in the logs directory. The file is also rotated and archived daily or upon reaching the 1GB file size limit.

In self-managed clusters, you can configure how the `logfile` is written in the `log4j2.properties` file located in `ES_PATH_CONF` (or check out the relevant portion of the [log4j2.properties in the sources](https://github.com/elastic/elasticsearch/blob/master/x-pack/plugin/core/src/main/config/log4j2.properties)). However, **Elastic strongly recommends using the default Log4j2 configuration**.

Orchestrated deployments (ECH, ECE, and ECK) do not support changes in `log4j2.properties` files of the {{es}} instances.

::::{note}
If you overwrite the `log4j2.properties` and do not specify appenders for any of the audit trails, audit events are forwarded to the root appender, which by default points to the `elasticsearch.log` file.
::::

For {{es}} configuration options that control event filtering in audit logs, refer to [](./configuring-audit-logs.md).

## Log entry format [audit-log-entry-format]

The audit events are formatted as JSON documents, and each event is printed on a separate line in the `<clustername>_audit.json` file. The entries themselves do not contain the end-of-line delimiter. The audit event JSON format is somewhat particular, as **most** fields follow a dotted name syntax, are ordered, and contain non-null string values. This format creates a structured columnar aspect, similar to a CSV, that can be more easily inspected visually (compared to an equivalent nested JSON document).

There are however a few attributes that are exceptions to the above format. The `put`, `delete`, `change`, `create` and `invalidate` attributes, which are only present for events with the `event.type: "security_config_change"` attribute, contain the **nested JSON** representation of the security change taking effect. The contents of the security config change are hence not displayed as top-level dot-named fields in the audit event document. That’s because the fields are specific to the particular kind of security change and do not show up in any other audit events. The benefits of a columnar format are therefore much more limited; the space-saving benefits of the nested structure is the favoured trade-off in this case.

When the `request.body` attribute is present (see [Auditing search queries](./auditing-search-queries.md)), it contains a string value containing the full HTTP request body, escaped as per the JSON RFC 4677.

Refer to [audit event types](elasticsearch://reference/elasticsearch/elasticsearch-audit-events.md) for a complete list of fields, as well as examples, for each entry type.

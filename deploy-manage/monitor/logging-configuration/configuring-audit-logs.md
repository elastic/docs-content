---
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
  serverless: unavailable
---

# Configure audit logging [audit-logging-configuration]

When auditing security events, a single client request might generate multiple audit events across multiple cluster nodes, potentially leading to a high volume of log data and I/O operations. To maintain clarity and ensure logs remain actionable, {{es}} and {{kib}} provide configuration mechanisms to control what events are logged and which can be ignored.

### Elasticsearch auditing configuration

{{es}} configuration options include:

  * [{{es}} audited events settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#event-audit-settings): Use include and exclude filters to control the types of events that get logged.
  * [{{es}} node information settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#node-audit-settings): Control whether to add or hide node information such as hostname or IP address in the audited events.
  * [{{es}} ignore policies settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#audit-event-ignore-policies): Use ignore policies for fine-grained control over which audit events are printed to the log file.

    ::::{tip}
    In {{es}}, all auditing settings except `xpack.security.audit.enabled` are dynamic. This means you can configure them using the [cluster update settings API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html), allowing changes to take effect immediately without requiring a restart. This approach is faster and more convenient than modifying `elasticsearch.yml`. 
    ::::

For a complete description of event details and format, refer to the following resources:
  * [{{es}} audit events details and schema]() asciidocalypse://elasticsearch/docs/reference/elasticsearch/elasticsearch-audit-events
  * [{{es}} log entry output format](/deploy-manage/monitor/logging-configuration/logfile-audit-output.md#audit-log-entry-format)

### Kibana auditing configuration

To control the logs that are outputted by Kibana, you can use [{{kib}} ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters). These are a list of filters that determine which events should be excluded from the audit log.

In self-managed systems, you can optionally configure audit logs location, and file/rolling file using [{{kib}} audit logging settings](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-settings).


::::{tip}
To configure {{kib}} settings, follow the same [procedure](./enabling-audit-logs.md#enable-audit-logging-procedure) as when enabling {{kib}} audit logs, but apply the relevant settings instead.
::::

For a complete description of auditing event details, such as `category`, `type`, or `action`, refer to [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging).

### General recommendations

* Consider starting with {{es}} [`xpack.security.audit.logfile.events.include`](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#xpack-sa-lf-events-include) and [{{kib}} ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters) settings to specify the type of events you want to include or exclude in the auditing output.

* If you need a more granular control, refer to [{{es}} audit events ignore policies](./logfile-audit-events-ignore-policies.md) for a better understanding how ignore policies work and when they are beneficial.

* Refer to [auditing search queries](./auditing-search-queries.md) for details on logging request bodies in the {{es}} audit logs.

  ::::{important}
  Sensitive data may be audited in plain text when including the request body in audit events, even though all the security APIs, such as those that change the user’s password, have the credentials filtered out when audited.
  ::::

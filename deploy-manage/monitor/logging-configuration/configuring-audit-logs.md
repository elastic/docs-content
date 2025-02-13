---
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
  serverless: unavailable
---

# Configure audit logging [audit-logging-configuration]

When auditing security events, a single client request might generate multiple audit events across multiple cluster nodes, potentially leading to a high volume of log data and *I/O operations*. To maintain clarity and ensure logs remain actionable, {{es}} and {{kib}} provide configuration mechanisms to control what events are logged and which can be ignored.

### Elasticsearch auditing configuration

**{{es}} configuration** options include:

  * [{{es}} audited events settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#event-audit-settings)
  * [{{es}} node information settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#node-audit-settings)
  * [{{es}} ignore policies settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#audit-event-ignore-policies)

    ::::{tip}
    In {{es}}, all auditing settings except `xpack.security.audit.enabled` are **dynamic**, which means you can configure them using the [cluster update settings API](https://www.elastic.co/guide/en/elasticsearch/reference/current/cluster-update-settings.html) as a faster and more convenient method that applies changes without requiring a restart.
    ::::

Note that {{ech}} deployments provide its own subset of supported settings for auditing configuration:
  * [Elasticsearch audit settings for Elastic Cloud Hosted deployments](https://www.elastic.co/guide/en/cloud/current/ec-add-user-settings.html#ec_audit_settings)

For a complete description of event details and format, refer to:
  * [{{es}} audit events details and schema](/deploy-manage/monitor/logging-configuration/elasticsearch-audit-events.md).
  * [{{es}} logentry output format](/deploy-manage/monitor/logging-configuration/logfile-audit-output.md#audit-log-entry-format)

### Kibana auditing configuration

**{{kib}} configuration** options include:

  * [{{kib}} ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters)

    ::::{tip}
    To configure {{kib}} settings, follow the same [procedure](./enabling-audit-logs.md#enable-audit-logging-procedure) as when enabling {{kib}} audit logs, but apply the relevant settings instead.
    ::::

Note that {{ech}} deployments provide its own subset of supported settings for auditing configuration:
  * [Kibana audit settings on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-manage-kibana-settings.html#ec_logging_and_audit_settings)

For a complete description of auditing event details, such as `category`, `type`, or `action`, refer to:
  * [{{kib}} audit events](https://www.elastic.co/guide/en/kibana/current/xpack-security-audit-logging.html#xpack-security-ecs-audit-logging)

### General recommendations

* Consider starting with [`xpack.security.audit.logfile.events.include`](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html#xpack-sa-lf-events-include) or the corresponding `exclude` setting to specify the type of events you want to include or exclude in the {{es}} auditing output.

* If you need a more granular control, refer to [{{es}} audit events ignore policies](./logfile-audit-events-ignore-policies.md) for a better understanding how ignore policies work and when they are beneficial.

* Refer to [auditing search queries](./auditing-search-queries.md) for details on logging request bodies in the {{es}} audit logs.

  ::::{important}
  Be advised that **sensitive data may be audited in plain text** when including the request body in audit events, even though all the security APIs, such as those that change the user’s password, have the credentials filtered out when audited.
  ::::

* Use {{kib}} [ignore filters](https://www.elastic.co/guide/en/kibana/current/security-settings-kb.html#audit-logging-ignore-filters) if you want to filter out certain events from the {{kib}} audit log.
---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/enable-audit-logging.html
---

# Enabling elasticsearch audit logs [enable-audit-logging]

You can log security-related events such as authentication failures and refused connections to monitor your cluster for suspicious activity (including data access authorization and user security configuration changes).

Audit logging also provides forensic evidence in the event of an attack.

::::{important}
Audit logs are **disabled** by default. You must explicitly enable audit logging.

::::


::::{tip}
Audit logs are only available on certain subscription levels. For more information, see {{subscriptions}}.
::::


To enable audit logging:

1. Set `xpack.security.audit.enabled` to `true` in `elasticsearch.yml`.
2. Restart {{es}}.

When audit logging is enabled, [security events](elasticsearch-audit-events.md) are persisted to a dedicated `<clustername>_audit.json` file on the host’s file system, on every cluster node. For more information, see [Logfile audit output](logfile-audit-output.md).

You can configure additional options to control what events are logged and what information is included in the audit log. For more information, see [Auditing settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/auditing-settings.html).

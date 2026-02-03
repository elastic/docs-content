---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logging.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# {{es}} deprecation logs [logging]

{{es}} writes deprecation logs to the [log directory](/deploy-manage/monitor/logging-configuration.md#access-kib-and-es-logs). These logs record a message when you use deprecated {{es}} functionality. You can use the deprecation logs to update your application before upgrading {{es}} to a new major version.

:::{tip}
You can also access deprecation warnings in the [upgrade assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md).
:::

By default, {{es}} rolls and compresses deprecation logs at 1GB. The default configuration preserves a maximum of five log files: four rolled logs and an active log.

{{es}} emits deprecation log messages at the `CRITICAL` level. Those messages are indicating that a used deprecation feature will be removed in a next major version. Deprecation log messages at the `WARN` level indicates that a less critical feature was used, it won’t be removed in next major version, but might be removed in the future.

To stop writing deprecation log messages, change the logging level:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.org.elasticsearch.deprecation": "OFF"
  }
}
```

Alternatively, in self-managed clusters, you can set `logger.deprecation.level` to `OFF` in `log4j2.properties` :

```properties
logger.deprecation.level = OFF
```

For more information on the available log levels, refer to [Configuring logging levels](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md).

You can identify what is triggering deprecated functionality if `X-Opaque-Id` was used as an HTTP header. The user ID is included in the `X-Opaque-ID` field in deprecation JSON logs.

```json
{
  "type": "deprecation",
  "timestamp": "2019-08-30T12:07:07,126+02:00",
  "level": "WARN",
  "component": "o.e.d.r.a.a.i.RestCreateIndexAction",
  "cluster.name": "distribution_run",
  "node.name": "node-0",
  "message": "[types removal] Using include_type_name in create index requests is deprecated. The parameter will be removed in the next major version.",
  "x-opaque-id": "MY_USER_ID",
  "cluster.uuid": "Aq-c-PAeQiK3tfBYtig9Bw",
  "node.id": "D7fUYfnfTLa2D7y-xw6tZg"
}
```

Deprecation logs can be indexed into the `.logs-deprecation.elasticsearch-default` data stream when `cluster.deprecation_indexing.enabled` setting is set to true.


### Deprecation logs throttling [_deprecation_logs_throttling]

Deprecation logs are deduplicated based on a deprecated feature key and `x-opaque-id` so that if a feature is repeatedly used, it will not overload the deprecation logs. This applies to both indexed deprecation logs and logs emitted to log files. You can disable the use of `x-opaque-id` in throttling by changing `cluster.deprecation_indexing.x_opaque_id_used.enabled` to false. Refer to this class [javadoc](https://artifacts.elastic.co/javadoc/org/elasticsearch/elasticsearch/8.17.3/org.elasticsearch.server/org/elasticsearch/common/logging/RateLimitingFilter.html) for more details.
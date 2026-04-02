---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logging.html
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Update {{es}} logging levels [logging]

$$$deprecation-logging$$$
$$$_deprecation_logs_throttling$$$

Log4j 2 log messages include a *level* field, which is one of the following (in order of increasing verbosity):

* `FATAL`
* `ERROR`
* `WARN`
* `INFO`
* `DEBUG`
* `TRACE`

By default, {{es}} includes all messages at levels `INFO`, `WARN`, `ERROR` and `FATAL` in its logs, but filters out messages at levels `DEBUG` and `TRACE`. This is the recommended configuration. 

Do not filter out messages at `INFO` or higher log levels, or else you may not be able to understand your cluster’s behavior or troubleshoot common problems. 

Do not enable logging at levels `DEBUG` or `TRACE` unless you are following instructions elsewhere in this manual which call for more detailed logging, or you are an expert user who will be reading the {{es}} source code to determine the meaning of the logs.

Messages are logged by a hierarchy of loggers which matches the hierarchy of Java packages and classes in the [{{es}} source code](https://github.com/elastic/elasticsearch/). Every logger has a corresponding [dynamic setting](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) which can be used to control the verbosity of its logs. The setting’s name is the fully-qualified name of the package or class, prefixed with `logger.`.

You can set each logger’s verbosity to the name of a log level, for instance `DEBUG`, which means that messages from this logger at levels up to the specified one will be included in the logs. You can also use the value `OFF` to suppress all messages from the logger.

For example, the `org.elasticsearch.discovery` package contains functionality related to the [discovery](../../distributed-architecture/discovery-cluster-formation/discovery-hosts-providers.md) process, and you can control the verbosity of its logs with the `logger.org.elasticsearch.discovery` setting. To enable `DEBUG` logging for this package, use the [Cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) as follows:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.org.elasticsearch.discovery": "DEBUG"
  }
}
```

To reset this package’s log verbosity to its default level, set the logger setting to `null`:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.org.elasticsearch.discovery": null
  }
}
```

Other ways to change log levels include:

1. [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

    ```yaml
    logger.org.elasticsearch.discovery: DEBUG
    ```

    This is most appropriate when debugging a problem on a single node.

2. `log4j2.properties` (self-managed clusters only):

    ```properties
    logger.discovery.name = org.elasticsearch.discovery
    logger.discovery.level = debug
    ```

    This is most appropriate when you already need to change your Log4j 2 configuration for other reasons. For example, you may want to send logs for a particular logger to another file. However, these use cases are rare.


::::{important}
{{es}}'s application logs are intended for humans to read and interpret. Different versions of {{es}} might report information in these logs in different ways. For example, they might add extra detail, remove unnecessary information, format the same information in different ways, rename the logger, or adjust the log level for specific messages. Do not rely on the contents of the application logs remaining exactly the same between versions.
::::

::::{note}
To prevent leaking sensitive information in logs, {{es}} suppresses certain log messages by default even at the highest verbosity levels. To disable this protection on a node, set the Java system property `es.insecure_network_trace_enabled` to `true`. This feature is primarily intended for test systems that do not contain any sensitive information. If you set this property on a system which contains sensitive information, you must protect your logs from unauthorized access.
::::

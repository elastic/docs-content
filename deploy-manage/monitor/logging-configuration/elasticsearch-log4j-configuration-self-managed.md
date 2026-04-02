---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logging.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---

# {{es}} log4j configuration [logging]

::::{important}
Elastic strongly recommends using the Log4j 2 configuration that is shipped by default.
::::

{{es}} uses [Log4j 2](https://logging.apache.org/log4j/2.x/) for logging. Log4j 2 can be configured using the log4j2.properties file. {{es}} exposes three properties, `${sys:es.logs.base_path}`, `${sys:es.logs.cluster_name}`, and `${sys:es.logs.node_name}` that can be referenced in the configuration file to determine the location of the log files. The property `${sys:es.logs.base_path}` will resolve to the log directory, `${sys:es.logs.cluster_name}` will resolve to the cluster name (used as the prefix of log filenames in the default configuration), and `${sys:es.logs.node_name}` will resolve to the node name (if the node name is explicitly set).

For example, if your log directory (`path.logs`) is `/var/log/elasticsearch` and your cluster is named `production` then `${sys:es.logs.base_path}` will resolve to `/var/log/elasticsearch` and `${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}.log` will resolve to `/var/log/elasticsearch/production.log`.

:::{tip}
To learn how to configure logging levels, refer to [](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md).
:::

```properties
####### Server JSON ############################
appender.rolling.type = RollingFile <1>
appender.rolling.name = rolling
appender.rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.json <2>
appender.rolling.layout.type = ECSJsonLayout <3>
appender.rolling.layout.dataset = elasticsearch.server <4>
appender.rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.json.gz <5>
appender.rolling.policies.type = Policies
appender.rolling.policies.time.type = TimeBasedTriggeringPolicy <6>
appender.rolling.policies.time.interval = 1 <7>
appender.rolling.policies.time.modulate = true <8>
appender.rolling.policies.size.type = SizeBasedTriggeringPolicy <9>
appender.rolling.policies.size.size = 256MB <10>
appender.rolling.strategy.type = DefaultRolloverStrategy
appender.rolling.strategy.fileIndex = nomax
appender.rolling.strategy.action.type = Delete <11>
appender.rolling.strategy.action.basepath = ${sys:es.logs.base_path}
appender.rolling.strategy.action.condition.type = IfFileName <12>
appender.rolling.strategy.action.condition.glob = ${sys:es.logs.cluster_name}-* <13>
appender.rolling.strategy.action.condition.nested_condition.type = IfAccumulatedFileSize <14>
appender.rolling.strategy.action.condition.nested_condition.exceeds = 2GB <15>
################################################
```

1. Configure the `RollingFile` appender
2. Log to `/var/log/elasticsearch/production_server.json`
3. Use JSON layout.
4. `dataset` is a flag populating the `event.dataset` field in a `ECSJsonLayout`. It can be used to distinguish different types of logs more easily when parsing them.
5. Roll logs to `/var/log/elasticsearch/production-yyyy-MM-dd-i.json`; logs will be compressed on each roll and `i` will be incremented
6. Use a time-based roll policy
7. Roll logs on a daily basis
8. Align rolls on the day boundary (as opposed to rolling every twenty-four hours)
9. Using a size-based roll policy
10. Roll logs after 256 MB
11. Use a delete action when rolling logs
12. Only delete logs matching a file pattern
13. The pattern is to only delete the main logs
14. Only delete if we have accumulated too many compressed logs
15. The size condition on the compressed logs is 2 GB


```properties
####### Server -  old style pattern ###########
appender.rolling_old.type = RollingFile
appender.rolling_old.name = rolling_old
appender.rolling_old.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.log <1>
appender.rolling_old.layout.type = PatternLayout
appender.rolling_old.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name]%marker %m%n
appender.rolling_old.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.old_log.gz
```

1. The configuration for `old style` pattern appenders. These logs will be saved in `*.log` files and if archived will be in `* .log.gz` files. Note that these should be considered deprecated and will be removed in the future.


::::{note}
Log4j’s configuration parsing gets confused by any extraneous whitespace; if you copy and paste any Log4j settings on this page, or enter any Log4j configuration in general, be sure to trim any leading and trailing whitespace.
::::


Note than you can replace `.gz` by `.zip` in `appender.rolling.filePattern` to compress the rolled logs using the zip format. If you remove the `.gz` extension then logs will not be compressed as they are rolled.

If you want to retain log files for a specified period of time, you can use a rollover strategy with a delete action.

```properties
appender.rolling.strategy.type = DefaultRolloverStrategy <1>
appender.rolling.strategy.action.type = Delete <2>
appender.rolling.strategy.action.basepath = ${sys:es.logs.base_path} <3>
appender.rolling.strategy.action.condition.type = IfFileName <4>
appender.rolling.strategy.action.condition.glob = ${sys:es.logs.cluster_name}-* <5>
appender.rolling.strategy.action.condition.nested_condition.type = IfLastModified <6>
appender.rolling.strategy.action.condition.nested_condition.age = 7D <7>
```

1. Configure the `DefaultRolloverStrategy`
2. Configure the `Delete` action for handling rollovers
3. The base path to the {{es}} logs
4. The condition to apply when handling rollovers
5. Delete files from the base path matching the glob `${sys:es.logs.cluster_name}-*`; this is the glob that log files are rolled to; this is needed to only delete the rolled {{es}} logs but not also delete the deprecation and slow logs
6. A nested condition to apply to files matching the glob
7. Retain logs for seven days


Multiple configuration files can be loaded (in which case they will get merged) as long as they are named `log4j2.properties` and have the {{es}} config directory as an ancestor; this is useful for plugins that expose additional loggers. The logger section contains the java packages and their corresponding log level. The appender section contains the destinations for the logs. Extensive information on how to customize logging and all the supported appenders can be found on the [Log4j documentation](https://logging.apache.org/log4j/2.x/manual/configuration.html).


## JSON log format [json-logging]

To make parsing {{es}} logs easier, logs are now printed in a JSON format. This is configured by a Log4J layout property `appender.rolling.layout.type = ECSJsonLayout`. This layout requires a `dataset` attribute to be set which is used to distinguish logs streams when parsing.

```properties
appender.rolling.layout.type = ECSJsonLayout
appender.rolling.layout.dataset = elasticsearch.server
```
Each line contains a single JSON document with the properties configured in `ECSJsonLayout`. See this class [javadoc](https://artifacts.elastic.co/javadoc/org/elasticsearch/elasticsearch/8.17.3/org.elasticsearch.server/org/elasticsearch/common/logging/ESJsonLayout.html) for more details. 

If a JSON document contains an exception, it will be printed over multiple lines. The first line will contain regular properties and subsequent lines will contain the stacktrace formatted as a JSON array.

::::{note}
You can still use your own custom layout. To do that replace the line `appender.rolling.layout.type` with a different layout. See sample below:
::::


```properties
appender.rolling.type = RollingFile
appender.rolling.name = rolling
appender.rolling.fileName = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}_server.log
appender.rolling.layout.type = PatternLayout
appender.rolling.layout.pattern = [%d{ISO8601}][%-5p][%-25c{1.}] [%node_name]%marker %.-10000m%n
appender.rolling.filePattern = ${sys:es.logs.base_path}${sys:file.separator}${sys:es.logs.cluster_name}-%d{yyyy-MM-dd}-%i.log.gz
```


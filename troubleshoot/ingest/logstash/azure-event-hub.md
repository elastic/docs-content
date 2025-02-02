---
mapped_pages:
  - https://www.elastic.co/guide/en/logstash/current/ts-plugins.html#ts-azure
---

# Azure Event Hub [ts-plugins]

## Kafka issues and solutions [ts-kafka]


#### Kafka session timeout issues (input) [ts-kafka-timeout]

**Symptoms**

Throughput issues and duplicate event processing {{ls}} logs warnings:

```
[2017-10-18T03:37:59,302][WARN][org.apache.kafka.clients.consumer.internals.ConsumerCoordinator]
Auto offset commit failed for group clap_tx1: Commit cannot be completed since
the group has already rebalanced and assigned the partitions to another member.
```

The time between subsequent calls to `poll()` was longer than the configured `session.timeout.ms`, which typically implies that the poll loop is spending too much time processing messages. You can address this by increasing the session timeout or by reducing the maximum size of batches returned in `poll()` with `max.poll.records`.

```
[INFO][org.apache.kafka.clients.consumer.internals.ConsumerCoordinator] Revoking
previously assigned partitions [] for group log-ronline-node09
`[2018-01-29T14:54:06,485][INFO]`[org.apache.kafka.clients.consumer.internals.ConsumerCoordinator]
Setting newly assigned partitions [elk-pmbr-9] for group log-pmbr
```

**Background**

Kafka tracks the individual consumers in a consumer group (for example, a number of {{ls}} instances) and tries to give each consumer one or more specific partitions of data in the topic they’re consuming. In order to achieve this, Kafka tracks whether or not a consumer ({{ls}} Kafka input thread) is making progress on their assigned partition, and reassigns partitions that have not made progress in a set timeframe.

When {{ls}} requests more events from the Kafka Broker than it can process within the timeout, it triggers reassignment of partitions. Reassignment of partitions takes time, and can cause duplicate processing of events and significant throughput problems.

**Possible solutions**

* Reduce the number of records per request that {{ls}} polls from the Kafka Broker in one request,
* Reduce the number of Kafka input threads, and/or
* Increase the relevant timeouts in the Kafka Consumer configuration.

**Details**

The `max_poll_records` option sets the number of records to be pulled in one request. If it exceeds the default value of 500, try reducing it.

The `consumer_threads` option sets the number of input threads. If the value exceeds the number of pipeline workers configured in the `logstash.yml` file, it should certainly be reduced. If the value is greater than 4, try reducing it to `4` or less if the client has the time/resources for it. Try starting with a value of `1`, and then incrementing from there to find the optimal performance.

The `session_timeout_ms` option sets the relevant timeout. Set it to a value that ensures that the number of events in `max_poll_records` can be safely processed within the time limit.

```
EXAMPLE
Pipeline throughput is `10k/s` and `max_poll_records` is set to 1k =>. The value
must be at least 100ms if `consumer_threads` is set to `1`. If it is set to a
higher value `n`, then the minimum session timeout increases proportionally to
`n * 100ms`.
```

In practice the value must be set much higher than the theoretical value because the behavior of the outputs and filters in a pipeline follows a distribution. The value should also be higher than the maximum time you expect your outputs to stall. The default setting is `10s == 10000ms`. If you are experiencing periodic problems with an output that can stall because of load or similar effects (such as the Elasticsearch output), there is little downside to increasing this value significantly to say `60s`.

From a performance perspective, decreasing the `max_poll_records` value is preferable to increasing the timeout value. Increasing the timeout is your only option if the client’s issues are caused by periodically stalling outputs. Check logs for evidence of stalling outputs, such as `ES output logging status 429`.


#### Kafka input plugin crashes when using schema registry [ts-schema-registry]

By default, the kafka input plugin checks connectivity and validates the schema registry during plugin registration before events are processed. In some circumstances, this process may fail when it tries to validate an authenticated schema registry, causing the plugin to crash.

The plugin offers a `schema_registry_validation` setting to change the default behavior. This setting allows the plugin to skip validation during registration, which allows the plugin to continue and events to be processed. See the [kafka input plugin documentation](https://www.elastic.co/guide/en/logstash/current/plugins-inputs-kafka.html#plugins-inputs-kafka-schema_registry_validation) for more information about the plugin and other configuration options.

::::{note}
An incorrectly configured schema registry will still stop the plugin from processing events.
::::


::::{note}
The default setting of `auto` is the best option for most circumstances and should not need to be changed.
::::



#### Large number of offset commits (input) [ts-kafka-many-offset-commits]

**Symptoms**

Logstash’s Kafka Input is causing a much higher number of commits to the offset topic than expected. Often the complaint also mentions redundant offset commits where the same offset is committed repeatedly.

**Solution**

For Kafka Broker versions 0.10.2.1 to 1.0.x: The problem is caused by a bug in Kafka. [https://issues.apache.org/jira/browse/KAFKA-6362](https://issues.apache.org/jira/browse/KAFKA-6362) The client’s best option is upgrading their Kafka Brokers to version 1.1 or newer.

For older versions of Kafka or if the above does not fully resolve the issue: The problem can also be caused by setting the value for `poll_timeout_ms` too low relative to the rate at which the Kafka Brokers receive events themselves (or if Brokers periodically idle between receiving bursts of events). Increasing the value set for `poll_timeout_ms` proportionally decreases the number of offsets commits in this scenario. For example, raising it by 10x will lead to 10x fewer offset commits.


#### Codec Errors in Kafka Input (before Plugin Version 6.3.4 only) [ts-kafka-codec-errors-input]

**Symptoms**

Logstash Kafka input randomly logs errors from the configured codec and/or reads events incorrectly (partial reads, mixing data between multiple events etc.).

```
Log example:  [2018-02-05T13:51:25,773][FATAL][logstash.runner          ] An
unexpected error occurred! {:error=>#<TypeError: can't convert nil into String>,
:backtrace=>["org/jruby/RubyArray.java:1892:in `join'",
"org/jruby/RubyArray.java:1898:in `join'",
"/usr/share/logstash/logstash-core/lib/logstash/util/buftok.rb:87:in `extract'",
"/usr/share/logstash/vendor/bundle/jruby/1.9/gems/logstash-codec-line-3.0.8/lib/logstash/codecs/line.rb:38:in
`decode'",
"/usr/share/logstash/vendor/bundle/jruby/1.9/gems/logstash-input-kafka-5.1.11/lib/logstash/inputs/kafka.rb:241:in
`thread_runner'",
"file:/usr/share/logstash/vendor/jruby/lib/jruby.jar!/jruby/java/java_ext/java.lang.rb:12:in
`each'",
"/usr/share/logstash/vendor/bundle/jruby/1.9/gems/logstash-input-kafka-5.1.11/lib/logstash/inputs/kafka.rb:240:in
`thread_runner'"]}
```

**Background**

There was a bug in the way the Kafka Input plugin was handling codec instances when running on multiple threads (`consumer_threads` set to > 1). [https://github.com/logstash-plugins/logstash-input-kafka/issues/210](https://github.com/logstash-plugins/logstash-input-kafka/issues/210)

**Solution**

* Upgrade Kafka Input plugin to v. 6.3.4 or later.
* If (and only if) upgrading is not possible, set `consumer_threads` to `1`.


#### Setting up debugging for Kerberos SASL [ts-kafka-kerberos-debug]

You can set up your machine to help you troubleshoot authentication failures in the Kafka client.

* In `config/jvm.options`, add:

    ```txt
    -Dsun.security.krb5.debug=true
    ```

* In `config/log4j2.properties`, add:

    ```txt
    logger.kafkainput.name = logstash.inputs.kafka
    logger.kafkainput.level = debug
    logger.kafkaoutput.name = logstash.outputs.kafka
    logger.kafkaoutput.level = debug
    logger.kafka.name = org.apache.kafka
    logger.kafka.level = debug
    ```


::::{note}
Logging entries for Kerberos are NOT sent through Log4j but go directly to the console.
::::



## Azure Event Hub issues and solutions [ts-azure]


#### Event Hub plugin can’t connect to Storage blob (input) [ts-azure-http]

**Symptoms**

Azure EventHub can’t connect to blob storage:

```
[2024-01-01T13:13:13,123][ERROR][com.microsoft.azure.eventprocessorhost.AzureStorageCheckpointLeaseManager][azure_eventhub_pipeline][eh_input_plugin] host logstash-a0a00a00-0aa0-0000-aaaa-0a00a0a0aaaa: Failure while creating lease store
com.microsoft.azure.storage.StorageException: The client could not finish the operation within specified maximum execution timeout.
```

Plugin can’t complete registration phase because it can’t connect to Azure Blob Storage configured in the plugin `storage_connection` setting.

**Background**

Azure Event Hub plugin can share the offset position of a consumer group with other consumers only if Blob Storage connection settings are configured. EventHub uses the AMQP protocol to transfer data, but Blob storage uses a library which leverages the JDK’s http client, `HttpURLConnection`. To troubleshoot HTTP connection problems, which may be related to proxy settings, the logging level for this part of the JDK has to be increased. The problem is that JDK uses Java Util Logging for its internal logging needs, which is not configurable with the standard `log4j2.properties` shipped with {{ls}}.

**Possible solutions**

* Configure {{ls}} settings to enable the JDK logging.

**Details**

Steps to enable JDK logging on {{ls}}:

* Create a properties file with the logging definitions for Java Util Logging (JUL).
* Configure a JVM property to inform JUL to use such definitions file.

**JUL definitions**

Create a file that you can use to define logging levels, handlers and loggers. For example, `<LS_HOME>/conf/jul.properties`.

```txt
handlers= java.util.logging.ConsoleHandler,java.util.logging.FileHandler
.level= ALL
java.util.logging.FileHandler.pattern = <USER's LOGS FOLDER>/logs/jul_http%u.log <1>
java.util.logging.FileHandler.limit = 50000
java.util.logging.FileHandler.count = 1
java.util.logging.FileHandler.level=ALL
java.util.logging.FileHandler.maxLocks = 100
java.util.logging.FileHandler.formatter = java.util.logging.SimpleFormatter

java.util.logging.ConsoleHandler.level = INFO
java.util.logging.ConsoleHandler.formatter = java.util.logging.SimpleFormatter

# defines the logger we are interested in
sun.net.www.protocol.http.HttpURLConnection.level = ALL <2>
```

1. The log file will be created in a path defined by the user (`<USER's LOGS FOLDER>/logs/`)
2. This configuration enables the `sun.net.www.protocol.http.HttpURLConnection` logger, and sets the logging level to `ALL`. It will log all messages directed to it, from highest to lowest priority.


**JVM property**

To inform the JUL framework of the selected definitions file a property (`java.util.logging.config.file`) has to be evaluated, this is where {{ls}}'s `config/jvm.properties` come in handy. Edit the file adding the property, pointing to the path where the JUL definitions file was created:

```txt
-Djava.util.logging.config.file=<LS_HOME>/conf/jul.properties
```

The logs could contain sensible information, such credentials, and could be verbose but should give hits on the connection problem at HTTP level with the Azure Blob Storage.


## Other issues [ts-other]

Coming soon, and you can help! If you have something to add, please:

* create an issue at [https://github.com/elastic/logstash/issues](https://github.com/elastic/logstash/issues), or
* create a pull request with your proposed changes at [https://github.com/elastic/logstash](https://github.com/elastic/logstash).

Also check out the [Logstash discussion forum](https://discuss.elastic.co/c/logstash).

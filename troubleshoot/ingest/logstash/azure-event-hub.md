---
navigation_title: "Azure Event Hub"
mapped_pages:
  - https://www.elastic.co/guide/en/logstash/current/ts-plugins.html#ts-azure
---

# Troubleshoot Logstash plugin for Azure Event Hub [ts-azure]

## Event Hub plugin can’t connect to Storage blob (input) [ts-azure-http]

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



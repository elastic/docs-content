---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/application-logs.html
  - https://www.elastic.co/guide/en/serverless/current/observability-correlate-application-logs.html
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
  - id: cloud-serverless
---

# Send application log data [observability-correlate-application-logs]

Application logs provide valuable insight into events that have occurred within your services and applications.

The format of your logs (structured or plaintext) influences your log ingestion strategy.


## Plaintext logs versus structured Elastic Common Schema (ECS) logs [observability-correlate-application-logs-plaintext-logs-vs-structured-elastic-common-schema-ecs-logs]

Logs are typically produced as either plaintext or structured. Plaintext logs contain only text and have no special formatting, for example:

```txt
2019-08-06T12:09:12.375Z INFO:spring-petclinic: Tomcat started on port(s): 8080 (http) with context path, org.springframework.boot.web.embedded.tomcat.TomcatWebServer
2019-08-06T12:09:12.379Z INFO:spring-petclinic: Started PetClinicApplication in 7.095 seconds (JVM running for 9.082), org.springframework.samples.petclinic.PetClinicApplication
2019-08-06T14:08:40.199Z DEBUG:spring-petclinic: init find form, org.springframework.samples.petclinic.owner.OwnerController
```

Structured logs follow a predefined, repeatable pattern or structure. This structure is applied at write time, preventing the need for parsing at ingest time. The Elastic Common Schema (ECS) defines a common set of fields to use when structuring logs. This structure allows logs to be ingested, and provides the ability to correlate, search, and aggregate on individual fields within your logs.

For example, the previous example logs might look like this when structured with ECS-compatible JSON:

```json
{"@timestamp":"2019-08-06T12:09:12.375Z", "log.level": "INFO", "message":"Tomcat started on port(s): 8080 (http) with context path ''", "service.name":"spring-petclinic","process.thread.name":"restartedMain","log.logger":"org.springframework.boot.web.embedded.tomcat.TomcatWebServer"}
{"@timestamp":"2019-08-06T12:09:12.379Z", "log.level": "INFO", "message":"Started PetClinicApplication in 7.095 seconds (JVM running for 9.082)", "service.name":"spring-petclinic","process.thread.name":"restartedMain","log.logger":"org.springframework.samples.petclinic.PetClinicApplication"}
{"@timestamp":"2019-08-06T14:08:40.199Z", "log.level":"DEBUG", "message":"init find form", "service.name":"spring-petclinic","process.thread.name":"http-nio-8080-exec-8","log.logger":"org.springframework.samples.petclinic.owner.OwnerController","transaction.id":"28b7fb8d5aba51f1","trace.id":"2869b25b5469590610fea49ac04af7da"}
```


## Ingesting logs [observability-correlate-application-logs-ingesting-logs]

There are several ways to ingest application logs into your project. Your specific situation helps determine the method that’s right for you.


### Plaintext logs [observability-correlate-application-logs-plaintext-logs]

With {{filebeat}} or {{agent}}, you can ingest plaintext logs, including existing logs, from any programming language or framework without modifying your application or its configuration.

For plaintext logs to be useful, you need to use {{filebeat}} or {{agent}} to parse the log data.

**![documentation icon](/solutions/images/serverless-documentation.svg "") Learn more in [Plaintext logs](/solutions/observability/logs/plaintext-application-logs.md)**


### ECS formatted logs [observability-correlate-application-logs-ecs-formatted-logs]

Logs formatted in ECS don’t require manual parsing and the configuration can be reused across applications. They also include log correlation. You can format your logs in ECS by using ECS logging plugins or {{apm-agent}} ECS reformatting.


#### ECS logging plugins [observability-correlate-application-logs-ecs-logging-plugins]

Add ECS logging plugins to your logging libraries to format your logs into ECS-compatible JSON that doesn’t require parsing.

To use ECS logging, you need to modify your application and its log configuration.

**![documentation icon](/solutions/images/serverless-documentation.svg "") Learn more in [ECS formatted logs](/solutions/observability/logs/ecs-formatted-application-logs.md)**


#### {{apm-agent}} log reformatting [observability-correlate-application-logs-apm-agent-log-reformatting]

Some Elastic {{apm-agent}}s can automatically reformat application logs to ECS format without adding an ECS logger dependency or modifying the application.

This feature is supported for the following {{apm-agent}}s:

* [Ruby](apm-agent-ruby://reference/configuration.md#config-log-ecs-formatting)
* [Python](apm-agent-python://reference/logs.md#log-reformatting)
* [Java](apm-agent-java://reference/logs.md#log-reformatting)

**![documentation icon](/solutions/images/serverless-documentation.svg "") Learn more in [ECS formatted logs](/solutions/observability/logs/ecs-formatted-application-logs.md)**


### {{apm-agent}} log sending [observability-correlate-application-logs-apm-agent-log-sending]

Automatically capture and send logs directly to the managed intake service using the {{apm-agent}} without using {{filebeat}} or {{agent}}.

Log sending is supported in the Java {{apm-agent}}.

**![documentation icon](/solutions/images/serverless-documentation.svg "") Learn more in [{{apm-agent}} log sending](/solutions/observability/logs/apm-agent-log-sending.md)**


## Log correlation [observability-correlate-application-logs-log-correlation]

Correlate your application logs with trace events to:

* See the context of a log and the parameters provided by a user
* See all logs belonging to a particular trace
* Move between logs and traces when debugging application issues

Learn more about log correlation in the agent-specific ingestion guides:

::::{tab-set}

:::{tab-item} OpenTelemetry (EDOT)

The {{edot}} (EDOT) provides SDKs for multiple programming languages with built-in support for log correlation:

* [Java](elastic-otel-java://reference/edot-java/index.md)
* [.NET](elastic-otel-dotnet://reference/edot-dotnet/index.md)
* [Node.js](elastic-otel-node://reference/edot-node/index.md)
* [PHP](elastic-otel-php://reference/edot-php/index.md)
* [Python](elastic-otel-python://reference/edot-python/index.md)

For more information about EDOT, refer to [Elastic Distribution of OpenTelemetry (EDOT)](opentelemetry://reference/index.md).

:::

:::{tab-item} APM Agents
:name: apm-agents

Elastic APM agents provide log correlation capabilities for the following languages:

* [Go](apm-agent-go://reference/logs.md)
* [Java](apm-agent-java://reference/logs.md#log-correlation-ids)
* [.NET](apm-agent-dotnet://reference/logs.md)
* [Node.js](apm-agent-nodejs://reference/logs.md)
* [Python](apm-agent-python://reference/logs.md#log-correlation-ids)
* [Ruby](apm-agent-ruby://reference/logs.md)

:::

::::
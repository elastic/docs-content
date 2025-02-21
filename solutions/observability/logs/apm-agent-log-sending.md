---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/logs-send-application.html
  - https://www.elastic.co/guide/en/serverless/current/observability-send-application-logs.html
---

# APM agent log sending [observability-send-application-logs]

Elastic APM agents can automatically capture and send logs directly to the managed intake service — enabling you to easily ingest log events without needing a separate log shipper like {{filebeat}} or {{agent}}.

**Supported APM agents/languages**

* Java

**Requirements**

The Elastic APM agent for Java.

**Pros**

* Simple to set up as it only relies on the APM agent.
* No modification of the application required.
* No need to deploy {{filebeat}}.
* No need to store log files in the file system.

**Cons**

* Experimental feature.
* Limited APM agent support.
* Not resilient to outages. Log messages can be dropped when buffered in the agent or in the managed intake service.


## Get started [observability-send-application-logs-get-started]

See the [Java agent](asciidocalypse://docs/apm-agent-java/docs/reference/ingestion-tools/apm-agent-java/logs.md#log-sending) documentation to get started.
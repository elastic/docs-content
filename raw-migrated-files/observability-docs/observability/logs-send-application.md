# {{apm-agent}} log sending [logs-send-application]

The Java APM agent can automatically capture and send logs directly to the managed intake service — enabling you to easily ingest log events without needing a separate log shipper like {{filebeat}}.

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


## Get started [get-started]

See the [Java agent](https://www.elastic.co/guide/en/apm/agent/java/current/logs.html#log-sending) documentation to get started.

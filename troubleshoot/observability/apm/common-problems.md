---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-common-problems.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-troubleshooting.html
---

# Common problems [apm-common-problems]

This section describes common problems you might encounter when using APM Server and the Applications UI in {{kib}}.

**APM Server**:

* [No data is indexed](#apm-no-data-indexed)
* [Common SSL-related problems](#apm-common-ssl-problems)
* [I/O Timeout](#apm-io-timeout)
* [Field limit exceeded](#apm-field-limit-exceeded)
* [Tail-based sampling causing high system memory usage and high disk IO](#apm-tail-based-sampling-memory-disk-io)

**Applications UI**:

* [Too many unique transaction names](#troubleshooting-too-many-transactions)
* [Unknown route](#troubleshooting-unknown-route)
* [Fields are not searchable](#troubleshooting-fields-unsearchable)
* [Service Maps: no connection between client and server](#service-map-rum-connections)
* [No data shown in the infrastructure tab](#troubleshooting-apm-infra-data)


## No data is indexed [apm-no-data-indexed]
```yaml {applies_to}
stack: all
```

If no data shows up in {{es}}, first make sure that your APM components are properly connected.

:::::::{tab-set}

::::::{tab-item} Fleet-managed
**Is {{agent}} healthy?**

In {{kib}} open **{{fleet}}** and find the host that is running the APM integration; confirm that its status is **Healthy**. If it isn’t, check the {{agent}} logs to diagnose potential causes. See [Monitor {{agent}}s](https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html) to learn more.

**Is APM Server happy?**

In {{kib}}, open **{{fleet}}** and select the host that is running the APM integration. Open the **Logs** tab and select the `elastic_agent.apm_server` dataset. Look for any APM Server errors that could help diagnose the problem.

**Can the {{apm-agent}} connect to APM Server**

To determine if the {{apm-agent}} can connect to the APM Server, send requests to the instrumented service and look for lines containing `[request]` in the APM Server logs.

If no requests are logged, confirm that:

1. SSL isn’t [misconfigured](#apm-ssl-client-fails).
2. The host is correct. For example, if you’re using Docker, ensure a bind to the right interface (for example, set `apm-server.host = 0.0.0.0:8200` to match any IP) and set the `SERVER_URL` setting in the {{apm-agent}} accordingly.

If you see requests coming through the APM Server but they are not accepted (a response code other than `202`), see [APM Server response codes](apm-server-response-codes.md) to narrow down the possible causes.

**Instrumentation gaps**

APM agents provide auto-instrumentation for many popular frameworks and libraries. If the {{apm-agent}} is not auto-instrumenting something that you were expecting, data won’t be sent to the {{stack}}. Reference the relevant [{{apm-agent}} documentation](https://www.elastic.co/guide/en/apm/agent/index.html) for details on what is automatically instrumented.
::::::

::::::{tab-item} APM Server binary
If no data shows up in {{es}}, first check that the APM components are properly connected.

To ensure that APM Server configuration is valid and it can connect to the configured output, {{es}} by default, run the following commands:

```sh
apm-server test config
apm-server test output
```

To see if the agent can connect to the APM Server, send requests to the instrumented service and look for lines containing `[request]` in the APM Server logs.

If no requests are logged, it might be that SSL is [misconfigured](#apm-ssl-client-fails) or that the host is wrong. Particularly, if you are using Docker, ensure to bind to the right interface (for example, set `apm-server.host = 0.0.0.0:8200` to match any IP) and set the `SERVER_URL` setting in the agent accordingly.

If you see requests coming through the APM Server but they are not accepted (response code other than `202`), consider the response code to narrow down the possible causes (see sections below).

Another reason for data not showing up is that the agent is not auto-instrumenting something you were expecting, check the [agent documentation](https://www.elastic.co/guide/en/apm/agent/index.html) for details on what is automatically instrumented.

APM Server currently relies on {{es}} to create indices that do not exist. As a result, {{es}} must be configured to allow [automatic index creation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) for APM indices.
::::::

:::::::

## Common SSL-related problems [apm-common-ssl-problems]
```yaml {applies_to}
stack: all
```

* [SSL client fails to connect](#apm-ssl-client-fails)
* [x509: cannot validate certificate](#apm-cannot-validate-certificate)
* [getsockopt: no route to host](#apm-getsockopt-no-route-to-host)
* [getsockopt: connection refused](#apm-getsockopt-connection-refused)
* [No connection could be made because the target machine actively refused it](#apm-target-machine-refused-connection)


### SSL client fails to connect [apm-ssl-client-fails]

The target host might be unreachable or the certificate may not be valid. To fix this problem:

1. Make sure that the APM Server process on the target host is running and you can connect to it. Try to ping the target host to verify that you can reach it from the host running APM Server. Then use either `nc` or `telnet` to make sure that the port is available. For example:

    ```shell
    ping <hostname or IP>
    telnet <hostname or IP> 5044
    ```

2. Verify that the certificate is valid and that the hostname and IP match.
3. Use OpenSSL to test connectivity to the target server and diagnose problems. See the [OpenSSL documentation](https://www.openssl.org/docs/manmaster/man1/openssl-s_client.md) for more info.


### x509: cannot validate certificate for <IP address> because it doesn’t contain any IP SANs [apm-cannot-validate-certificate]

This happens because your certificate is only valid for the hostname present in the Subject field. To resolve this problem, try one of these solutions:

* Create a DNS entry for the hostname, mapping it to the server’s IP.
* Create an entry in `/etc/hosts` for the hostname. Or, on Windows, add an entry to `C:\Windows\System32\drivers\etc\hosts`.
* Re-create the server certificate and add a Subject Alternative Name (SAN) for the IP address of the server. This makes the server’s certificate valid for both the hostname and the IP address.


### getsockopt: no route to host [apm-getsockopt-no-route-to-host]

This is not an SSL problem. It’s a networking problem. Make sure the two hosts can communicate.


### getsockopt: connection refused [apm-getsockopt-connection-refused]

This is not an SSL problem. Make sure that {{ls}} is running and that there is no firewall blocking the traffic.


### No connection could be made because the target machine actively refused it [apm-target-machine-refused-connection]

A firewall is refusing the connection. Check if a firewall is blocking the traffic on the client, the network, or the destination host.


## I/O Timeout [apm-io-timeout]
```yaml {applies_to}
stack: all
```

I/O Timeouts can occur when your timeout settings across the stack are not configured correctly, especially when using a load balancer.

You may see an error like the one below in the {{apm-agent}} logs, and/or a similar error on the APM Server side:

```txt
[ElasticAPM] APM Server responded with an error:
"read tcp 123.34.22.313:8200->123.34.22.40:41602: i/o timeout"
```

To fix this, ensure timeouts are incrementing from the {{apm-agent}}, through your load balancer, to the APM Server.

By default, the agent timeouts are set at 10 seconds, and the server timeout is set at 3600 seconds. Your load balancer should be set somewhere between these numbers.

For example:

```txt
APM agent --> Load Balancer  --> APM Server
   10s            15s               3600s
```

The APM Server timeout can be configured by updating the [maximum duration for reading an entire request](../../../solutions/observability/apps/general-configuration-options.md#apm-read_timeout).


## Field limit exceeded [apm-field-limit-exceeded]

When adding too many distinct tag keys on a transaction or span, you risk creating a [mapping explosion](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings).

For example, you should avoid that user-specified data, like URL parameters, is used as a tag key. Likewise, using the current timestamp or a user ID as a tag key is not a good idea. However, tag **values** with a high cardinality are not a problem. Just try to keep the number of distinct tag keys at a minimum.

The symptom of a mapping explosion is that transactions and spans are not indexed anymore after a certain time. Usually, on the next day, the spans and transactions will be indexed again because a new index is created each day. But as soon as the field limit is reached, indexing stops again.

In the agent logs, you won’t see a sign of failures as the APM server asynchronously sends the data it received from the agents to {{es}}. However, the APM server and {{es}} log a warning like this:

```txt
{\"type\":\"illegal_argument_exception\",\"reason\":\"Limit of total fields [1000] in [INDEX_NAME] has been exceeded\"}
```


## Tail-based sampling causing high system memory usage and high disk IO [apm-tail-based-sampling-memory-disk-io]
```yaml {applies_to}
stack: all
```

Tail-based sampling requires minimal memory to run, and there should not be a noticeable increase in RSS memory usage. However, since tail-based sampling writes data to disk, it is possible to see a significant increase in OS page cache memory usage due to disk IO. If you see a drop in throughput and excessive disk activity after enabling tail-based sampling, please ensure that there is enough memory headroom in the system for OS page cache to perform disk IO efficiently.


## Too many unique transaction names [troubleshooting-too-many-transactions]
```yaml {applies_to}
stack: all
```

Transaction names are defined in each APM agent; when an APM agent supports a framework, it includes logic for naming the transactions that the framework creates. In some cases though, like when using an APM agent’s API to create custom transactions, it is up to the user to define a pattern for transaction naming. When transactions are named incorrectly, each unique URL can be associated with a unique transaction group—causing an explosion in the number of transaction groups per service, and leading to inaccuracies in the Applications UI.

To fix a large number of unique transaction names, you need to change how you are using the APM agent API to name your transactions. To do this, ensure you are **not** naming based on parameters that can change. For example, user ids, product ids, order numbers, query parameters, etc., should be stripped away, and commonality should be found between your unique URLs.

Let’s look at an example from the RUM agent documentation. Here are a few URLs you might find on Elastic.co:

```yaml
// Blog Posts
https://www.elastic.co/blog/reflections-on-three-years-in-the-elastic-public-sector
https://www.elastic.co/blog/say-heya-to-the-elastic-search-awards
https://www.elastic.co/blog/and-the-winner-of-the-elasticon-2018-training-subscription-drawing-is

// Documentation
https://www.elastic.co/guide/en/elastic-stack/current/index.html
https://www.elastic.co/guide/en/apm/get-started/current/index.html
https://www.elastic.co/guide/en/infrastructure/guide/current/index.html
```

These URLs, like most, include unique names. If we named transactions based on each unique URL, we’d end up with the problem described above—a very large number of different transaction names. Instead, we should strip away the unique information and group our transactions based on common information. In this case, that means naming all blog transactions, `/blog`, and all documentation transactions, `/guide`.

If you feel like you’d be losing valuable information by following this naming convention, don’t fret! You can always add additional metadata to your transactions using [labels](/solutions/observability/apps/metadata.md#apm-data-model-labels) (indexed) or [custom context](/solutions/observability/apps/metadata.md#apm-data-model-custom) (non-indexed).

After ensuring you’ve correctly named your transactions, you might still see errors in the Applications UI related to transaction group limit reached:

`The number of transaction groups has been reached. Current APM server capacity for handling unique transaction groups has been reached. There are at least X transactions missing in this list. Please decrease the number of transaction groups in your service or increase the memory allocated to APM server.`

You will see this warning if an agent is creating too many transaction groups. This could indicate incorrect instrumentation which will have to be fixed in your application. Alternatively you can increase the memory of the APM server.

`Number of transaction groups exceed the allowed maximum(1,000) that are displayed. The maximum number of transaction groups displayed in Kibana has been reached. Try narrowing down results by using the query bar..`

You will see this warning if your results have more than `1000` unique transaction groups. Alternatively you can use the query bar to reduce the number of unique transaction groups in your results.

**More information**

While this can happen with any APM agent, it typically occurs with the RUM agent. For more information on how to correctly set `transaction.name` in the RUM agent, see [custom initial page load transaction names](https://www.elastic.co/guide/en/apm/agent/rum-js/current/custom-transaction-name.html).

The RUM agent can also set the `transaction.name` when observing for transaction events. See [`apm.observe()`](https://www.elastic.co/guide/en/apm/agent/rum-js/current/agent-api.html#observe) for more information.

If your problem is occurring in a different APM agent, the tips above still apply. See the relevant [Agent API documentation](https://www.elastic.co/guide/en/apm/agent) to adjust how you’re naming your transactions.


## Unknown route [troubleshooting-unknown-route]
```yaml {applies_to}
stack: all
```

The [transaction overview](../../../solutions/observability/apps/transactions-2.md) will only display helpful information when the transactions in your services are named correctly. If you’re seeing "GET unknown route" or "unknown route" in the Applications UI, it could be a sign that something isn’t working as it should.

Elastic APM agents come with built-in support for popular frameworks out-of-the-box. This means, among other things, that the APM agent will try to automatically name HTTP requests. As an example, the Node.js agent uses the route that handled the request, while the Java agent uses the Servlet name.

"Unknown route" indicates that the APM agent can’t determine what to name the request, perhaps because the technology you’re using isn’t supported, the agent has been installed incorrectly, or because something is happening to the request that the agent doesn’t understand.

To resolve this, you’ll need to head over to the relevant [APM agent documentation](https://www.elastic.co/guide/en/apm/agent). Specifically, view the agent’s supported technologies page. You can also use the agent’s public API to manually set a name for the transaction.


## Fields are not searchable [troubleshooting-fields-unsearchable]
```yaml {applies_to}
stack: all
```

In Elasticsearch, index templates are used to define settings and mappings that determine how fields should be analyzed. The recommended index templates for APM come from the built-in {{es}} apm-data plugin. These templates, by default, enable and disable indexing on certain fields.

As an example, some APM agents store cookie values in `http.request.cookies`. Since `http.request` has disabled dynamic indexing, and `http.request.cookies` is not declared in a custom mapping, the values in `http.request.cookies` are not indexed and thus not searchable.

**Ensure an APM data view exists** As a first step, you should ensure the correct data view exists. In {{kib}}, go to **Stack Management** > **Data views**. You should see the APM data view—​the default is `traces-apm*,apm-*,logs-apm*,apm-*,metrics-apm*,apm-*`. If you don’t, the data view doesn’t exist. To fix this, navigate to the Applications UI in {{kib}} and select **Add data**. In the APM tutorial, click **Load Kibana objects** to create the APM data view.

**Ensure a field is searchable** There are two things you can do to if you’d like to ensure a field is searchable:

1. Index your additional data as [labels](/solutions/observability/apps/metadata.md) instead. These are dynamic by default, which means they will be indexed and become searchable and aggregatable.
2. Create a custom mapping for the field.


## Service Maps: no connection between client and server [service-map-rum-connections]
```yaml {applies_to}
stack: all
```

If the service map is not showing an expected connection between the client and server, it’s likely because you haven’t configured [`distributedTracingOrigins`](https://www.elastic.co/guide/en/apm/agent/rum-js/current/distributed-tracing-guide.html).

This setting is necessary, for example, for cross-origin requests. If you have a basic web application that provides data via an API on `localhost:4000`, and serves HTML from `localhost:4001`, you’d need to set `distributedTracingOrigins: ['https://localhost:4000']` to ensure the origin is monitored as a part of distributed tracing. In other words, `distributedTracingOrigins` is consulted prior to the APM agent adding the distributed tracing `traceparent` header to each request.


## No data shown in the infrastructure tab [troubleshooting-apm-infra-data]
```yaml {applies_to}
stack: all
```

If you don’t see any data in the **Infrastructure** tab for a selected service in the Applications UI, there are a few possible causes and solutions.

**If you also do *not* see the data in the** [**Infrastructure inventory**](../../../solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md)

Refer to the [Infrastructure troubleshooting docs](../troubleshooting-infrastructure-monitoring.md).

**If you *do* see the data in the** [**Infrastructure inventory**](../../../solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md)

It’s likely that there is a problem correlating APM and infrastructure data. The `host.hostname` field value in the APM data and the `host.name` field value in infrastructure data are used to correlate data, and the queries used to correlate the data are case sensitive.

To fix this, make sure these two fields match exactly.

For example, if the APM agent is not configured to use the correct host name, the host name might be set to the container name or the Kubernetes pod name. To get the correct host name, you need to set some additional configuration options, specifically `system.kubernetes.node.name` as described in [Kubernetes data](../../../solutions/observability/apps/elastic-apm-events-intake-api.md#apm-api-kubernetes-data).


## Common response codes [observability-apm-troubleshooting-common-response-codes]
```yaml {applies_to}
serverless: all
```


### HTTP 400: Data decoding error / Data validation error [bad-request]

The most likely cause for this error is using an incompatible version of an {{apm-agent}}. See [minimum supported APM agent versions](../../../solutions/observability/apps/elastic-apm-agents.md#observability-apm-agents-elastic-apm-agents-minimum-supported-versions) to verify compatibility.


### HTTP 400: Event too large [event-too-large]

APM agents communicate with the Managed intake service by sending events in an HTTP request. Each event is sent as its own line in the HTTP request body. If events are too large, you can reduce the size of the events that your APM agents send by: [enabling span compression](../../../solutions/observability/apps/spans.md) or [reducing collected stack trace information](../../../solutions/observability/apps/reduce-storage.md#observability-apm-reduce-stacktrace).


### HTTP 401: Invalid token [unauthorized]

The API key is invalid.


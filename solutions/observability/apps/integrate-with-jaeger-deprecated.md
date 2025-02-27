---
navigation_title: "Jaeger (deprecated)"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-jaeger-integration.html
applies_to:
  stack: all
---



# Integrate with Jaeger (deprecated) [apm-jaeger-integration]


::::{warning}
Support for Jaeger is deprecated and will be removed in a future version of Elastic APM. [Jaeger clients are deprecated](https://www.jaegertracing.io/docs/1.35/client-libraries/) in favor of OpenTelemetry SDKs, and OpenTelemetry has removed all Jaeger exporters from their [specification](https://github.com/open-telemetry/opentelemetry-specification/pull/2858).
::::


Elastic APM integrates with [Jaeger](https://www.jaegertracing.io/), an open-source, distributed tracing system. This integration allows users with an existing Jaeger setup to switch from the default Jaeger backend, to the {{stack}}. Best of all, no instrumentation changes are needed in your application code.


## Supported architecture [apm-jaeger-architecture]

Jaeger architecture supports different data formats and transport protocols that define how data can be sent to a collector. Elastic APM, as a Jaeger collector, supports communication with **Jaeger agents** via gRPC.

* The APM integration serves Jaeger gRPC over the same host and port as the Elastic {{apm-agent}} protocol.
* The APM integration gRPC endpoint supports TLS. If SSL is configured, SSL settings will automatically be applied to the APM integration’s Jaeger gRPC endpoint.
* The gRPC endpoint supports probabilistic sampling. Sampling decisions can be configured [centrally](#apm-configure-sampling-central-jaeger) with {{apm-agent}} central configuration, or [locally](#apm-configure-sampling-local-jaeger) in each Jaeger client.

See the [Jaeger docs](https://www.jaegertracing.io/docs/1.27/architecture) for more information on Jaeger architecture.


## Get started [apm-get-started-jaeger]

Connect your preexisting Jaeger setup to Elastic APM in three steps:

* [Configure Jaeger agents](#apm-configure-agent-client-jaeger)
* [Configure Sampling](#apm-configure-sampling-jaeger)
* [Start sending data](#apm-configure-start-jaeger)

::::{important}
There are [caveats](#apm-caveats-jaeger) to this integration.
::::



### Configure Jaeger agents [apm-configure-agent-client-jaeger]

The APM integration serves Jaeger gRPC over the same host and port as the Elastic {{apm-agent}} protocol.

:::::::{tab-set}

::::::{tab-item} {{ecloud}}
1. Log into [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body) and select your deployment.
2. In {{kib}}, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Select **Elastic APM**. If the integration is already installed, under the polices tab, select **Actions** > **Edit integration**. If the integration has not been installed, select **Add Elastic APM**. Copy the URL. If you’re using Agent authorization, copy the Secret token as well.
4. Configure the APM Integration as a collector for your Jaeger agents.

    As of this writing, the Jaeger agent binary offers the following CLI flags, which can be used to enable TLS, output to {{ecloud}}, and set the APM Integration secret token:

    ```bash
    --reporter.grpc.tls.enabled=true
    --reporter.grpc.host-port=<apm-url:443>
    --agent.tags="elastic-apm-auth=Bearer <secret-token>"
    ```


::::{tip}
For the equivalent environment variables, change all letters to upper-case and replace punctuation with underscores (`_`). See the [Jaeger CLI flags documentation](https://www.jaegertracing.io/docs/1.27/cli/) for more information.
::::
::::::

::::::{tab-item} Self-managed
1. Configure the APM Integration as a collector for your Jaeger agents. In {{kib}}, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Elastic APM**. If the integration is already installed, under the polices tab, select **Actions** > **Edit integration**. If the integration has not been installed, select **Add Elastic APM**. Copy the Host. If you’re using Agent authorization, copy the Secret token as well.

    As of this writing, the Jaeger agent binary offers the `--reporter.grpc.host-port` CLI flag. Use this to define the host and port that the APM Integration is listening on:

    ```bash
    --reporter.grpc.host-port=<apm-endpoint:8200>
    ```

2. (Optional) Enable encryption

    When TLS is enabled for the APM Integration, Jaeger agents must also enable TLS communication:

    ```bash
    --reporter.grpc.tls.enabled=true
    ```

3. (Optional) Enable token-based authorization

    A secret token or API key can be used to ensure only authorized Jaeger agents can send data to the APM Integration. When enabled, use an agent level tag to authorize Jaeger agent communication with the APM Server:

    ```bash
    --agent.tags="elastic-apm-auth=Bearer <secret-token>"
    ```


::::{tip}
For the equivalent environment variables, change all letters to upper-case and replace punctuation with underscores (`_`). See the [Jaeger CLI flags documentation](https://www.jaegertracing.io/docs/1.27/cli/) for more information.
::::
::::::

:::::::

### Configure Sampling [apm-configure-sampling-jaeger]

The APM integration supports probabilistic sampling, which can be used to reduce the amount of data that your agents collect and send. Probabilistic sampling makes a random sampling decision based on the configured sampling value. For example, a value of `.2` means that 20% of traces will be sampled.

There are two different ways to configure the sampling rate of your Jaeger agents:

* [{{apm-agent}} central configuration (default)](#apm-configure-sampling-central-jaeger)
* [Local sampling in each Jaeger client](#apm-configure-sampling-local-jaeger)


#### {{apm-agent}} central configuration (default) [apm-configure-sampling-central-jaeger]

Central sampling, with {{apm-agent}} central configuration, allows Jaeger clients to poll APM Server for the sampling rate. This means sample rates can be configured on the fly, on a per-service and per-environment basis. See [Central configuration](apm-agent-central-configuration.md) to learn more.


#### Local sampling in each Jaeger client [apm-configure-sampling-local-jaeger]

If you don’t have access to the Applications UI, you’ll need to change the Jaeger client’s `sampler.type` and `sampler.param`. This enables you to set the sampling configuration locally in each Jaeger client. See the official [Jaeger sampling documentation](https://www.jaegertracing.io/docs/1.27/sampling/) for more information.


### Start sending data [apm-configure-start-jaeger]

That’s it! Data sent from Jaeger clients to the APM Server can now be viewed in the Applications UI.


## Caveats [apm-caveats-jaeger]

There are some limitations and differences between Elastic APM and Jaeger that you should be aware of.

**Jaeger integration limitations:**

* Because Jaeger has its own trace context header, and does not currently support W3C trace context headers, it is not possible to mix and match the use of Elastic’s APM agents and Jaeger’s clients.
* Elastic APM only supports probabilistic sampling.

**Differences between APM Agents and Jaeger Clients:**

* Jaeger clients only sends trace data. APM agents support a larger number of features, like multiple types of metrics, and application breakdown charts. When using Jaeger, features like this will not be available in the Applications UI.
* Elastic APM’s [Learn about data types](learn-about-application-data-types.md) is different than Jaegers. For Jaeger trace data to work with Elastic’s data model, we rely on spans being tagged with the appropriate [`span.kind`](https://github.com/opentracing/specification/blob/master/semantic_conventions.md).

    * Server Jaeger spans are mapped to Elastic APM [Transactions](transactions.md).
    * Client Jaeger spans are mapped to Elastic APM [Spans](spans.md) — unless the span is the root, in which case it is mapped to an Elastic APM [Transactions](transactions.md).

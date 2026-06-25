---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-open-telemetry-direct.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-agents-opentelemetry-opentelemetry-native-support.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Contrib OpenTelemetry Collectors and language SDKs [apm-open-telemetry-direct]

The {{stack}} natively supports the OpenTelemetry protocol (OTLP). This means logs, metrics, and trace data collected from your applications and infrastructure can be sent directly to the {{stack}}.

* Send data to Elastic from a contrib [OpenTelemetry Collector](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md#apm-connect-open-telemetry-collector)
* Send data to Elastic from a contrib [OpenTelemetry language SDK](/solutions/observability/apm/opentelemetry/upstream-opentelemetry-collectors-language-sdks.md#apm-instrument-apps-otel)

To compare approaches and choose the best one for your use case, refer to [OpenTelemetry](/solutions/observability/apm/opentelemetry/index.md).

::::{important}
The {{product.edot-collector}} (EDOT Collector) includes additional features and configurations to seamlessly integrate with Elastic. Refer to [EDOT compared to contrib OpenTelemetry](opentelemetry://reference/compatibility/edot-vs-upstream.md) for a comparison.
::::

## Send data from a contrib OpenTelemetry Collector [apm-connect-open-telemetry-collector]

Connect your OpenTelemetry Collector instances to Elastic {{observability}} or {{obs-serverless}} using the OTLP exporter:

::::{applies-switch}

:::{applies-item} stack:

```yaml
receivers: <1>
  # ...
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
processors: <2>
  # ...
  memory_limiter:
    check_interval: 1s
    limit_mib: 2000
  batch:

exporters:
  debug:
    verbosity: detailed <3>
  otlp: <4>
    # Elastic endpoint without the "https://" prefix
    endpoint: "${env:ELASTIC_OTLP_ENDPOINT}" <5> <7>
    headers:
      # Elastic secret token (for API key, use the ApiKey prefix)
      Authorization: "Bearer ${env:ELASTIC_SECRET_TOKEN}" <6> <7>

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [debug, otlp]
    metrics:
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [debug, otlp]
    logs: <8>
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [debug, otlp]
```

1. The receivers, like the [OTLP receiver](https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver), that forward data emitted by OpenTelemetry SDKs, or the [host metrics receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver).
2. Use the [Batch processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md) and the [memory limiter processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md). For more information, refer to [recommended processors](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md#recommended-processors).
3. The [debug exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/debugexporter) is helpful for troubleshooting, and supports configurable verbosity levels: `basic` (default), `normal`, and `detailed`.
4. Elastic endpoint configuration. Elastic supports a ProtoBuf payload via both the OTLP protocol over gRPC transport [(OTLP/gRPC)](https://opentelemetry.io/docs/specs/otlp/#otlpgrpc) and the OTLP protocol over HTTP transport [(OTLP/HTTP)](https://opentelemetry.io/docs/specs/otlp/#otlphttp). To learn more about these exporters, refer to the OpenTelemetry Collector documentation: [OTLP/HTTP Exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter) or [OTLP/gRPC exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter). When adding an endpoint to an existing configuration an optional name component can be added, like `otlp/elastic`, to distinguish endpoints as described in the [OpenTelemetry Collector Configuration Basics](https://opentelemetry.io/docs/collector/configuration/#basics).
5. Hostname and port of the Elastic endpoint. For self-managed deployments, use the address of your [EDOT Collector in gateway mode](elastic-agent://reference/edot-collector/modes.md) (for example, `edot-collector:4317` for gRPC or `edot-collector:4318` for HTTP). For {{ech}}, use the [Managed OTLP endpoint](opentelemetry://reference/motlp/index.md).
6. Credential for Elastic [secret token authorization](/solutions/observability/apm/secret-token.md) (`Authorization: "Bearer a_secret_token"`) or [API key authorization](/solutions/observability/apm/api-keys.md) (`Authorization: "ApiKey an_api_key"`).
7. Environment-specific configuration parameters can be conveniently passed in as environment variables documented in the [OpenTelemetry Collector environment variables reference](https://opentelemetry.io/docs/collector/configuration/#environment-variables) (for example, `ELASTIC_OTLP_ENDPOINT` and `ELASTIC_SECRET_TOKEN`).
8. To send OpenTelemetry logs to {{stack}} version 8.0+, declare a `logs` pipeline. {applies_to}`stack: preview`

:::

:::{applies-item} serverless:

```yaml
receivers:   <1>
  # ...
  otlp:

processors:   <2>
  # ...
  memory_limiter:
    check_interval: 1s
    limit_mib: 2000
  batch:

exporters:
  logging:
    loglevel: warn   <3>
  otlp/elastic:   <4>
    # Elastic endpoint without the "https://" prefix
    endpoint: "${ELASTIC_OTLP_ENDPOINT}" <5> <7>
    headers:
      # Elastic API key
      Authorization: "ApiKey ${ELASTIC_API_KEY}" <6> <7>

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [logging, otlp/elastic]
    metrics:
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [logging, otlp/elastic]
    logs:   <8>
      receivers: [otlp]
      processors: [..., memory_limiter, batch]
      exporters: [logging, otlp/elastic]
```

1. The receivers, like the [OTLP receiver](https://github.com/open-telemetry/opentelemetry-collector/tree/main/receiver/otlpreceiver), that forward data emitted by OpenTelemetry SDKs, or the [host metrics receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/receiver/hostmetricsreceiver).
2. We recommend using the [Batch processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md) and the [memory limiter processor](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/memorylimiterprocessor/README.md). For more information, refer to [recommended processors](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/README.md#recommended-processors).
3. The [logging exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/loggingexporter) is helpful for troubleshooting and supports various logging levels, like `debug`, `info`, `warn`, and `error`.
4. {{obs-serverless}} endpoint configuration. Elastic supports a ProtoBuf payload via both the OTLP protocol over gRPC transport [(OTLP/gRPC)](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md#otlpgrpc) and the OTLP protocol over HTTP transport [(OTLP/HTTP)](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md#otlphttp). To learn more about these exporters, refer to the OpenTelemetry Collector documentation: [OTLP/HTTP Exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter) or [OTLP/gRPC exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter).
5. URL of the [Managed OTLP endpoint](opentelemetry://reference/motlp/index.md). Find your endpoint URL in the {{serverless-full}} project settings.
6. Credential for Elastic API key authorization (`Authorization: "ApiKey an_api_key"`).
7. Environment-specific configuration parameters can be conveniently passed in as environment variables documented in the [OpenTelemetry Collector environment variables reference](https://opentelemetry.io/docs/collector/configuration/#configuration-environment-variables) (for example, `ELASTIC_OTLP_ENDPOINT` and `ELASTIC_API_KEY`).
8. To send OpenTelemetry logs to your project, declare a `logs` pipeline. {applies_to}`serverless: preview`

:::

::::

You’re now ready to export traces and metrics from your services and applications.

::::{important}
When using the OpenTelemetry Collector, send data through the [`OTLP` exporter](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlphttpexporter). Using other methods, like the [`elasticsearch` exporter](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/elasticsearchexporter), bypasses all the validation and data processing that Elastic performs. Also, your data will not be viewable in your {{observability}} project if you use the `elasticsearch` exporter.
::::

## Send data from a contrib OpenTelemetry SDK [apm-instrument-apps-otel]

::::{note}
The following instructions show how to send data directly from an OpenTelemetry SDK to Elastic, which is appropriate when getting started. However, sending data from an OpenTelemetry SDK to the OpenTelemetry Collector is preferred, as the Collector processes and exports data to Elastic. Read more about when and how to use a collector in the [OpenTelemetry documentation](https://opentelemetry.io/docs/collector/#when-to-use-a-collector).
::::

To export traces and metrics to Elastic, instrument your services and applications with the OpenTelemetry API, SDK, or both. For example, if you are a Java developer, you need to instrument your Java app with the [OpenTelemetry agent for Java](https://github.com/open-telemetry/opentelemetry-java-instrumentation). Refer to the [OpenTelemetry Instrumentation guides](https://opentelemetry.io/docs/instrumentation/) to download the OpenTelemetry agent or SDK for your language.

Define environment variables to configure the OpenTelemetry agent or SDK and enable communication with Elastic. For example, if you are instrumenting a Java app, define the following environment variables:

::::{applies-switch}

:::{applies-item} stack:

```bash
export OTEL_RESOURCE_ATTRIBUTES=service.name=checkoutService,service.version=1.1,deployment.environment=production
export OTEL_EXPORTER_OTLP_ENDPOINT=https://elastic-endpoint:4318
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer a_secret_token"
export OTEL_METRICS_EXPORTER="otlp" \
export OTEL_LOGS_EXPORTER="otlp" \ <1>
java -javaagent:/path/to/opentelemetry-javaagent-all.jar \
     -classpath lib/*:classes/ \
     com.mycompany.checkout.CheckoutServiceServer
```

1. The OpenTelemetry logs intake through Elastic is in technical preview. {applies_to}`stack: preview`

`OTEL_RESOURCE_ATTRIBUTES`
:   Fields that describe the service and the environment that the service runs in. Refer to [attributes](/solutions/observability/apm/opentelemetry/attributes.md) for more information.

`OTEL_EXPORTER_OTLP_ENDPOINT`
:   Elastic endpoint URL. For self-managed deployments, use the address of your EDOT Collector or {{apm-server}} OTLP endpoint. For {{ech}}, use the [Managed OTLP endpoint](opentelemetry://reference/motlp/index.md).

`OTEL_EXPORTER_OTLP_HEADERS`
:   Authorization header that includes the Elastic secret token or API key: `"Authorization=Bearer a_secret_token"` or `"Authorization=ApiKey an_api_key"`.

    For information on how to format an API key, refer to [API keys](/solutions/observability/apm/api-keys.md).

    Note the required space between `Bearer` and `a_secret_token`, and `ApiKey` and `an_api_key`.

    ::::{note}
    If you are using a version of the Python OpenTelemetry agent *earlier than* 1.27.0, the content of the header *must* be URL-encoded. You can use the Python standard library’s `urllib.parse.quote` function to encode the content of the header.
    ::::

`OTEL_METRICS_EXPORTER`
:   Metrics exporter to use. Refer to [exporter selection](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection) for more information.

`OTEL_LOGS_EXPORTER`
:   Logs exporter to use. Refer to [exporter selection](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection) for more information.

:::

:::{applies-item} serverless:

```bash
export OTEL_RESOURCE_ATTRIBUTES=service.name=checkoutService,service.version=1.1,deployment.environment=production
export OTEL_EXPORTER_OTLP_ENDPOINT=https://your-motlp-endpoint:443
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey an_api_key"
export OTEL_METRICS_EXPORTER="otlp" \
export OTEL_LOGS_EXPORTER="otlp" \   <1>
java -javaagent:/path/to/opentelemetry-javaagent-all.jar \
     -classpath lib/*:classes/ \
     com.mycompany.checkout.CheckoutServiceServer
```

1. The OpenTelemetry logs intake through Elastic is in technical preview. {applies_to}`serverless: preview`

`OTEL_RESOURCE_ATTRIBUTES`
:   Fields that describe the service and the environment that the service runs in. Refer to [attributes](/solutions/observability/apm/opentelemetry/attributes.md) for more information.

`OTEL_EXPORTER_OTLP_ENDPOINT`
:   Elastic endpoint URL. The URL of the [Managed OTLP endpoint](opentelemetry://reference/motlp/index.md).

`OTEL_EXPORTER_OTLP_HEADERS`
:   Authorization header that includes the Elastic API key: `"Authorization=ApiKey an_api_key"`. Note the required space between `ApiKey` and `an_api_key`.

    For information on how to format an API key, refer to [API keys](/solutions/observability/apm/api-keys.md).

    ::::{note}
    If you are using a version of the Python OpenTelemetry agent *earlier than* 1.27.0, the content of the header *must* be URL-encoded. You can use the Python standard library’s `urllib.parse.quote` function to encode the content of the header.

    ::::

`OTEL_METRICS_EXPORTER`
:   Metrics exporter to use. Refer to [exporter selection](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection) for more information.

`OTEL_LOGS_EXPORTER`
:   Logs exporter to use. Refer to [exporter selection](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/#exporter-selection) for more information.

:::

::::

You are now ready to collect traces and [metrics](/solutions/observability/apm/opentelemetry/collect-metrics.md), and then [verify](/solutions/observability/apm/opentelemetry/collect-metrics.md#apm-open-telemetry-verify-metrics) and [visualize](/solutions/observability/apm/opentelemetry/collect-metrics.md#apm-open-telemetry-visualize) them.

## Proxy requests to {{apm-server}} [apm-open-telemetry-proxy-apm]

```{applies_to}
stack: ga
```

:::{note}
For new users, Elastic recommends sending OpenTelemetry data to the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) or [Managed OTLP endpoint](opentelemetry://reference/motlp.md) instead of to the {{apm-server}}.
:::

{{apm-server}} supports both the [OTLP/gRPC](https://opentelemetry.io/docs/specs/otlp/#otlpgrpc) and [OTLP/HTTP](https://opentelemetry.io/docs/specs/otlp/#otlphttp) protocol on the same port as Elastic {{apm-agent}} requests. For ease of setup, use OTLP/HTTP when proxying or load balancing requests to Elastic.

If you use the OTLP/gRPC protocol, requests to Elastic must use either HTTP/2 over TLS or HTTP/2 Cleartext (H2C). No matter which protocol is used, OTLP/gRPC requests will have the `"Content-Type: application/grpc"` header.

When using a layer 7 (L7) proxy like {{aws}} ALB, proxy the requests in a way that ensures they follow the rules outlined previously. For example, with ALB you can create rules to select an alternative backend protocol based on the headers of requests coming into ALB. In this example, you’d select the gRPC protocol when the  `"Content-Type: application/grpc"` header exists on a request.

Many L7 load balancers handle HTTP and gRPC traffic separately and rely on explicitly defined routes and service configurations to correctly proxy requests. Since {{apm-server}} serves both protocols on the same port, it may not be compatible with some L7 load balancers. For example, to work around this issue in [Ingress NGINX Controller for {{k8s}}](https://github.com/kubernetes/ingress-nginx), either:

* Use the `otlp` exporter in the EDOT collector. Set annotation `nginx.ingress.kubernetes.io/backend-protocol: "GRPC"` on the K8s Ingress object proxying to {{apm-server}}.
* Use the `otlphttp` exporter in the EDOT collector. Set annotation `nginx.ingress.kubernetes.io/backend-protocol: "HTTP"` (or `"HTTPS"` if {{apm-server}} expects TLS) on the K8s Ingress object proxying to {{apm-server}}.

The preferred approach is to deploy a L4 (TCP) load balancer (for example, [NLB](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html) on {{aws}}) in front of {{apm-server}}, which forwards raw TCP traffic transparently without protocol inspection.

For more information on how to configure an {{aws}} ALB to support gRPC, refer to this {{aws}} blog post: [Application Load Balancer Support for End-to-End HTTP/2 and gRPC](https://aws.amazon.com/blogs/aws/new-application-load-balancer-support-for-end-to-end-http-2-and-grpc/).

For more information on how {{apm-server}} services gRPC requests, refer to [Muxing gRPC and HTTP/1.1](https://github.com/elastic/apm-server/blob/main/dev_docs/otel.md#muxing-grpc-and-http11).

:::{include} /solutions/observability/apm/_snippets/apm-server-vs-mis.md
:::

## Next steps [apm-open-telemetry-direct-next]

* [Collect metrics](/solutions/observability/apm/opentelemetry/collect-metrics.md)
* Add [resource attributes](/solutions/observability/apm/opentelemetry/attributes.md)
* Learn about the [limitations of this integration](/solutions/observability/apm/opentelemetry/limitations.md)

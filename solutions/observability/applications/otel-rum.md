---
navigation_title: OpenTelemetry for Real User Monitoring (RUM)
description: Instrument web applications with OpenTelemetry for Real User Monitoring using Elastic Observability.
applies_to:
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# OpenTelemetry for Real User Monitoring (RUM)

:::{important}
Using OpenTelemetry for Real User Monitoring (RUM) with {{product.observability}} is currently in **Technical Preview**. This feature is provided as-is and has [limitations](#known-limitations). It should not be used in production environments. Elastic provides best-effort support for Technical Preview features and they are not covered under standard SLAs.
:::

This documentation outlines the process for instrumenting your web application with OpenTelemetry browser instrumentation, using {{product.observability}} as the backend. Unlike the [EDOT SDKs](opentelemetry://reference/edot-sdks/index.md), this approach uses upstream OpenTelemetry JavaScript packages directly. The following sections detail the required components and their proper configuration to acquire traces, logs, and metrics from the application to visualize them within {{kib}}.

While this guide uses upstream OpenTelemetry instrumentation, you can also use the [EDOT Collector](elastic-agent://reference/edot-collector/index.md) components as part of your data ingestion pipeline.

## Prerequisites

This guide assumes you're using an {{product.observability}} deployment. You can use an existing one or set up a new one. If you're new to {{product.observability}}, follow the guidelines in [Get started with {{product.observability}}](/solutions/observability/get-started.md).

:::{warning}
Avoid using OpenTelemetry alongside any other {{apm-agent}}, including Elastic {{product.apm}} agents. Running multiple agents in the same application process might lead to conflicting instrumentation, duplicate telemetry, or other unexpected behavior.
:::

### OTLP endpoint

You need a OTLP endpoint in order to ingest data from the OpenTelemetry RUM instrumentation. Also if you want to get the most of {{product.observability}} such endpoint should belong to an [EDOT Collector](elastic-agent://reference/edot-collector/index.md) in gateway mode. If you're setting up a new deployment, you can create an {{ecloud}} hosted deployment or {{serverless-short}} project, which includes the [{{motlp}}](opentelemetry://reference/motlp.md). If you own a self hosted stack or your deployment does not have the {{motlp}} you should configure an [EDOT Collector in Gateway mode](https://www.elastic.co/docs/reference/edot-collector/modes#edot-collector-as-gateway).

Once you have your OTLP endpoint ready the recommendation is to set up a reverse proxy to forward the telemetry from your web application origin to the collector. The primary reasons for having such set up are:

- EDOT Collector requires an `Authorization` header with an ApiKey in order to accept OTLP exports. Setting up the required key in a web application makes it publicly available and its not advised to have this kind of secrets available to anyone with a browser.
- You can apply rate limiting or any other mechanisms to control traffic before it reaches the EDOT Collector.
- If you have set up your own EDOT Collector it's likely to have a different origin than your web application. In this scenario you will have to set up [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) for the web application in EDOT Collector configuration file. This procerdure can be cumbersome if you have to manage a large numned of applications.


The following snippet shows the configuration for an NGINX reverse proxy to forward all telemetry to the EDOT Collector located at `collector.example.com` from the origin `webapp.example.com`:

```nginx
server {
    # Configuration for HTTP/HTTPS goes here
    location / {
        # Take care of preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always; # Set te allowed origins
            add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always; # Set te allowed origins
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Authorization 'ApiKey ...your Elastic API key...'; # Set the auth header here. It's recommended to get it from a secrets manager.
        proxy_pass https://collector.example.com:4318;
    }
}
```

## Installation

OpenTelemetry packages for web instrumentation are published to npm. You can install them with the package manager of your choice.

The following packages hold the necessary components to set up the base for your instrumentations:

```bash
npm install @opentelemetry/api @opentelemetry/core @opentelemetry/resources @opentelemetry/sdk-trace-base @opentelemetry/sdk-trace-web @opentelemetry/exporter-trace-otlp-http @opentelemetry/instrumentation
```

You can then install the instrumentations that you're interested in.

## Basic configuration

The minimal configuration you need to instrument your web application with OpenTelemetry includes:

- **OTEL_EXPORTER_OTLP_ENDPOINT**: The full URL of the proxy you have configured in the [OTLP endpoint](#otlp-endpoint) section.
- **OTEL_RESOURCE_ATTRIBUTES**: A JavaScript object that will be used to define the resource. The most important attributes to define are:
  - `service.name` (string): Name of the application you're instrumenting.
  - `service.version` (string, optional): A string representing the version or build of your app.
  - `deployment.environment.name` (string, optional): Name of the environment where the app runs (if applicable); for example, "prod", "dev", or "staging".
- **OTEL_LOG_LEVEL**: Use this configuration to set the log level of the OpenTelemetry components you're going to use.

## Set up OpenTelemetry for the browser

To begin instrumenting your web application with OpenTelemetry in the browser, you need a script. This script configures the essential components, including the context manager, signal providers, processors, and exporters. After setting up the script, you can register the installed instrumentations so they can observe your application and send traces, metrics, and logs to your designated endpoint.

The following start script is in plain JavaScript. If you are using TypeScript, you can adapt this script by changing the file extension to `.ts` and adding the necessary type definitions. OpenTelemetry packages are written in TypeScript, so they include the appropriate type definitions.

:::{note}
Each signal configuration is independent of the others, meaning that you can configure only what you need. The OpenTelemetry API defaults to no-op providers for traces, metrics, and logs.
:::

::::::{stepper}

:::::{step} Set the configuration

First, set the configuration options that are to be used by all the signals and the instrumentation code. Also initialize the internal logger at the level defined in the configuration.

For this part, you need to install the following dependencies:

- `@opentelemetry/api`: All the packages are included. Each signal configuration uses it to register the providers for each signal.
- `@opentelemetry/core`: Contains core types and some utilities for the rest of the packages. It parses strings to the correct type.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/api @opentelemetry/core
```

After the dependencies are installed, configure the following options:

:::{dropdown} Configuration example

```javascript
import { diag, DiagConsoleLogger } from '@opentelemetry/api';
import { diagLogLevelFromString } from '@opentelemetry/core';

// Set the configuration options
const OTEL_LOG_LEVEL = 'info'; // Possible values: error, warn, info, debug, verbose
const OTEL_EXPORTER_OTLP_ENDPOINT = 'https://proxy.example.com'; // Point to your reverse proxy configured in the section above
const OTEL_RESOURCE_ATTRIBUTES = {
  'service.name': 'my-web-app',
  'service.version': '1.2.3',
  'deployment.environment.name': 'qa',
  // You can add other attributes
};

// Set the log level for the OTEL components
// You can raise the level to "debug" if you want more details
diag.setLogger(
  new DiagConsoleLogger(),
  { logLevel: diagLogLevelFromString(OTEL_LOG_LEVEL) },
);
diag.info('OTEL bootstrap', config);
```

:::

:::::

:::::{step} Define the resource

A resource is an entity that generates telemetry, with its characteristics captured in resource attributes. An example is a web application operating within a browser that produces telemetry data. Further details are available in [OpenTelemetry Resources](https://opentelemetry.io/docs/concepts/resources/).

A standardized set of attributes is specified in [Browser resource semantic conventions](https://opentelemetry.io/docs/specs/semconv/resource/browser/), which can be included alongside those outlined in the configuration section. OpenTelemetry offers resource detectors like `browserDetector` to help set these attributes like brands, mobile, and platform.

To define the resource, install the following dependencies:

- `@opentelemetry/resources`: This package helps you to define and work with resources because a Resource is not a plain object and has some properties (like immutability) and constraints.
- `@opentelemetry/browser-detector`: Detectors help you to define a resource by querying the runtime and environment and resolving some attributes. In this case, the browser detector resolves the language, brands, and mobile attributes of the browser namespace.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/resources @opentelemetry/browser-detector
```

After the dependencies are installed, define the resource for your instrumentation with the following code:

```javascript
import { resourceFromAttributes, detectResources } from '@opentelemetry/resources';
import { browserDetector } from '@opentelemetry/opentelemetry-browser-detector';

const detectedResources = detectResources({ detectors: [browserDetector] });
let resource = resourceFromAttributes(OTEL_RESOURCE_ATTRIBUTES);
resource = resource.merge(detectedResources);
```

Having this information on spans and errors is useful in diagnostic situations for identifying application and dependency compatibility issues with certain browsers.

:::::

:::::{step} Configure trace

To enable instrumentations to transmit traces and allow for the creation of custom spans through the OpenTelemetry API, a [TracerProvider](https://opentelemetry.io/docs/concepts/signals/traces/#tracer-provider) must be configured. This provider necessitates the inclusion of several key components:

- **Resource**: The resource to be associated with the spans created by the tracers (previously defined).
- **Span Processor**: A component that manages the spans generated by the tracers and forwards them to a [SpanExporter](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter). The exporter should be configured to direct data to an endpoint designated for traces.
- **Span Exporter**: Manages the transmission of spans to the Collector.
- **Context Manager**: A crucial mechanism for managing the active Span context across asynchronous operations and threads. It ensures that when a new Span is created, it correctly identifies its parent Span, thereby maintaining the integrity of the trace structure.

For this part, you need to install the following dependencies:

- `@opentelemetry/sdk-trace-base`: This package contains all the core components to set up tracing regardless of the runtime they're running in (Node.js or browser).
- `@opentelemetry/sdk-trace-web`: This package contains a tracer provider that runs in web browsers.
- `@opentelemetry/exporter-trace-otlp-http`: This package contains the exporter for the HTTP/JSON protocol.
- `@opentelemetry/context-zone`: This package contains a context manager which uses on [zone.js](https://www.npmjs.com/package/zone.js) library.

```bash
npm install @opentelemetry/sdk-trace-base\
      @opentelemetry/sdk-trace-web\
      @opentelemetry/exporter-trace-otlp-http\
      @opentelemetry/context-zone
```

Once the dependencies are installed, you can configure and register a tracer provider with the following code:

:::{dropdown} Tracer provider configuration

```javascript
import { trace } from '@opentelemetry/api';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';

// Set the traces endpoint based on the config provided
const tracesEndpoint = `${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/traces`;

// Set the tracer provider for instrumentations and calls to the API to start and end spans
const tracerProvider = new WebTracerProvider({
  resource,  // All spans will be associated with this resource
  spanProcessors: [
    new BatchSpanProcessor(new OTLPTraceExporter({
      url: tracesEndpoint,
    })),
  ],
});
tracerProvider.register({ contextManager: new ZoneContextManager() });
```

:::

Now you can use the OpenTelemetry API to get a tracer and start creating your own spans. Instrumentations can also do it after you register them.

:::::

:::::{step} Configure metrics

Similar to traces, you should configure a [MeterProvider](https://opentelemetry.io/docs/concepts/signals/metrics/#meter-provider) for metrics. This provider necessitates the inclusion of several key components:

- **Resource**: The resource to be associated with the metrics created by the meters.
- **Metric Reader**: Used to determine how often metrics are collected and what destination they should be exported to. In this case, we will use a `PeriodicExportingMetricReader` configured to collect and export metrics at a fixed interval.
- **Metric Exporter**: Responsible for serializing and sending the collected and aggregated metric data to a backend observability platform. We will use the OTLP/HTTP exporter.

For this part, you need to install the following dependencies:

- `@opentelemetry/sdk-metrics`: This package contains all the required components to set up metrics.
- `@opentelemetry/exporter-metrics-otlp-http`: This package contains the exporter for the HTTP/JSON protocol.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/sdk-metrics @opentelemetry/exporter-metrics-otlp-http
```

After the dependencies are installed, configure and register a meter provider with the following code:

:::{dropdown} Meter provider configuration

```javascript
import { metrics } from '@opentelemetry/api';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';

// Set the metrics endpoint based on the config provided
const metricsEndpoint = `${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/metrics`;

// Create metric reader to process metrics and export using OTLP
const metricReader = new PeriodicExportingMetricReader({
  exporter: new OTLPMetricExporter({ url: metricsEndpoint }),
});

// Create meter provider to send metrics
const meterProvider = new MeterProvider({
  resource: resource,  // All metrics will be associated with this resource
  readers: [metricReader],
});
metrics.setGlobalMeterProvider(meterProvider);
```

:::

:::::

:::::{step} Configure logs

Like traces and metrics you need to configure a [LoggerProvider](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider) if you want to record relevant events that are happening in your application via API or instrumenations. This provider necessitates the inclusion of several key components:

- **Resource**: The resource to be associated with the log records created by the loggers.
- **LogRecord Processor**: A component that manages the log records generated by the loggers and forwards them to a [LogExporter](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter). The exporter should be configured to direct data to an endpoint designated for logs.
- **Log Exporter**: Manages the transmission of log records to the Collector.



For this part, you need to install the following dependencies:

- `@opentelemetry/api-logs`: This package contains the logs API. This API is not included yet in the generic API package because logs are still experimental.
- `@opentelemetry/sdk-logs`: This package contains all the required components to set up logs.
- `@opentelemetry/exporter-logs-otlp-http`: This package contains the exporter for the HTTP/JSON protocol.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/api-logs @opentelemetry/sdk-logs @opentelemetry/exporter-logs-otlp-http
```

After the dependencies are installed, you can configure and register a logger provider with the following code:

:::{dropdown} Logger provider configuration

```javascript
import { logs, SeverityNumber } from '@opentelemetry/api-logs';
import { BatchLogRecordProcessor, LoggerProvider } from '@opentelemetry/sdk-logs';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';

// Set the logs endpoint based on the config provided
const logsEndpoint = `${OTEL_EXPORTER_OTLP_ENDPOINT}/v1/logs`;

// Configure logging to send to the Collector
const logExporter = new OTLPLogExporter({ url: logsEndpoint });

const loggerProvider = new LoggerProvider({
  resource: resource,
  processors: [new BatchLogRecordProcessor(logExporter)]
});
logs.setGlobalLoggerProvider(loggerProvider);
```

:::

:::::

:::::{step} Register instrumentations

The final step for setting up Real User Monitoring (RUM) through OpenTelemetry is registering instrumentations. Instrumentations are modules that automatically capture telemetry data, like network requests or DOM interactions, by using the OpenTelemetry API.

With the OpenTelemetry SDK, resource attributes, and exporters already configured, all telemetry data generated by these registered instrumentations is automatically processed and exported.

Install the following dependencies:

- `@opentelemetry/instrumentation`: This package contains the core components of instrumentations along with some utilities.
- `@opentelemetry/instrumentation-document-load`: This instrumentation package measures the time it took the document to load and also the load timings of its resources. More info at [instrumentation-document-load](https://www.npmjs.com/package/@opentelemetry/instrumentation-document-load).
- `@opentelemetry/instrumentation-long-task`: This instrumentation gathers information about long tasks being executed in your browser, helping to spot issues like unresponsive UI in your web application. More info at [instrumentation-long-task](https://www.npmjs.com/package/@opentelemetry/instrumentation-long-task).
- `@opentelemetry/instrumentation-fetch`: This instrumentation keeps track of your web application requests made through the Fetch API. More info at [instrumentation-fetch](https://www.npmjs.com/package/@opentelemetry/instrumentation-fetch).
- `@opentelemetry/instrumentation-xml-http-request`: This instrumentation keeps track of your web application requests made through the XMLHttpRequest API. More info at [instrumentation-xml-http-request](https://www.npmjs.com/package/@opentelemetry/instrumentation-xml-http-request).
- `@opentelemetry/instrumentation-user-interaction`: This instrumentation measures user interactions in your web application. More info at [instrumentation-user-interaction](https://www.npmjs.com/package/@opentelemetry/instrumentation-user-interaction).

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/instrumentation\
      @opentelemetry/instrumentation-document-load\
      @opentelemetry/instrumentation-long-task\
      @opentelemetry/instrumentation-fetch\
      @opentelemetry/instrumentation-xml-http-request\
      @opentelemetry/instrumentation-user-interaction
```

After the dependencies are installed, you can configure and register instrumentations with the following code:

:::{dropdown} Instrumentations registration

```javascript
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { LongTaskInstrumentation } from '@opentelemetry/instrumentation-long-task';
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction'
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';

// Register instrumentations
registerInstrumentations({
  instrumentations: [
    new DocumentLoadInstrumentation(),
    new LongTaskInstrumentation(),
    new FetchInstrumentation(),
    new XMLHttpRequestInstrumentation(),
    new UserInteractionInstrumentation(),
  ],
});
```

:::

:::::

:::::{step} Complete setup script

All these pieces together give you a complete setup of all the signals for your web site or application. For conveninence its better to have it in a separate file which can be named `telemetry.js`. This file should export a function that accepts the configuration allowing you to reuse the setup across different UIs.

To install all the dependencies needed for the complete setup, run the following command:

```bash
npm install @opentelemetry/api\
      @opentelemetry/core\
      @opentelemetry/resources\
      @opentelemetry/browser-detector\
      @opentelemetry/sdk-trace-base\
      @opentelemetry/sdk-trace-web\
      @opentelemetry/context-zone\
      @opentelemetry/exporter-trace-otlp-http\
      @opentelemetry/sdk-metrics\
      @opentelemetry/exporter-metrics-otlp-http\
      @opentelemetry/api-logs\
      @opentelemetry/sdk-logs\
      @opentelemetry/exporter-logs-otlp-http\
      @opentelemetry/instrumentation\
      @opentelemetry/instrumentation-document-load\
      @opentelemetry/instrumentation-long-task\
      @opentelemetry/instrumentation-fetch\
      @opentelemetry/instrumentation-xml-http-request\
      @opentelemetry/instrumentation-user-interaction
```

After the dependencies are installed, you can wrap the setup in a function with the following code:

:::{dropdown} Complete setup script example

```javascript
// file: telemetry.js
import { diag, DiagConsoleLogger, trace, metrics } from '@opentelemetry/api';
import { diagLogLevelFromString } from '@opentelemetry/core';
import { resourceFromAttributes, detectResources } from '@opentelemetry/resources';
import { browserDetector } from '@opentelemetry/opentelemetry-browser-detector';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { WebTracerProvider } from '@opentelemetry/sdk-trace-web';
import { MeterProvider, PeriodicExportingMetricReader } from '@opentelemetry/sdk-metrics';
import { OTLPMetricExporter } from '@opentelemetry/exporter-metrics-otlp-http';
import { logs, SeverityNumber } from '@opentelemetry/api-logs';
import { BatchLogRecordProcessor, LoggerProvider } from '@opentelemetry/sdk-logs';
import { OTLPLogExporter } from '@opentelemetry/exporter-logs-otlp-http';
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { DocumentLoadInstrumentation } from '@opentelemetry/instrumentation-document-load';
import { FetchInstrumentation } from '@opentelemetry/instrumentation-fetch';
import { LongTaskInstrumentation } from '@opentelemetry/instrumentation-long-task';
import { UserInteractionInstrumentation } from '@opentelemetry/instrumentation-user-interaction';
import { XMLHttpRequestInstrumentation } from '@opentelemetry/instrumentation-xml-http-request';

const initDone = Symbol('OTEL initialized');

// Expected properties of the config object:
// - logLevel
// - endpoint
// - resourceAttributes
export function initOpenTelemetry(config) {
  // To avoid multiple calls
  if (window[initDone]) {
    return;
  }
  window[initDone] = true;
  diag.setLogger(
    new DiagConsoleLogger(),
    { logLevel: diagLogLevelFromString(config.logLevel) },
  );
  diag.info('OTEL bootstrap', config);

  // Resource definition
  const detectedResources = detectResources({ detectors: [browserDetector] });
  const resource = resourceFromAttributes(config.resourceAttributes)
                              .merge(detectedResources);

  // Trace signal setup
  const tracesEndpoint = `${config.endpoint}/v1/traces`;
  const tracerProvider = new WebTracerProvider({
    resource,
    spanProcessors: [
      new BatchSpanProcessor(new OTLPTraceExporter({
        url: tracesEndpoint,
      })),
    ],
  });
  tracerProvider.register({ contextManager: new ZoneContextManager() })

  // Metrics signal setup
  const metricsEndpoint = `${config.endpoint}/v1/metrics`;
  const metricReader = new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({ url: metricsEndpoint }),
  });
  const meterProvider = new MeterProvider({
    resource: resource,
    readers: [metricReader],
  });
  metrics.setGlobalMeterProvider(meterProvider);

  // Logs signal setup
  const logsEndpoint = `${config.endpoint}/v1/logs`;
  const logExporter = new OTLPLogExporter({ url: logsEndpoint });

  const loggerProvider = new LoggerProvider({
    resource: resource,
    processors: [new BatchLogRecordProcessor(logExporter)]
  });
  logs.setGlobalLoggerProvider(loggerProvider);

  // Register instrumentations
  registerInstrumentations({
    instrumentations: [
      new DocumentLoadInstrumentation(),
      new LongTaskInstrumentation(),
      new FetchInstrumentation(),
      new XMLHttpRequestInstrumentation(),
      new UserInteractionInstrumentation(),
    ],
  });
}
```

:::

:::::

::::::

## Integrate with your application

With the setup placed in a file, it's time to apply it to your web application. You can choose from two main approaches:

1. **Import the code**: Use your build tooling to manage the dependencies and integrate the code into the application bundle. This is the simplest option and is recommended, although it increases the size of your application bundle.

2. **Bundle in a file**: Use a bundler to generate a separate JavaScript file that you include in the `<head>` section of your HTML page. This approach keeps the telemetry code separate from your application bundle.

### Import the code

This approach is recommended. The build tooling manages the dependencies and integrates the code into the application bundle. This might increase the size of your application bundle.

For example, if you're using Webpack, you can import the code like this:

:::{dropdown} Example: Import telemetry.js in your app

```javascript
// file: app.(js|ts) entry point of your application
import { initOpenTelemetry } from 'telemetry.js';

initOpenTelemetry({
  logLevel: 'info',
  endpoint: 'https://proxy.example.com',
  resourceAttributes: {
    'service.name': 'my-web-app',
    'service.version': '1',
  }
});

// Your app code
```

:::

### Bundle in a file

You can use a bundler to generate a separate JavaScript file. Place the file within the application's assets folder and include it in the `<head>` section of the HTML page. 

Assuming the JavaScript files reside in a folder named "js", the HTML file structure looks like this:

:::{dropdown} HTML example

```html
<!doctype html>
<html>
  <head>
    <script src="./js/telemetry-bundle.js"></script>
    <script>
      initOpenTelemetry({
        logLevel: 'info',
        endpoint: 'https://host:port/',
        resourceAttributes: {
          'service.name': 'my-web-app',
          'service.version': '1',
        }
      });
    </script>
    …
  </head>
  <body>
    <!-- app HTML content -->
  </body>
</html>
```

:::

## Manual instrumentation to extend your telemetry

Automatic instrumentation provides a convenient baseline for web application telemetry, but often lacks the necessary depth to fully understand complex user journeys or correlate technical performance with business outcomes.

The OpenTelemetry API is essential for filling this gap. By using the OpenTelemetry API directly, you can send highly specific, custom telemetry to augment automatic collection. This custom instrumentation allows you to:

1. **Define custom spans and traces**: Create explicit spans around unique critical business logic or user interactions (for example, complex calculations, multi-step forms) for granular detail.
2. **Log application-specific events**: Generate high-fidelity logs that directly correlate with the flow of a trace for better debugging.
3. **Create custom metrics**: Record application-specific KPIs not covered by standard RUM metrics (for example, UI component render counts, client-side transaction success rates).

Leveraging the OpenTelemetry API to augment data collection makes your application's observability truly comprehensive, bridging the gap between technical monitoring and business intelligence.

### Track request path with traces

Your web application might initiate several HTTP requests to an associated API. With the instrumentations established in the previous section, a span is generated for each request, each part of a separate trace, meaning they are treated as independent operations. While this provides a clear breakdown of each individual request, there are cases where consolidating multiple related requests within a single, cohesive trace is highly desirable for better observability.

An example is a recurring task that updates the user interface at regular intervals to display various datasets that fluctuate over time. In this case, grouping all the API calls necessary for a single UI refresh into one trace allows you to view the overall performance and flow of the entire update cycle.

:::{dropdown} Example: Group API calls in a trace

```javascript
import { trace } from '@opentelemetry/api';
const tracer = trace.getTracer('app-tracer');

// Update the UI
setInterval(function () {
  tracer.startActiveSpan('ui-update', async function (span) {
    const datasetOne = await fetchDatasetOne();
    // Update the UI with 1st dataset, some other async work
    const datasetTwo = await fetchDatasetTwo();
    // Update the UI with 2nd dataset
    span.end();
  });
}, intervalTime)
```

:::

By using the `startActiveSpan` callback mechanism, you can wrap the asynchronous data fetching logic within a dedicated active trace. This technique accurately captures the execution flow and performance characteristics of operations that involve multiple steps or services. You get a single root span for the entire operation; this root span established by the callback acts as the primary container for the entire sequence of events. Contained within this root span are two distinct child spans that represent each request from the UI to the API.

### Record relevant events with logs

Relevant events occurring within your application can be recorded using a logger. A typical scenario involves documenting business-critical occurrences, such as conversions or purchases.

```javascript
import { logs, SeverityNumber } from '@opentelemetry/api-logs';
const logger = logs.getLogger('app-logger');

logger.emit({
  eventName: 'purchase',
  timestamp: Date.now(),
  attributes: {
    'orderId': '12345-54321',
    'amount': '200.56',
  }
});
```

## Browser constraints

Review the following constraints in your web application to avoid any data transmission issues.

### Content Security Policy

If your website is making use of Content Security Policies (CSPs), make sure that the domain of your OTLP endpoint is included. If your Collector endpoint is `https://collector.example.com:4318/v1/traces`, add the following directive:

```text
connect-src collector.example.com:4318/v1/traces
```

### Cross-Origin Resource Sharing (CORS)

If your website and Collector are hosted at a different origin, your browser might block the requests going out to your Collector. To solve this, you need to configure special headers for Cross-Origin Resource Sharing (CORS). This configuration depends on the solution you want to adopt and is described in the [OTLP endpoint](#otlp-endpoint) section.

## Known limitations

- The Managed OTLP endpoint (mOTLP) cannot be directly configured for CORS. A reverse proxy is required.
- {{apm-server}} does not support CORS configuration for OTLP endpoints.
- Metrics from browser-based RUM might have limited utility compared to backend metrics.
- Some OpenTelemetry instrumentations for browsers are still experimental.
- Performance impact on the browser should be monitored, especially when using multiple instrumentations.
- Authentication using API keys requires special handling in the reverse proxy configuration.

## Troubleshooting

This section provides solutions to common issues you might encounter when setting up OpenTelemetry for RUM with {{product.observability}}.

:::{dropdown} Module import or bundler errors

If you see errors like "Cannot find module" or bundler-specific issues:

1. Ensure all required packages are installed and listed in `package.json`.

2. Different bundlers (Webpack, Rollup, Vite) may require specific configuration for OpenTelemetry packages.

3. For Webpack, you may need to add polyfills for Node.js modules. Add to your webpack config:

```javascript
resolve: {
  fallback: {
    "process": require.resolve("process/browser"),
    "buffer": require.resolve("buffer/")
  }
}
```

4. For Vite, add to your `vite.config.js`:

```javascript
optimizeDeps: {
  include: ['@opentelemetry/api', '@opentelemetry/sdk-trace-web']
}
```

5. If using TypeScript, ensure `tsconfig.json` has appropriate module resolution:

```json
{
  "compilerOptions": {
    "moduleResolution": "node",
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

:::

:::{dropdown} Reverse proxy configuration issues

If your reverse proxy is not forwarding requests correctly:

1. Ensure the reverse proxy (NGINX, Apache, etc.) is running and accessible.

2. Use curl to test the proxy endpoint directly:

```bash
curl -X POST https://your-proxy/v1/traces \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-webapp.example.com" \
  -d '{"test": "data"}' \
  -v
```

3. Review proxy logs for errors or blocked requests.

4. Ensure the proxy can reach the backend Collector or mOTLP endpoint.

:::

:::{dropdown} Configuration issues

If your OpenTelemetry setup isn't initializing correctly:

1. Ensure `OTEL_EXPORTER_OTLP_ENDPOINT` doesn't include the signal path (like `/v1/traces`). The SDK adds this automatically:

```javascript
// Correct
const OTEL_EXPORTER_OTLP_ENDPOINT = 'https://collector.example.com:4318';

// Incorrect
const OTEL_EXPORTER_OTLP_ENDPOINT = 'https://collector.example.com:4318/v1/traces';
```

2. Verify `service.name` is set and doesn't contain special characters:

```javascript
const OTEL_RESOURCE_ATTRIBUTES = {
  'service.name': 'my-web-app', // Required
  'service.version': '1.0.0',
};
```

3. Ensure providers are registered before instrumentations:

```javascript
// Correct order:
// 1. Configure and register tracer provider
trace.setGlobalTracerProvider(tracerProvider);
// 2. Then register instrumentations
registerInstrumentations({...});
```

:::

:::{dropdown} Data not appearing in {{kib}}

If you've instrumented your application but don't see data in {{kib}}, check the following:

1. Ensure `OTEL_EXPORTER_OTLP_ENDPOINT` points to the correct endpoint. Test the endpoint connectivity using browser developer tools.

2. Open your browser's developer console (F12) and look for network errors or OpenTelemetry-related error messages. Common issues include failed requests to the OTLP endpoint.

3. Ensure `service.name` is set in your resource attributes. Without this attribute, data might not be properly categorized in {{kib}}.

4. In {{kib}}, navigate to **{{stack-manage-app}}** > **{{index-manage-app}}** > **Data Streams** and verify that OpenTelemetry data streams are being created (for example, `traces-*`, `logs-*`, `metrics-*`).

5. Set `OTEL_LOG_LEVEL` to `debug` to get detailed information about what's happening:

```javascript
const OTEL_LOG_LEVEL = 'debug';
```

:::

:::{dropdown} CORS errors

CORS errors are the most common issue with browser-based RUM. Symptoms include:

- Network requests blocked in the browser console
- Error messages like "Access to fetch at '...' from origin '...' has been blocked by CORS policy"

1. Verify CORS configuration: If using a reverse proxy, ensure the CORS headers are correctly configured. The `Access-Control-Allow-Origin` header must match your web application's origin.

2. Check allowed headers: Ensure all necessary headers are included in `Access-Control-Allow-Headers`, especially `Authorization` if using authentication.

3. Verify preflight requests: CORS requires preflight OPTIONS requests. Ensure your reverse proxy or Collector handles these correctly with a 204 response.

4. Test with a request: Try sending a test request using `curl` or a tool like Postman to verify the endpoint is accessible:

```bash
curl -X POST https://your-proxy-endpoint/v1/traces \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-webapp.example.com" \
  -v
```

:::

:::{dropdown} Content Security Policy (CSP) violations

If you get CSP violation errors in the browser console, your Content Security Policy is blocking connections to the OTLP endpoint.

Add the Collector endpoint to your CSP `connect-src` directive:

```text
Content-Security-Policy: connect-src 'self' https://collector.example.com:4318
```

:::

:::{dropdown} Authentication failures

If using mOTLP or a Collector with authentication requirements:

1. Ensure your authentication credentials are valid and not expired.

2. If using a reverse proxy, verify it's correctly forwarding the `Authorization` header:

```nginx
proxy_set_header Authorization $http_authorization;
```

3. The `Authorization` header must be listed in `Access-Control-Allow-Headers` for preflight requests.

:::

:::{dropdown} Spans or traces not correlating correctly

If you get disconnected spans or traces that should be related:

1. Ensure you're using `startActiveSpan` correctly for creating parent-child span relationships.

2. All spans in a trace should have the same resource attributes, especially `service.name`.

3. Register instrumentations after configuring the tracer provider, not before.

:::

:::{dropdown} Instrumentation not capturing data

If specific instrumentations aren't working:

1. Ensure instrumentations are registered after the tracer provider is configured.

2. Some instrumentations have specific browser requirements. Check the console for warnings.

3. Register instrumentations one at a time to identify which ones are causing issues.

:::

:::{dropdown} Integration method issues

If you're having issues with how you've integrated the telemetry code:

1. Ensure the telemetry initialization happens before your application code:

```javascript
// Top of your entry file
import { initOpenTelemetry } from './telemetry.js';
initOpenTelemetry({...});

// Then your app code
import { MyApp } from './app.js';
```

2. Some bundlers may remove OpenTelemetry code if it appears unused. Use `/* @preserve */` comments or configure your bundler to keep it.

3. Verify the script path is correct and the file is being served:

```html
<!-- Check browser network tab to verify this loads -->
<script src="./js/telemetry-bundle.js"></script>
```

4. If `initOpenTelemetry` is not defined, ensure your bundler is exposing it globally. For Webpack:

```javascript
output: {
  library: 'initOpenTelemetry',
  libraryTarget: 'window',
  libraryExport: 'default'
}
```

:::

If you continue to experience issues:

1. Ensure your target browsers support the OpenTelemetry features you're using.
2. Consult the [OpenTelemetry JavaScript documentation](https://opentelemetry.io/docs/languages/js/) for additional troubleshooting guidance.
3. Set the log level to `verbose` for maximum detail:

```javascript
const OTEL_LOG_LEVEL = 'verbose';
```

4. Start with only traces (no metrics or logs) and one instrumentation to isolate the issue.
5. Review the code examples throughout this guide and compare with your implementation.

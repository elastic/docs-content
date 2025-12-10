---
navigation_title: OpenTelemetry for Real User Monitoring (RUM)
description: Instrument web applications with OpenTelemetry for Real User Monitoring using Elastic Observability.
applies_to:
  product: preview
  stack:
  serverless:
    observability:
products:
  - id: cloud-serverless
  - id: observability
---

# OpenTelemetry for Real User Monitoring (RUM)

:::{important}
Using OpenTelemetry for Real User Monitoring (RUM) with {{product.observability}} is currently in technical preview and should not be used in production environments. This feature may be changed or removed in a future release and has [known limitations](#known-limitations). Features in preview are not subject to support SLAs like GA features.
:::

You can instrument your web application with OpenTelemetry browser instrumentation for use with {{product.observability}}. The following sections detail the required components and their proper configuration to acquire traces, logs, and metrics from the application to visualize them within {{kib}}.

## Before you begin [before-you-begin]

You need an OTLP endpoint to ingest data from the OpenTelemetry RUM instrumentation. If you're setting up a new deployment, [create](/solutions/observability/get-started.md) an {{ecloud}} hosted deployment or {{serverless-short}} project, which includes the [{{motlp}}](opentelemetry://reference/motlp.md). If you own a self-hosted stack or your deployment does not have the {{motlp}}, configure an [EDOT Collector in Gateway mode](https://www.elastic.co/docs/reference/edot-collector/modes#edot-collector-as-gateway).

After you have prepared the OTLP endpoint, set up a reverse proxy to forward the telemetry from your web application origin to the Collector. You need a reverse proxy for the following reasons:

- EDOT Collector requires an `Authorization` header with an ApiKey to accept OTLP exports. Setting up the required key in a web application makes it publicly available, which is not advisable. A reverse proxy can help you manage this key securely.
- If you have set up your own EDOT Collector, it's likely to have a different origin than your web application. In this scenario you have to set up [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) for the web application in the EDOT Collector configuration file. This procedure can be cumbersome if you have to manage many applications.
- You can apply rate limiting or any other mechanisms to control traffic before it reaches the EDOT Collector.

The following snippet shows the configuration for an NGINX reverse proxy to forward all telemetry to the EDOT Collector located at `collector.example.com` from the origin `webapp.example.com`:

:::{dropdown} NGINX reverse proxy configuration
```nginx
server {
    # Configuration for HTTP/HTTPS goes here
    location / {
        # Take care of preflight requests
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Max-Age' 1728000; # 20 days in seconds
            add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always; # Set the allowed origins for preflight requests
            add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' 'webapp.example.com' always; # Set the allowed origins for requests
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Headers' 'Accept,Accept-Language,Authorization,Content-Language,Content-Type' always;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # Set the auth header for the Collector here. It's recommended to follow the security best practices
        # for adding secrets into services according to your infrastructure and company policy. A couple of references:
        # for Docker: https://docs.docker.com/engine/swarm/secrets/#intermediate-example-use-secrets-with-a-nginx-service
        # for K8s: https://kubernetes.io/docs/concepts/configuration/secret/
        proxy_set_header Authorization 'ApiKey ...your Elastic API key...'; 
        proxy_pass https://collector.example.com:4318;
    }
}
```
:::

:::{warning}
Avoid using the OTel RUM agent alongside any other {{apm-agent}}, including Elastic {{product.apm}} agents. Running multiple agents might lead to conflicting instrumentation, duplicate telemetry, or other unexpected behavior.
:::

## Define the basic settings [otel-rum-basic-settings]

The minimal configuration you need to instrument your web application with OpenTelemetry includes:

- **OTEL_EXPORTER_OTLP_ENDPOINT**: The full URL of the proxy you have configured in the [OTLP endpoint](#before-you-begin) section.
- **OTEL_RESOURCE_ATTRIBUTES**: A JavaScript object that will be used to define the resource. The most important attributes to define are:
  - `service.name` (string): Name of the application you're instrumenting.
  - `service.version` (string, optional): A string representing the version or build of your app.
  - `deployment.environment.name` (string, optional): Name of the environment where the app runs (if applicable); for example, "prod", "dev", or "staging".
- **OTEL_LOG_LEVEL**: Use this configuration to set the log level of the OpenTelemetry components you're going to use.

## Set up OpenTelemetry for the browser [otel-rum-set-up-open-telemetry-for-the-browser]

To instrument your web application with OpenTelemetry in the browser, you need to add a script that configures the essential components, including the context manager, signal providers, processors, and exporters. After adding the script, you can register the instrumentations so they can observe your app and send telemetry data to your endpoint.

The following starter script is in plain JavaScript. If you use TypeScript, you can adapt this script by changing the file extension to `.ts` and adding the necessary type definitions. OpenTelemetry packages are written in TypeScript, so they include the appropriate type definitions for TypeScript.

:::{note}
Each signal configuration is independent of the others and has to be configured independently. The OpenTelemetry API defaults to no-op providers for traces, metrics, and logs.
:::

::::::{stepper}

:::::{step} Set the configuration

Start by setting the options to be used by all the signals and the instrumentation code, as well as initializing the internal logger.

For this step, you need the following dependencies:

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

A [resource](https://opentelemetry.io/docs/concepts/resources/) is an entity that generates telemetry, with its characteristics captured in resource attributes. An example is a web application operating within a browser that produces telemetry data.

A standardized set of attributes is specified in [Browser resource semantic conventions](https://opentelemetry.io/docs/specs/semconv/resource/browser/), which can be included alongside those outlined in the configuration section. OpenTelemetry offers resource detectors like `browserDetector` to help set these attributes like brands, mobile, and platform.

To define the resource, you need the following dependencies:

- `@opentelemetry/resources`: This package helps you to define and work with resources because a Resource is not a plain object and has some properties (like immutability) and constraints.
- `@opentelemetry/browser-detector`: Detectors help you to define a resource by querying the runtime and environment and resolving some attributes. In this case, the browser detector resolves the language, brands, and mobile attributes of the browser namespace.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/resources @opentelemetry/browser-detector
```

After the dependencies are installed, define the resource for your instrumentation with the following code:

:::{dropdown} Resource definition
```javascript
import { resourceFromAttributes, detectResources } from '@opentelemetry/resources';
import { browserDetector } from '@opentelemetry/opentelemetry-browser-detector';

const detectedResources = detectResources({ detectors: [browserDetector] });
let resource = resourceFromAttributes(OTEL_RESOURCE_ATTRIBUTES);
resource = resource.merge(detectedResources);
```
:::
:::::

:::::{step} (Optional) Configure tracing

Configure a [TracerProvider](https://opentelemetry.io/docs/concepts/signals/traces/#tracer-provider) to enable instrumentations to transmit traces and allow for the creation of custom spans. A TracerProvider requires several components:

- **Resource**: The resource to be associated with the spans created by the tracers. You defined this in the second step.
- **Span Processor**: A component that manages the spans generated by the tracers and forwards them to a [SpanExporter](https://opentelemetry.io/docs/specs/otel/trace/sdk/#span-exporter). The exporter should be configured to direct data to an endpoint designated for traces.
- **Span Exporter**: Manages the transmission of spans to the Collector.
- **Context Manager**: A mechanism for managing the active Span context across asynchronous operations and threads. It ensures that when a new Span is created, it correctly identifies its parent Span.

For this step, you need the following dependencies:

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

After the dependencies are installed, configure and register a TracerProvider with the following code:

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

Now you can use the OpenTelemetry API to get a tracer and start creating your own spans. Instrumentations are also using OpenTelemetry API to get tracers and send telemetry data. Registering intrumentations after having the tracer provider set up ensures they have the right tracers when requested to the API.

:::::

:::::{step} (Optional) Configure metrics

Similar to traces, configure a [MeterProvider](https://opentelemetry.io/docs/concepts/signals/metrics/#meter-provider) for metrics. A MeterProvider requires several components:

- **Resource**: The resource to be associated with the metrics created by the meters. You defined this in the second step.
- **Metric Reader**: Used to determine how often metrics are collected and what destination they should be exported to. In this case, use a `PeriodicExportingMetricReader` configured to collect and export metrics at a fixed interval.
- **Metric Exporter**: Responsible for serializing and sending the collected and aggregated metric data to a backend observability platform. Use the OTLP/HTTP exporter.

For this step, you need the following dependencies:

- `@opentelemetry/sdk-metrics`: This package contains all the required components to set up metrics.
- `@opentelemetry/exporter-metrics-otlp-http`: This package contains the exporter for the HTTP/JSON protocol.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/sdk-metrics @opentelemetry/exporter-metrics-otlp-http
```

After the dependencies are installed, configure and register a MeterProvider with the following code:

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

:::::{step} (Optional) Configure logs

Like traces and metrics, configure a [LoggerProvider](https://opentelemetry.io/docs/specs/otel/logs/sdk/#loggerprovider) if you want to record relevant events that are happening in your application using the API or instrumentations. A LoggerProvider requires several components:

- **Resource**: The resource to be associated with the log records created by the loggers. You defined this in the second step.
- **LogRecord Processor**: A component that manages the log records generated by the loggers and forwards them to a [LogExporter](https://opentelemetry.io/docs/specs/otel/logs/sdk/#logrecordexporter). The exporter should be configured to direct data to an endpoint designated for logs.
- **Log Exporter**: Manages the transmission of log records to the Collector.

For this step, you need the following dependencies:

- `@opentelemetry/api-logs`: This package contains the logs API. This API is not yet included in the generic API package because logs are still experimental.
- `@opentelemetry/sdk-logs`: This package contains all the required components to set up logs.
- `@opentelemetry/exporter-logs-otlp-http`: This package contains the exporter for the HTTP/JSON protocol.

To install the dependencies, run the following command:

```bash
npm install @opentelemetry/api-logs @opentelemetry/sdk-logs @opentelemetry/exporter-logs-otlp-http
```

After the dependencies are installed, configure and register a LoggerProvider with the following code:

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

:::::{step} Register the instrumentations

The final step for setting up Real User Monitoring (RUM) through OpenTelemetry is registering the instrumentations. Instrumentations are modules that automatically capture telemetry data, like network requests or DOM interactions, by using the OpenTelemetry API.

With the OpenTelemetry SDK, resource attributes, and exporters already configured, all telemetry data generated by these registered instrumentations is automatically processed and exported.

Install the following dependencies:

- `@opentelemetry/instrumentation`: This package contains the core components of instrumentations along with some utilities.
- `@opentelemetry/auto-instrumentations-web`: This package contains the more common instrumentations for web apps. Which are:
  - `@opentelemetry/instrumentation-document-load`: This instrumentation package measures the time it took the document to load and also the load timings of its resources. More info at [instrumentation-document-load](https://www.npmjs.com/package/@opentelemetry/instrumentation-document-load).
  - `@opentelemetry/instrumentation-fetch`: This instrumentation keeps track of your web application requests made through the Fetch API. More info at [instrumentation-fetch](https://www.npmjs.com/package/@opentelemetry/instrumentation-fetch).
  - `@opentelemetry/instrumentation-xml-http-request`: This instrumentation keeps track of your web application requests made through the XMLHttpRequest API. More info at [instrumentation-xml-http-request](https://www.npmjs.com/package/@opentelemetry/instrumentation-xml-http-request).
  - `@opentelemetry/instrumentation-user-interaction`: This instrumentation measures user interactions in your web application. More info at [instrumentation-user-interaction](https://www.npmjs.com/package/@opentelemetry/instrumentation-user-interaction).
- `@opentelemetry/instrumentation-long-task`: This instrumentation is not part of the auto instrumentations package. It gathers information about long tasks being executed in your browser, helping to spot issues like unresponsive UI in your web application. More info at [instrumentation-long-task](https://www.npmjs.com/package/@opentelemetry/instrumentation-long-task).
  
To install the dependencies, run the following command:

```bash
npm install @opentelemetry/instrumentation\
      @opentelemetry/auto-instrumentations-web\
      @opentelemetry/instrumentation-long-task
```

After the dependencies are installed, configure and register instrumentations with the following code:

:::{dropdown} Instrumentations registration
```javascript
import { registerInstrumentations } from '@opentelemetry/instrumentation';
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';
import { LongTaskInstrumentation } from '@opentelemetry/instrumentation-long-task';


// Register instrumentations
registerInstrumentations({
  instrumentations: [
    getWebAutoInstrumentations(),
    new LongTaskInstrumentation(),
  ],
});
```
:::
:::::

:::::{step} Complete the setup script

All these pieces together give you a complete setup of all the signals for your web site or application. For convenience, it's better to have it in a separate file which can be named, for example, `telemetry.js`. This file should export a function that accepts the configuration allowing you to reuse the setup across different UIs.

To install all the dependencies needed for the complete setup, run the following command:

:::{dropdown} Install setup script dependencies
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
      @opentelemetry/auto-instrumentations-web\
      @opentelemetry/instrumentation-long-task
```
:::

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
import { getWebAutoInstrumentations } from '@opentelemetry/auto-instrumentations-web';
import { LongTaskInstrumentation } from '@opentelemetry/instrumentation-long-task';

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
      getWebAutoInstrumentations(),
      new LongTaskInstrumentation(),
    ],
  });
}
```
:::
:::::
::::::

## Integrate with your application

With the setup script in a single file, you can now apply it to your web application. You can choose from two main approaches:

1. **Import the code**: Use your build tooling to manage the dependencies and integrate the code into the application bundle. This is the simplest option and is recommended, although it increases the size of your application bundle.

2. **Bundle in a file**: Use a bundler to generate a separate JavaScript file that you include in the `<head>` section of your HTML page. This approach keeps the telemetry code separate from your application bundle.

### Import the code 

This approach is recommended, especially if you're using a web framework. The build tooling manages the dependencies and integrates the code into the application bundle. However, this approach increases the size of your application bundle.

For example, if you're using Webpack, you can import the code like this:

:::{dropdown} Example: Import telemetry.js in your app

```javascript
import { initOpenTelemetry } from 'telemetry.js';

initOpenTelemetry({
  logLevel: 'info',
  endpoint: 'https://proxy.example.com',
  resourceAttributes: {
    'service.name': 'my-web-app',
    'service.version': '1',
  }
});
```
:::

If you're using a framework, there are some suitable places for it, depending on which one you're using:

| Framework | Method |
|-----------|-------------|
| **React** | Create a component which initializes the instrumentation when mounted. The component should be added as child of the `<App/>` component. |
| **VueJs** | Create a plugin which does the initialization when installed in the app. Refer to the [VueJS docs](https://vuejs.org/guide/reusability/plugins.html) for more details. |
| **Angular** | Add the initialization snippet in `./src/main.ts` which is the entry point of the application. Refer to the [Angular docs](https://v17.angular.io/guide/file-structure#application-source-files) for more details. |

### Bundle in a file

You can use a bundler like Webpack, Rollup, or Vite to generate a separate JavaScript file. 

#### Webpack

This is an example of a `webpack.config.js` to author a library as described in the [Webpack documentation](https://webpack.js.org/guides/author-libraries/) in UMD format.

:::{dropdown} Example: Webpack configuration
```javascript
const path = require('path');

module.exports = {
  entry: './path/to/telemetry.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'telemetry.umd.js',
    library: {
      type: 'umd'
    }
  },
};
```
:::

#### Vite

This is an example of a `vite.config.js` file in [library mode](https://vite.dev/guide/build#library-mode) to get a bundle in UMD format.

:::{dropdown} Example: Vite configuration
```javascript
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'vite';

const __dirname = dirname(fileURLToPath(import.meta.url))
export default defineConfig({
  build: {
    lib: {
        entry: resolve(__dirname, './path/to/telemetry.js'),
        formats: ['umd'],
        name: 'telemetry',
        fileName: (format) => `telemetry.${format}.js`
    },
    sourcemap: true,
  }
});

```
:::

Place the file within the application's assets folder and include it in the `<head>` section of the HTML page. Assuming the files are in a folder named `js` you can load the telemetry file in a synchronous or asynchronous way.

::::{dropdown} Example: Synchronous / Blocking pattern
Add a `<script>` tag to load the bundle and use the `initOpenTelemetry` global function to initialize the agent:

```html
<script src="./js/telemetry.umd.js"></script>
<script>
  initOpenTelemetry({
    logLevel: 'info',
    endpoint: 'https://proxy.example.com',
    resourceAttributes: {
      'service.name': 'my-web-app',
      'service.version': '1',
    }
  });
</script>
```
::::
::::{dropdown} Example: Asynchronous / Non-Blocking pattern
Loading the script asynchronously ensures the agent script doesn't block other resources on the page. However, it still blocks the browser's `onload` event.

```html
<script>
  ;(function(d, s, c) {
    var j = d.createElement(s),
      t = d.getElementsByTagName(s)[0]

    j.src = './js/telemetry.umd.js'
    j.onload = function() {elasticApm.init(c)}
    t.parentNode.insertBefore(j, t)
  })(
    document,
    'script',
    {
      logLevel: 'info',
      endpoint: 'https://proxy.example.com',
      resourceAttributes: {'service.name': 'my-web-app', 'service.version': '1'} }
  )
</script>
```

:::{note}
Because the downloading and initializing of the instrumentations happens asynchronously, distributed tracing doesn't work for requests that occur before the agent is initialized.
:::

::::


## Extend your telemetry with manual instrumentation

By using the OpenTelemetry API directly, you can send highly specific, custom telemetry to augment automatic collection. This custom instrumentation allows you to:

- Create explicit spans around unique critical business logic or user interactions (for example, complex calculations, multi-step forms) for granular detail.
- Generate high-fidelity logs that directly correlate with the flow of a trace for better debugging.
- Record application-specific KPIs not covered by standard RUM metrics (for example, UI component render counts, client-side transaction success rates).

### Track request path with traces

With the instrumentations configured in the previous section, a span is generated for each request, each part of a separate trace, meaning they're treated as independent operations. While this provides a clear breakdown of each individual request, you might need to consolidate multiple related requests within a single, cohesive trace.

An example is a recurring task that updates the user interface at regular intervals to display various datasets that fluctuate over time. Grouping all the API calls necessary for a single UI refresh into one trace allows you to view the overall performance and flow of the entire update cycle.

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

By using the `startActiveSpan` callback mechanism, you can wrap the asynchronous data fetching logic within a dedicated active trace.

### Record relevant events with logs

Relevant events occurring within your application can be recorded using a logger. A typical scenario involves documenting business-critical occurrences, such as conversions or purchases.

:::{dropdown} Example: Record relevant events with logs
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
:::

## Browser constraints

Review the following constraints in your web application to avoid any data transmission issues.

### Content security policies (CSP)

If your website is making use of Content Security Policies (CSPs), make sure that the domain of your OTLP endpoint is included. If your Collector endpoint is `https://collector.example.com:4318/v1/traces`, add the following directive:

```text
connect-src collector.example.com:4318/v1/traces
```

### Cross-origin resource sharing (CORS)

If your website and the configured endpoint have a different origin, your browser might block the export requests. If you followed the instructions in the [OTLP endpoint](#before-you-begin) section, you already set up the necessary CORS headers. Otherwise you need to configure special headers for CORS in the receiving endpoint.

## Known limitations

These are the known limitations of using OpenTelemetry for RUM with {{product.observability}}:

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

3. For Webpack, you may need to add polyfills for Node.js modules. Add this to your Webpack config:

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

1. Ensure the reverse proxy (NGINX, Apache, and so on) is running and accessible.

2. Use `curl` to test the proxy endpoint directly:

```bash
curl -X POST https://your-proxy/v1/traces \
  -H "Content-Type: application/json" \
  -H "Origin: https://your-webapp.example.com" \
  -d '{"test": "data"}' \
  -v
```

3. Review proxy logs for errors or blocked requests.

4. Ensure the proxy can reach the backend EDOT Collector or mOTLP endpoint.

:::

:::{dropdown} Configuration issues

If your OpenTelemetry setup isn't initializing correctly:

1. Ensure `OTEL_EXPORTER_OTLP_ENDPOINT` doesn't include the signal path (like `/v1/traces`). The script provided adds this automatically:

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
tracerProvider.register({ contextManager: new ZoneContextManager() });
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

If using mOTLP or an EDOT Collector with authentication requirements:

1. Ensure your authentication credentials are valid and not expired.

2. If using a reverse proxy, verify it's correctly forwarding the `Authorization` header:

```nginx
proxy_set_header Authorization 'ApiKey _elastic_api_key_';
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
<script src="./js/telemetry.umd.js"></script>
```

4. If `initOpenTelemetry` is not defined, ensure your bundler is exposing it globally. For example, for Webpack:

```javascript
output: {
  library: 'initOpenTelemetry',
  libraryTarget: 'window',
  libraryExport: 'default'
}
```

:::

### General troubleshooting steps

If you continue to experience issues:

1. Ensure your target browsers support the OpenTelemetry features you're using.
2. Consult the [OpenTelemetry JavaScript documentation](https://opentelemetry.io/docs/languages/js/) for additional troubleshooting guidance.
3. Set the log level to `verbose` for maximum detail:

```javascript
const OTEL_LOG_LEVEL = 'verbose';
```

4. Start with only traces (no metrics or logs) and one instrumentation to isolate the issue.
5. Review the code examples throughout this guide and compare with your implementation.

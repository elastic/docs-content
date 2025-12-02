---
navigation_title: EDOT Node.js
description: Troubleshooting guide for the Elastic Distribution of OpenTelemetry Node.js (EDOT Node.js).
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_node: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-sdk
---

# Troubleshooting the EDOT Node.js SDK

Use the information on this page to troubleshoot issues using EDOT Node.js.

If you need help and you're an existing Elastic customer with a support contract, create a ticket in the [Elastic Support portal](https://support.elastic.co/customers/s/login/). Other users can post in the [APM discuss forum](https://discuss.elastic.co/c/apm) or [open a GitHub issue](https://github.com/elastic/elastic-otel-node/issues).

As a first step, review the [supported technologies](elastic-otel-node://reference/edot-node/supported-technologies.md) to ensure your application is supported by the SDK. Are you using a Node.js version that the SDK supports? Are the versions of your dependencies in the [supported version range](elastic-otel-node://reference/edot-node/supported-technologies.md#instrumentations) to be instrumented?

## Set a service name

Make sure you have set a service name set using `OTEL_SERVICE_NAME=my-service` or through the `OTEL_RESOURCE_ATTRIBUTES=service.name=my-service` environment variables. Otherwisem by default the data is sent to the `unknown_service:node` service: you might be getting data but it might all be under that service.

## Check connectivity

Check from the host, VM, pod, container running your application, that connectivity is available to the Collector. For more detailed connectivity troubleshooting, refer to [Connectivity issues](../../connectivity.md). Run the following command:

```bash
curl -i $ELASTIC_OTLP_ENDPOINT \
    -X POST -d "{}" -H content-type:application/json \
    -H "Authorization: ApiKey $ELASTIC_API_KEY"
```

For example, if you [configured](elastic-otel-node://reference/edot-node/configuration.md#basic-configuration) EDOT Node.js with:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud"
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=ApiKey Zm9vO...mJhcg=="
...
```

Then you would run:

```bash
curl -i https://my-deployment-abc123.ingest.us-west-2.aws.elastic.cloud \
    -X POST -d "{}" -H content-type:application/json \
    -H "Authorization: ApiKey Zm9vO...mJhcg=="
```

If that works correctly, you should expect to see output similar to the following:

```
HTTP/1.1 200 OK
Content-Type: application/json
Date: Thu, 27 Mar 2025 23:07:09 GMT
Content-Length: 21

{"partialSuccess":{}}
```


## Deactivate the SDK

If your application has an issue, but you are not sure if the EDOT Node.js SDK could be the cause, try deactivating the SDK.

You can exclude the SDK by not starting it with your application by running the following command:

```bash
node my-app.js   # instead of 'node --import @elastic/opentelemetry-node my-app.js'
```

Or by setting the `OTEL_SDK_DISABLED` environment variable:

```bash
export OTEL_SDK_DISABLED=true
node --import @elastic/opentelemetry-node my-app.js
```

## SDK diagnostic logs [sdk-diagnostic-logs]

Turn on verbose diagnostic or debug logging from EDOT Node.js:

1. Set the `OTEL_LOG_LEVEL` environment variable to `verbose`.
2. Restart your application, and reproduce the issue. If the issue is about not seeing telemetry that you expect to see, be sure to use your application so that telemetry data is generated. For troubleshooting missing telemetry, refer to [No application-level telemetry visible in {{kib}}](missing-app-telemetry.md).
3. Gather the full verbose log from application start until after the issue was reproduced.

For more information, refer to [Enable debug logging for EDOT SDKs](enable-debug-logging.md).

The start of the diagnostic log will look something like this:

```
% OTEL_LOG_LEVEL=verbose node --import @elastic/opentelemetry-node my-app.js
{"name":"elastic-otel-node","level":10,"msg":"import.mjs: registering module hook","time":"2025-03-27T23:29:12.075Z"}
{"name":"elastic-otel-node","level":10,"msg":"ElasticNodeSDK opts: {}","time":"2025-03-27T23:29:12.392Z"}
{"name":"elastic-otel-node","level":20,"msg":"@opentelemetry/api: Registered a global for diag v1.9.0.","time":"2025-03-27T23:29:12.392Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@elastic/opentelemetry-instrumentation-openai\"","time":"2025-03-27T23:29:12.393Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@opentelemetry/instrumentation-amqplib\"","time":"2025-03-27T23:29:12.394Z"}
{"name":"elastic-otel-node","level":20,"msg":"Enabling instrumentation \"@opentelemetry/instrumentation-aws-sdk\"","time":"2025-03-27T23:29:12.395Z"}
...
{"name":"elastic-otel-node","level":10,"msg":"Metrics exporter protocol set to http/protobuf","time":"2025-03-27T23:29:12.408Z"}
{"name":"elastic-otel-node","level":30,"preamble":true,"distroVersion":"0.7.0","env":{"os":"darwin 24.3.0","arch":"arm64","runtime":"Node.js v18.20.4"},"msg":"start Elastic Distribution of OpenTelemetry Node.js","time":"2025-03-27T23:29:12.409Z"}
...
```

Look for warnings (`"level":40`) or errors (`"level":50`) in the log output that might indicate an issue.

## Deactivate an instrumentation

To deactivate an instrumentation, set the [`OTEL_NODE_DISABLED_INSTRUMENTATIONS`](elastic-otel-node://reference/edot-node/configuration.md#otel_node_disabledenabled_instrumentations-details) environment variable.

For example, to deactivate `@opentelemetry/instrumentation-net` and `@opentelemetry/instrumentation-dns` run the following commands:

```bash
export OTEL_NODE_DISABLED_INSTRUMENTATIONS=dns,net
...
node --import @elastic/opentelemetry-node my-app.js
```

## Check if EDOT Node.js is running

Look for `start Elastic Distribution of OpenTelemetry Node.js` in the application log.

As it is starting, EDOT Node.js always logs at the "info" level a preamble to indicate that it has started. For example:

```json
{"name":"elastic-otel-node","level":30,"preamble":true,"distroVersion":"0.7.0","env":{"os":"darwin 24.3.0","arch":"arm64","runtime":"Node.js v18.20.4"},"msg":"start Elastic Distribution of OpenTelemetry Node.js","time":"2025-03-27T22:14:08.288Z"}
...
```

The `distroVersion` field also indicates which version of EDOT Node.js is being used.



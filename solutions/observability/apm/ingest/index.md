---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-collect-application-data.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-send-data-to-elastic.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Collect application data [apm-collect-application-data]

::::{note}
**For Observability Serverless projects**, the **Admin** role or higher is required to send APM data to Elastic. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
::::

## Language-specific options [_language_specific_options]

Use Elastic APM agents or an OpenTelemetry language SDK to instrument a service in the language its written in:

* [**OpenTelemetry**](/solutions/observability/apm/opentelemetry/index.md): OpenTelemetry is an open source set of APIs, SDKs, tooling, and integrations that enable the capture and management of telemetry data from your services and applications. Elastic offers [Elastic Distributions of OpenTelemetry (EDOT)](opentelemetry://reference/edot-sdks/index.md), which are customized versions of [OpenTelemetry language SDKs](https://opentelemetry.io/docs/languages/) that are optimized to work with an Elastic backend.
* [**Elastic APM agents**](/solutions/observability/apm/apm-agents/index.md): Elastic APM agents are instrumentation libraries written in the same language as your service.


**Not sure which method is right for you?** Compare the available options.

### Capabilities [_capabilities]

|  | Elastic Distributions of OpenTelemetry (EDOT) | Elastic APM agent |
| --- | --- | --- |
| **Support level** | Fully supported for available languages | Fully supported |
| **Data protocol** | [OpenTelemetry protocol (OTLP)](https://opentelemetry.io/docs/specs/otel/protocol/) | Elastic protocol |
| **Central configuration** | {applies_to}`product: preview` Supported<br>*Refer to* [*Central configuration*](opentelemetry://reference/central-configuration.md) | Supported<br>*Refer to* [*APM agent central configuration*](/solutions/observability/apm/apm-server/apm-agent-central-configuration.md) |

For a comparison of EDOT and APM data streams, refer to [Comparison with classic APM data streams](opentelemetry://reference/compatibility/data-streams.md#comparison-with-classic-apm-data-streams).

### Availability [apm-collect-data-availability]

| Language | Elastic Distributions of OpenTelemetry (EDOT) | Elastic APM agent |
| --- | --- | --- |
| **Android** | EDOT Android | Not available |
| **Go** | Not available | Go agent |
| **iOS** | EDOT iOS  | Not available |
| **Java** | EDOT Java | Java agent |
| **.NET** | EDOT .NET | .NET agent |
| **Node.js** | EDOT Node.js | Node.js agent |
| **PHP** | EDOT PHP | PHP agent |
| **Python** | EDOT Python | Python agent |
| **Ruby** | Not available | Ruby agent |

## Service-specific options [_service_specific_options]

Elastic also offers several tools to help you collect data from specific services:

* **Kubernetes**: The Elastic APM attacher for Kubernetes simplifies the instrumentation and configuration of your application pods. Read more in the [APM attacher for Kubernetes docs](apm-k8s-attacher://reference/index.md).
* **AWS Lambda Functions**: Helps you monitor your AWS Lambda functions. Read more in the [APM Architecture for AWS Lambda docs](apm-aws-lambda://reference/index.md).
* **Jaeger (deprecated)**: Helps you to switch an existing Jaeger setup from the default Jaeger backend to the {{stack}}. Read more in [Integrate with Jaeger](/solutions/observability/apm/ingest/jaeger.md).
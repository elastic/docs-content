---
navigation_title: LLM observability
description: Overview of LLM observability with Elastic, including supported technologies and quickstart instructions.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: preview
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# LLM observability with EDOT

Applications make more and more use of Generative Artificial Intelligence (GenAI). Telemetry data in terms of spans, metrics and logs when communicating with the GenAI APIs becomes more and more important to operate the application in production and understand the application's behavior and health state.

Elastic currently supports LLM observability through the Elastic Distributions of Opentelemetry (EDOT). The EDOT Java, EDOT Node.js, and EDOT Python distributions support LLM observability as a tech preview.

## Supported technologies

The following LLM platforms are supported:

| Technology | [EDOT Java](https://github.com/open-telemetry/opentelemetry-java-instrumentation/tree/main/instrumentation/openai/openai-java-1.1/javaagent) | [EDOT Node.js](elastic-otel-node://reference/edot-node/supported-technologies.md#llm-instrumentations) | [EDOT Python](elastic-otel-python://reference/edot-python/supported-technologies.md#llm-instrumentations) |
|:-----------|:----------|:-------------|:------------|
| OpenAI Client | ✅ | ✅ | ✅ |
| AWS Bedrock | ❌ | ❌ | ✅ |
| Google Vertex AI | ❌ | ❌ | ✅ |

See the [Supported Technologies section in the corresponding EDOT SDK](opentelemetry://reference/edot-sdks/index.md) for detailed information on supported versions.

## Quickstart

Follow these steps to instrument LLMs using EDOT.

### Instrument your LLM application

Select the environment and target system from the [quick start overview](/solutions/observability/get-started/opentelemetry/quickstart/index.md) and follow the setup instructions to instrument your LLM application. Instrumentation for the supported technologies is enabled by default.

### Configuration

See the [Configuration section in the corresponding EDOT SDK](opentelemetry://reference/edot-sdks/index.md) to turn on or off specific instrumentations and check which instrumentation is active by default.

When you complete the setup and configuration of the EDOT SDK and there is a workload on your application, start checking for telemetry data in {{kib}}. If there's no data showing up, see the troubleshooting of the corresponding EDOT SDK.

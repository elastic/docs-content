---
navigation_title: "LLM Observability"
---

# LLM Observability

While LLMs hold incredible transformative potential, they also bring complex challenges in reliability, performance, and cost management. Traditional monitoring tools require an evolved set of observability capabilities to ensure these models operate efficiently and effectively.
To keep your LLM-powered applications reliable, efficient, cost-effective, and easy to troubleshoot, Elastic provides a powerful LLM observability framework including key metrics, logs, and traces, along with pre-configured, out-of-the-box dashboards that deliver deep insights into model prompts and responses, performance, usage, and costs.
Elastic’s end-to-end LLM observability is delivered through the following methods: 

- Metrics and logs ingestion for LLM APIs (via Elastic integrations)
- APM tracing for OpenAI Models (via instrumentation)

## Metrics and logs ingestion for LLM APIs (via Elastic integrations)

Elastic’s LLM integrations now support the most widely adopted models, including OpenAI, Azure OpenAI, and a diverse range of models hosted on Amazon Bedrock and Google Vertex AI:

- Amazon Bedrock
- Azure OpenAI
- GCP Vertex AI
- OpenAI

## APM tracing for OpenAI Models (via instrumentation)

Elastic offers specialized OpenTelemetry Protocol (OTLP) tracing for applications leveraging OpeAI models hosted on OpenAI, Azure, and Amazon Bedrock, providing a detailed view of request flows. This tracing capability captures critical insights, including the specific models used, request duration, errors encountered, token consumption per request, and the interaction between prompts and responses. Ideal for troubleshooting, APM tracing allows you to find exactly where the issue is happening with precision and efficiency in your OpenAI-powered application. 

You can Instrument the application with one of the following OpenTelemetry API:

- Python
- Node.js
- Java

## Getting started

Check these instructions on how to setup and collect OpenTelemetry data for your LLM applications [create a link to https://github.com/elastic/opentelemetry/pull/100/files#diff-965570d21670c0ee4bba4b303960e5fe83b285f66b001ff8f31f0413f65a9d47 once the content is finalized and merged]

## Use cases

Understand LLM performance and reliability
For an SRE team optimizing a customer support system powered by Azure OpenAI, Elastic’s Azure OpenAI integration provides critical insights. They can quickly identify which model variants experience higher latency or error rates, enabling smarter decisions on model deployment or even switching providers based on real-time performance metrics.

[image]

## Troubleshoot OpenAI-powered applications

Consider an enterprise utilizing an OpenAI model for real-time user interactions. Encountering unexplained delays, an SRE can use OpenAI tracing to dissect the transaction pathway, identify if one specific API call or model invocation is the bottleneck, and monitor a request to see  the exact prompt and response between the user and the LLM. Such insight is pivotal for prompt resolution.

[image]

## Addressing Cost and Usage Concerns

For cost-sensitive deployments, being acutely aware of which LLM configurations are more cost-effective is crucial. Elastic’s dashboards, pre-configured to display model usage patterns, help mitigate unnecessary spending effectively. You can find out-of-the box dashboards for Azure OpenAI, OpenAI, Amazon Bedrock, and Google VertexAI models.

[image]

## Understand Compliance with Guardrails in Amazon Bedrock

With the Elastic Amazon Bedrock integration for Guardrails, SREs can swiftly address security concerns, like verifying if certain user interactions prompt policy violations. Elastic's observability logs clarify whether guardrails rightly blocked potentially harmful responses, bolstering compliance assurance.

[image]

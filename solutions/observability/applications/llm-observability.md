---
navigation_title: "LLM Observability"
---

# LLM Observability

While LLMs hold incredible transformative potential, they also bring complex challenges in reliability, performance, and cost management. Traditional monitoring tools require an evolved set of observability capabilities to ensure these models operate efficiently and effectively.
To keep your LLM-powered applications reliable, efficient, cost-effective, and easy to troubleshoot, Elastic provides a powerful LLM observability framework including key metrics, logs, and traces, along with pre-configured, out-of-the-box dashboards that deliver deep insights into model prompts and responses, performance, usage, and costs.
Elastic’s end-to-end LLM observability is delivered through the following methods: 

- Metrics and logs ingestion for LLM APIs (via [Elastic integrations](https://www.elastic.co/guide/en/integrations/current/introduction.html))
- APM tracing for LLM Models (via [instrumentation](https://elastic.github.io/opentelemetry/))

## Metrics and logs ingestion for LLM APIs (via Elastic integrations)

Elastic’s LLM integrations now support the most widely adopted models, including OpenAI, Azure OpenAI, and a diverse range of models hosted on Amazon Bedrock and Google Vertex AI. Depending on the LLM provider you choose, the following table shows which source you can use and which type of data -- log or metrics -- you can collect.

| **LLM Provider**  | **Source**  | **Metrics** | **Logs** | 
|--------|------------|------------|
| [Amazon Bedrock](https://www.elastic.co/guide/en/integrations/current/aws_bedrock.html)| [AWS CloudWatch Logs](https://github.com/elastic/integrations/tree/main/packages/aws_bedrock#compatibility) | ✅ | ✅ |  
| [Azure OpenAI](https://www.elastic.co/guide/en/integrations/current/azure_openai.html)| [Azure Monitor and Event Hubs](https://github.com/elastic/integrations/tree/main/packages/azure_openai#azure-openai-integration) | ✅ | ✅ | 
| [GCP Vertex AI](https://www.elastic.co/guide/en/integrations/current/gcp_vertexai.html) | [GCP Cloud Monitoring](https://github.com/elastic/integrations/tree/main/packages/gcp_vertexai#overview)  | ✅ | 🚧 | 
| [OpenAI](https://www.elastic.co/guide/en/integrations/current/openai.html) | [OpenAI Usage API](https://platform.openai.com/docs/api-reference/usage) | ✅| 🚧 | 

## APM tracing for LLM models (via instrumentation)

Elastic offers specialized OpenTelemetry Protocol (OTLP) tracing for applications leveraging LLM models hosted on OpenAI, Azure, and Amazon Bedrock, providing a detailed view of request flows. This tracing capability captures critical insights, including the specific models used, request duration, errors encountered, token consumption per request, and the interaction between prompts and responses. Ideal for troubleshooting, APM tracing allows you to find exactly where the issue is happening with precision and efficiency in your LLM-powered application. 

You can instrument the application with one of the following Elastic Distributions of OpenTelemetry (EDOT):

- [Python](https://github.com/elastic/elastic-otel-python)
- [Node.js](https://github.com/elastic/elastic-otel-node)
- [Java](https://github.com/elastic/elastic-otel-java)

EDOT includes many types of instrumentation. This [table](https://elastic.github.io/opentelemetry/use-cases/llm/#supported-technologies) lists the supported technologies.

### Getting started

Check [these instructions](https://elastic.github.io/opentelemetry/use-cases/llm/) on how to setup and collect OpenTelemetry data for your LLM applications. 

## Use cases

### Understand LLM performance and reliability

For an SRE team optimizing a customer support system powered by Azure OpenAI, Elastic’s [Azure OpenAI integration](https://www.elastic.co/guide/en/integrations/current/azure_openai.html) provides critical insights. They can quickly identify which model variants experience higher latency or error rates, enabling smarter decisions on model deployment or even switching providers based on real-time performance metrics.

:::{image} /solutions/images/llm-performance-reliability.png
:alt:  LLM performance and reliability
:screenshot:
:::

### Troubleshoot OpenAI-powered applications

Consider an enterprise utilizing an OpenAI model for real-time user interactions. Encountering unexplained delays, an SRE can use OpenAI tracing to dissect the transaction pathway, identify if one specific API call or model invocation is the bottleneck, and monitor a request to see the exact prompt and response between the user and the LLM. 

:::{image} /solutions/images/llm-openai-applications.png
:alt:  Troubleshoot OpenAI-powered applications
:screenshot:
:::

### Addressing cost and usage concerns

For cost-sensitive deployments, being acutely aware of which LLM configurations are more cost-effective is crucial. Elastic’s dashboards, pre-configured to display model usage patterns, help mitigate unnecessary spending effectively. You can use out-of-the-box dashboards for metrics, logs, and traces.

:::{image} /solutions/images/llm-costs-usage-concerns.png
:alt:  LLM cost and usage concerns
:screenshot:
:::

### Understand compliance with guardrails in Amazon Bedrock

With the Elastic Amazon Bedrock integration for Guardrails, SREs can swiftly address security concerns, like verifying if certain user interactions prompt policy violations. Elastic's observability logs clarify whether guardrails rightly blocked potentially harmful responses, bolstering compliance assurance.

:::{image} /solutions/images/llm-amazon-bedrock-guardrails.png
:alt:  Elastic Amazon Bedrock integration for Guardrails
:screenshot:
:::


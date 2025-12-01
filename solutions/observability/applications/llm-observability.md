---
navigation_title: LLM and agentic AI observability
---

# LLM and Agentic AI Observability

While LLMs hold incredible transformative potential, they also bring complex challenges in reliability, performance, and cost management. Traditional monitoring tools require an evolved set of observability capabilities to ensure these models operate efficiently and effectively.
To keep your LLM-powered applications reliable, efficient, cost-effective, and easy to troubleshoot, Elastic provides a powerful LLM observability framework including key metrics, logs, and traces, along with pre-configured, out-of-the-box dashboards that deliver deep insights into model prompts and responses, performance, usage, and costs.
Elastic’s end-to-end LLM observability is delivered through the following methods:

- Metrics and logs ingestion for LLM APIs (via [Elastic integrations](integration-docs://reference/index.md))
- APM tracing for LLM Models (via [instrumentation](opentelemetry://reference/index.md))

## LLM / Agentic Platform Observability

Elastic’s LLM integrations now support the most widely adopted models, including OpenAI, Azure OpenAI, and a diverse range of models hosted on Amazon Bedrock and Google Vertex AI. Depending on the LLM provider you choose, the following table shows which type of data -- log or metrics -- you can collect.

| **LLM and Agentic Platform**  | **Metrics** | **Logs** | 
|--------|------------|------------|
| [Amazon Bedrock](integration-docs://reference/aws_bedrock.md)| ✅ | ✅ |  
| [Amazon Bedrock AgentCore](integration-docs://reference/aws_bedrock_agentcore.md)| ✅ | ✅ |  
| [Azure AI Foundry](integration-docs://reference/azure_ai_foundry.md) | ✅| ✅ | 
| [Azure OpenAI](integration-docs://reference/azure_openai.md)| ✅ | ✅ | 
| [GCP Vertex AI](integration-docs://reference/gcp_vertexai.md) | ✅ | ✅ | 
| [OpenAI](integration-docs://reference/openai.md) | ✅| 🚧 | 


## LLM and agentic AI application observability with APM (distributed tracing)

Elastic offers specialized OpenTelemetry Protocol (OTLP) tracing for applications leveraging LLM models hosted on Amazon Bedrock, OpenAI, Azure OpenAI, and GCP Vertex AI, providing a detailed view of request flows. This tracing capability captures critical insights, including the specific models used, request duration, errors encountered, token consumption per request, and the interaction between prompts and responses. Ideal for troubleshooting, APM tracing allows you to find exactly where the issue is happening with precision and efficiency in your LLM-powered application.

You can instrument the application with one of the following Elastic Distributions of OpenTelemetry (EDOT):

- [Python](https://github.com/elastic/elastic-otel-python)
- [Node.js](https://github.com/elastic/elastic-otel-node)
- [Java](https://github.com/elastic/elastic-otel-java)

EDOT includes many types of LLM instrumentation. This [table](/solutions/observability/get-started/opentelemetry/use-cases/llms/index.md#supported-technologies) lists the supported technologies.

### Getting started

Check [these instructions](/solutions/observability/get-started/opentelemetry/use-cases/llms/index.md) on how to setup and collect OpenTelemetry data for your LLM applications.

## Use cases

### Understand LLM performance and reliability

For an SRE team optimizing a customer support system powered by Azure OpenAI, Elastic’s [Azure OpenAI integration](integration-docs://reference/azure_openai/index.md) provides critical insights. They can quickly identify which model variants experience higher latency or error rates, enabling smarter decisions on model deployment or even switching providers based on real-time performance metrics.

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


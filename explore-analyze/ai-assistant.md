---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/search-ai-assistant.html
  - https://www.elastic.co/guide/en/observability/current/obs-ai-assistant.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-for-security.html
  - https://www.elastic.co/guide/en/serverless/current/observability-ai-assistant.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-assistant.html
  - https://www.elastic.co/guide/en/serverless/current/ai-assistant-knowledge-base.html
---

# AI assistant

$$$token-limits$$$

**AI Assistant** is a chat-based interactive tool to help you with a variety of tasks related to Elasticsearch and Kibana, including:

- **Constructing queries**: Assists you in building queries to search and analyze your data, including converting queries from other languages to [ES|QL](query-filter/languages/esql.md).
- **Indexing data**: Guides you on how to index data into Elasticsearch.
- **Using APIs**: Calls Elasticsearch APIs on your behalf if you need specific operations performed.
- **Generating sample data**: Helps you create sample data for testing and development purposes.
- **Visualizing and analyzing data**: Assists you in creating visualizations and analyzing your data using Kibana.
- **Troubleshooting**: Explains errors, messages, and suggests remediation.

AI Assistant requires specific privileges and a generative AI connector.

% Check [Configure AI Assistant](../deploy-manage/) for more details on how to enable and configure it.

The capabilities and ways to interact with AI Assistant can differ for each solution. Find more information in the respective solution docs:

- [{{obs-ai-assistant}}](../solutions/observability/observability-ai-assistant.md)
- [AI Assistant for Security](../solutions/security/ai/ai-assistant.md)

## Prompt best practices [rag-for-esql]
Elastic AI Assistant allows you to take full advantage of the Elastic platform to improve your operations. It can help you write an ES|QL query for a particular use case, or answer general questions about how to use the platform. Its ability to assist you depends on the specificity and detail of your questions. The more context and detail you provide, the more tailored and useful its responses will be.

To maximize its usefulness, consider using more detailed prompts or asking for additional information. For instance, after asking for an ES|QL query example, you could ask a follow-up question like, “Could you give me some other examples?” You can also ask for clarification or further exposition, for example "Provide comments explaining the query you just gave."

In addition to practical advice, AI Assistant can offer conceptual advice, tips, and best practices for enhancing your security measures. You can ask it, for example:

- “How do I set up a machine learning job in Elastic Security to detect anomalies in network traffic volume over time?”
- “I need to monitor for unusual file creation patterns that could indicate ransomware activity. How would I construct this query using EQL?”

## Your data and AI Assistant [ai-assistant-data-information]
Elastic does not use customer data for model training. This includes anything you send the model, such as alert or event data, detection rule configurations, queries, and prompts. However, any data you provide to AI Assistant will be processed by the third-party provider you chose when setting up the generative AI connector as part of the assistant setup.

Elastic does not control third-party tools, and assumes no responsibility or liability for their content, operation, or use, nor for any loss or damage that may arise from your using such tools. Exercise caution when using AI tools with personal, sensitive, or confidential information. Any data you submit may be used by the provider for AI training or other purposes. There is no guarantee that the provider will keep any information you provide secure or confidential. You should familiarize yourself with the privacy practices and terms of use of any generative AI tools prior to use.

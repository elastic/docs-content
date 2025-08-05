---
navigation_title: Elastic AI SOC Engine
applies_to:
  serverless:
    security: preview
---
# Elastic AI SOC Engine with {{sec-serverless}}

Elastic AI Security Operations Center (SOC) Engine (EASE) is an {{sec-serverless}} project type that provides AI-powered tools and case management to augment third-party SIEM and EDR/XDR platforms. This page describes how to create an {{sec-serverless}} EASE project, how to ingest your data, and how to use its key features.

## Create an EASE project

To create an EASE project:

1. [Create](/solutions/security/get-started/create-security-project.md) an {{sec-serverless}} project, and on the **Confirm your project settings** page, select **Elastic AI SOC Engine**. 

   :::{image} /solutions/images/security-ease-create-ease-project.png
   :alt: The Confirm your project settings page
   :::

2. Click **Create serverless project**, and wait for your project to be provisioned. When it's ready, open it.


## Ingest your SOC data

To ingest your SOC data: 

1. Go to the **Configurations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /solutions/images/security-ease-integrations.png
    :alt: The integrations page of an EASE project
    :::

2. From the **Integrations** tab, select any [integration](integration-docs://reference/index.md) you want to ingest data from to view deployment instructions and more information.

## Select a model

EASE uses LLM connectors to enable its AI features such as Attack Discovery and AI Assistant. The Elastic Managed LLM is enabled by default. You can also [create custom connectors](/solutions/security/ai/set-up-connectors-for-large-language-models-llm.md). Keep in mind that different models [perform differently](/solutions/security/ai/large-language-model-performance-matrix.md) on different tasks. 


## Features

EASE provides a set of capabilities designed to help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond. Once your data is ingested, you can start using the following features:

- **[Attack Discovery](/solutions/security/ai/attack-discovery.md)**: Helps you analyze alerts in your environment and identify threats. Each discovery represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible. 

     :::{image} /solutions/images/security-attck-disc-example-disc.png
     :alt: Attack Discovery detail view
     :::

- **[AI Assistant](/solutions/security/ai/ai-assistant.md)**: An LLM-powered virtual assistant specialized for digital security; it helps with data analysis, alert investigation, incident response, and {{esql}} query generation. You can add custom background knowledge and data to its [knowledge base](/solutions/security/ai/ai-assistant-knowledge-base.md) and use natural language to ask for its assistance with your SOC operations.

- **[Cases](/solutions/security/investigate/cases.md)**: Helps you track and share related information about security issues. Track key investigation details and collect alerts in a central location.

    :::{image} /solutions/images/security-ease-cases.png
    :alt: The Cases page in an EASE project
    :::


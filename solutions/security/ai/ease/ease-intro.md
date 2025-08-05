---
applies_to:
  serverless:
    security: preview
---


# Elastic AI SOC Engine

This page describes Elastic AI SOC Engine (EASE), how to create an EASE project, how to ingest your data into EASE, and how to use its key features. EASE is a {{sec-serverless}} project type specialized to provide AI-powered tools and case management to augment third-party SIEM and EDR/XDR platforms. 

## Create an EASE project

To create an EASE project:

1. [Create](/solutions/security/get-started/create-security-project.md) a {{sec-serverless}} project, and on the **Confirm your project settings** page, select **Elastic AI SOC Engine**. 
2. Click **Create serverless project** and wait for your project to be provisioned. When it's ready, open it.


## Ingest your SOC data

To ingest your SOC data: 

1. Go to the **Configurations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /solutions/images/security-ease-integrations.png
    :alt: The integrations page of an EASE project
    :::

2. From the **Integrations** tab, select any integration you want to ingest data from to view more information about it. Learn more about [{{integrations}}](integration-docs://reference/index.md).


## Features

Ease provides a set of capabilities designed to help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond. Once your data is ingested, you can start using the following features:

- **[Attack Discovery](/solutions/security/ai/attack-discovery.md)**: helps you analyze alerts in your environment and identify threats. Each discovery represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible. 

     :::{image} /solutions/images/security-attck-disc-example-disc.png
     :alt: Attack Discovery detail view
     :::

- **[AI Assistant](/solutions/security/ai/ai-assistant.md)**: an LLM powered virtual assistant specialized for digital security; it helps with data analysis, alert investigation, incident response, and {{esql}} query generation. You can add custom background knowledge and data to its [knowledge base](/solutions/security/ai/ai-assistant-knowledge-base.md), use natural language to ask for its assistance with your SOC operations, and much more.

- **[Cases](/solutions/security/investigate/cases.md)**: helps you track and share related information about security issues. Track key investigation details, collect alerts in a central location, and more. 

    :::{image} /solutions/images/security-ease-cases.png
    :alt: The Cases page in an EASE project
    :::


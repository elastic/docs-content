
# Elastic AI SOC Engine

This page provides an overview of Elastic AI SOC Engine (EASE) and its key features. EASE is a {{serverless}} deployment type specialized to provide AI-powered tools and case management that can augment third-party SIEM and EDR platforms. 

## Get started with EASE

To create an EASE project:
1. [Create](security/get-started/create-security-project.md) a {{sec-serverless}} project, and on the **Confirm your project settings** page, select **Elastic AI SOC Engine**. 
2. Click **Create serverless project** and wait for your project to be provisioned. When it's ready, open it.
3. Use integrations to ingest your alerts to start working with Ease. 

## Features

Ease provides a set of capabilities designed to help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond. Follow the documentation links below to learn more about each feature:

- **[Attack Discovery](/solutions/security/ai/attack-discovery.md)**: helps you analyze alerts in your environment and identify threats. Each discovery represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible. 
    :::{image} /solutions/images/security-attck-disc-example-disc.png
    :alt: Attack Discovery detail view
    :::

- **[AI Assistant](/solutions/security/ai/ai-assistant.md)**: an LLM powered virtual assistant specialized for digital security; it helps with data analysis, alert investigation, incident response, and {{esql}} query generation. You can add custom background knowledge and data to its [knowledge base](/solutions/security/ai/ai-assistant-knowledge-base.md), use natural language to ask for its assistance with your SOC operations, and much more.

- **[Cases](/solutions/security/investigate/cases.md)**: helps you track and share related information about security issues. Track key investigation details, collect alerts in a central location, and more. 
    :::{image} /solutions/images/security-ease-cases.png
    :alt: The Cases page in an EASE deployment
    :::


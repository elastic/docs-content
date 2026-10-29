---
navigation_title: Elastic AI SOC Engine
applies_to:
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---
# Elastic AI SOC Engine with {{sec-serverless}}

Elastic AI SOC Engine (EASE) is an {{sec-serverless}} project type that provides cutting-edge AI-powered tools to augment your existing SIEM and EDR/XDR platforms. Because serverless deployments are quick to deploy and easy to configure, and because all the integrations that you can use to ingest data to EASE can run as [{{managed-integrations}}](/manage-data/ingest/managed-integrations/managed-integrations.md), you can start getting value from EASE in minutes.

This page describes how to create an EASE project, how to ingest your data, and how to use its key features.

## Features

EASE provides a set of capabilities designed to help make the most of each security analyst’s time, fight alert fatigue, and reduce your mean time to respond. Once your data is ingested, you can start using the following features:

- **[Attack Discovery](/solutions/security/ai/attack-discovery/index.md)**: Helps you analyze alerts in your environment and identify threats. Each discovery represents a potential attack and describes relationships among multiple alerts to tell you which users and hosts are involved, how alerts correspond to the MITRE ATT&CK matrix, and which threat actor might be responsible.

     :::{image} /solutions/images/security-attck-disc-example-disc.png
     :alt: Attack Discovery detail view
     :width: 600px
     :::

     You can [schedule](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md#schedule-discoveries) Attack Discovery to run automatically, and notify you of any discoveries through a range of connectors such as Slack, Teams, PagerDuty, or email.

- **[{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md)**: An LLM-powered chat experience for digital security. It helps with data analysis, alert investigation, incident response, and {{esql}} query generation, and includes built-in Security skills, custom agents, and tools. To get started, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md). If your project still uses AI Assistant, refer to [](/explore-analyze/ai-features/ai-chat-experiences/ai-agent-or-ai-assistant.md) to switch.

- **[Cases](/solutions/security/investigate/security-cases.md)**: Helps you track and share related information about security issues. Track key investigation details and collect alerts in a central location.

    :::{image} /solutions/images/security-ease-cases.png
    :alt: The Cases page in an EASE project showing the default state
    :::

- **[Value report](/solutions/security/ai/ease/ease-value-report.md)**:

   :::{include} /solutions/_snippets/value-report-intro.md
   :::

## Create an EASE project

To create an EASE project:

1. [Create](/solutions/security/get-started.md#create-sec-serverless-project) an {{sec-serverless}} project, and on the **Confirm your project settings** page, select **Elastic AI SOC Engine**.

   :::{image} /solutions/images/security-ease-create-ease-project.png
   :alt: The Confirm your project settings page
   :::

2. Click **Create serverless project**, and wait for your project to be provisioned. When it's ready, open it.

## Ingest your SIEM and EDR/XDR data

To ingest third-party security data:

1. Go to the **Configurations** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /solutions/images/security-ease-integrations.png
    :alt: The integrations page of an EASE project
    :width: 600px
    :::

2. From the **Integrations** tab, select a SIEM and EDR/XDR platform from which you want to ingest data to view setup instructions and more information. You can ingest data from:

    * CrowdStrike
    * Elastic Security
    * Google SecOps
    * Microsoft Sentinel
    * SentinelOne
    * Splunk

## Select a model

EASE uses LLM connectors to enable its AI features such as Attack Discovery and {{agent-builder}}. Elastic Managed LLMs are enabled by default. You can also [configure your own third-party LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md). Keep in mind that different models [perform differently](/solutions/security/ai/large-language-model-performance-matrix.md) on different tasks.

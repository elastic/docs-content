---
navigation_title: Automatic Import
description: Automatic Import uses an LLM to build a custom Elastic integration from a sample of your data when no prebuilt integration exists. Learn when to use it and how it works.
type: overview
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/automatic-import.html
  - https://www.elastic.co/guide/en/serverless/current/security-automatic-import.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: security
  - id: observability
---

# Automatic Import [automatic-import]

:::{include} /explore-analyze/_snippets/automatic-import-intro.md
:::

## When to use Automatic Import [automatic-import-when-to-use]

Use the option that fits your data source:

* **A prebuilt integration exists:** Use it. To check, search the [Elastic integrations catalog](integration-docs://reference/index.md).
* **{{agent}} can collect the data from files, cloud storage, Kafka, TCP, UDP, or another [supported method](/explore-analyze/ai-features/automatic-import/create-integration.md#_create_a_new_custom_integration):** Use Automatic Import.
* **The source is an HTTP API, or you need full control of the package:** Use the [Elastic integration skills](https://github.com/elastic/integration-skills) in your AI coding environment to build and test a package, then [upload it to {{kib}}](integrations://extend/upload-new-integration.md). {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` Automatic Import can't collect data from HTTP APIs.

## How Automatic Import works [automatic-import-how-it-works]

An integration has one data stream for each type of data that your source produces. For each data stream, you upload a sample and select how {{agent}} collects the data. The integration doesn't include dashboards.

:::::{applies-switch}

::::{applies-item} { "serverless": "ga", "stack": "ga 9.4+" }

After the LLM analyzes your samples:

1. **Review and approve:** You check the field mappings and the ingest pipeline, adjust the pipeline if needed, and approve the integration. By default, approving also installs it.
2. **Collect data:** You add the integration to an agent policy, and {{agent}} starts collecting the data.
3. **Update:** To change the integration, you edit it and approve a new version. You can edit it only on the cluster or project where you created it. To use it elsewhere, download its package and upload it there.

::::

::::{applies-item} stack: ga 9.0-9.3

Each integration has one data stream. After the LLM analyzes your sample, you select **Add to Elastic** to install the integration, then add it to an agent policy.

::::

:::::

## Requirements [automatic-import-requirements]

* A working [LLM connector](/explore-analyze/ai-features/llm-guides/llm-connectors.md). For model guidance, refer to [Recommended models](#automatic-import-recommended-models).
* The required project feature tier or subscription: [Security Analytics Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md#elastic-sec-project-features) for {{sec-serverless}} projects, [Observability Complete](/deploy-manage/deploy/elastic-cloud/project-settings.md#obs-serverless-project-features) for {{obs-serverless}} projects, or an [Enterprise](https://www.elastic.co/pricing) subscription for {{stack}}.
* {applies_to}`stack: ga 9.4+` The **Automatic Import** feature privilege in {{kib}}.
* To install the integration and add it to an agent policy: The **Integrations** [feature privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md), and **All** for **Fleet** or its **Agent policies** sub-feature.

## Recommended models [automatic-import-recommended-models]

Automatic Import works with any LLM, but results vary by model. Models that perform well for Attack Discovery also perform well for Automatic Import. To compare models, refer to the LLM performance matrices for [{{elastic-sec}}](/solutions/security/ai/large-language-model-performance-matrix.md) and the [{{observability}} AI Assistant](/solutions/observability/ai/llm-performance-matrix.md).

::::{important}
Using Automatic Import allows users to create new third-party data integrations through the use of third-party generative AI models (“GAI models”). Any third-party GAI models that you choose to use are owned and operated by their respective providers. Elastic does not own or control these third-party GAI models, nor does it influence their design, training, or data-handling practices. Using third-party GAI models with Elastic solutions, and using your data with third-party GAI models is at your discretion. Elastic bears no responsibility or liability for the content, operation, or use of these third-party GAI models, nor for any potential loss or damage arising from their use. Users are advised to exercise caution when using GAI models with personal, sensitive, or confidential information, as data submitted can be used to train the models or for other purposes. Elastic recommends familiarizing yourself with the development practices and terms of use of any third-party GAI models before use. You are responsible for ensuring that your use of Automatic Import complies with the terms and conditions of any third-party platform you connect with.
::::

## Next steps [automatic-import-next-steps]

* [Create a custom integration with Automatic Import](/explore-analyze/ai-features/automatic-import/create-integration.md): Prepare a sample, build the integration, and start collecting data.
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` [Manage integrations created with Automatic Import](/explore-analyze/ai-features/automatic-import/manage-integrations.md): Edit an integration or use it on another cluster or project.

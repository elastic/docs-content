---
navigation_title: "Connectors"
description: "Learn about the Agent Builder connectors library, which configures access to external systems for agents."
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Connectors in {{agent-builder}}

:::{note}
:applies_to: stack: preview 9.4+, serverless: preview

The connectors library is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) in {{kib}}.
:::

The {{agent-builder}} connectors library lets you configure action-based connectors that give agents access to external systems, such as messaging services, cloud functions, and third-party APIs.

:::{note}
{{agent-builder}} connectors leverage the underlying {{kib}} [Stack connectors](/deploy-manage/manage-connectors.md) framework to securely store credentials and manage integrations. However, they are distinct from [AI connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md), which are used exclusively to configure external LLM providers.
:::

Connectors are managed at the deployment level from **Manage components** > **Connectors**. They are not assigned per agent. Individual connector types in the catalog may be marked **Technical Preview**.

## How agents use connectors

Unlike standalone tools, {{agent-builder}} connectors do not require manual assignment to agents. {{kib}} makes connector capabilities natively available during conversations through a dynamic schema-attachment model.

When an agent needs to interact with an external system, it automatically reads the schemas of your configured connectors. It then uses a built-in system tool (`platform.core.execute_connector_sub_action`) to independently format API payloads and run specific sub-actions (for example, looking up a Slack channel ID or searching AlienVault OTX for threat intelligence) without any manual tool mapping.

## Add a connector

To register a new connector:

1. In the left sidebar, select **Manage components** > **Connectors**.
2. Select the mosaic to add a connector.
3. Choose a connector type from the catalog.
4. Provide the required configuration.
5. Save the connector.

The configured connector appears in the library and is immediately available for your agents to use dynamically.

## Related pages

- [Tools in {{agent-builder}}](tools.md)
- [Skills in {{agent-builder}}](skills.md)
- [Plugins in {{agent-builder}}](plugins.md)
- [Custom agents](custom-agents.md)

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

The {{agent-builder}} connectors library lets you configure action-based connectors that give agents access to external systems, such as messaging services, cloud functions, and third-party APIs.

Connectors are managed at the deployment level from **Manage components** > **Connectors**. They are not assigned per agent. Individual connector types in the catalogue may be marked **Technical Preview**.


## Add a connector

To register a new connector:

1. In the left sidebar, select **Manage components** > **Connectors**.
2. Select the button to add a connector.
3. Choose a connector type from the catalogue. Individual connector types may be marked as **Technical Preview**.
4. Provide the required configuration.
5. Save the connector.

The configured connector appears in the library.

## Related pages

- [Tools in {{agent-builder}}](tools.md)
- [Skills in {{agent-builder}}](skills.md)
- [Plugins in {{agent-builder}}](plugins.md)
- [Custom agents](custom-agents.md)

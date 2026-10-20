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
:applies_to: stack: preview 9.4-9.5

The connectors library is hidden until you turn on the `agentBuilder:experimentalFeatures` [advanced setting](get-started.md#enable-experimental-features-optional) in {{kib}}.
:::

The {{agent-builder}} connectors library lets you configure action-based connectors that give agents access to external systems, such as messaging services, cloud functions, and third-party APIs.

:::{note}
{{agent-builder}} connectors leverage the underlying {{kib}} [Stack connectors](/deploy-manage/manage-connectors.md) framework to securely store credentials and manage integrations. However, they are distinct from [Generative AI connectors](/explore-analyze/ai-features/llm-guides/llm-connectors.md), which are used exclusively to configure external LLM providers and are deprecated. {{agent-builder}} connectors are not affected by that deprecation.
:::

You manage connectors per {{kib}} space from **Manage components** → **Connectors**. Individual connector types in the catalog can be marked **Technical preview**.

## How agents use connectors

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` An agent can only run the connectors assigned to it. Agents look up connectors and load their sub-actions and parameter schemas at run time through the built-in `connector-discovery` [skill](skills.md), which **Enable Elastic capabilities** includes. To assign connectors, refer to [Assign connectors to an agent](#assign-connectors-to-an-agent).

{applies_to}`stack: preview 9.4-9.5` Unlike standalone tools, connectors don't need to be assigned to agents: any agent can use any connector in the space.

When an agent needs to interact with an external system, it automatically reads the schemas of the connectors available to it. It then uses a built-in system tool (`platform.core.execute_connector_sub_action`) to independently format API payloads and run specific sub-actions (for example, looking up a Slack channel ID or searching AlienVault OTX for threat intelligence) without any manual tool mapping.

## Add a connector

To register a new connector:

1. In the sidebar, select **Manage components** → **Connectors** to open the **Connectors library**.
2. Select **Create connector**.
3. Select a connector type from the catalog.
4. Provide the required configuration.
5. Select **Save**.

The configured connector appears in the library.

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` To let an agent use the connector, [assign it to the agent](#assign-connectors-to-an-agent).

{applies_to}`stack: preview 9.4-9.5` Any agent can use the connector immediately.

## Assign connectors to an agent [assign-connectors-to-an-agent]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

An agent can only use the connectors you assign to it, and new agents start with none. You assign connectors from the agent after you save it.

To assign connectors in {{kib}}, you need permission to edit the agent and the **Actions and Connectors: All** {{kib}} privilege. If **Enable Elastic capabilities** is off for the agent, also assign the built-in `connector-discovery` skill. Without it, the agent can't find its connectors.

To assign a connector to an agent:

1. Select the agent. Then, in the sidebar under **Customize**, select **Connectors**.
2. Select **Add connector**.
3. Select one of the following:
   - **From library**: Assign connectors that already exist in the connectors library.
   - **Create new connector**: Configure a new connector. It's added to the library and assigned to the agent.

To unassign a connector, remove it from the agent's **Connectors** page. The connector stays in the library, and other agents it's assigned to can still use it.

:::{important}
Agents that were never assigned connectors can't use any. This includes:

- The built-in **Elastic AI Agent**.
- Agents created with the [Agents API](kibana-api.md#agents-apis) without `connector_ids`.
- {applies_to}`stack: preview 9.6+` Agents created in 9.4 or 9.5 without a connector list. In those versions, these agents could use any connector. After you upgrade, assign connectors to them.
- {applies_to}`serverless: preview` Existing agents without a connector list, including agents created before new agents started with an empty list. Previously, these agents could use any connector. Assign connectors to them.

Agents that already had a connector list in 9.5 or on {{serverless-short}} can now run only the connectors in that list. Previously, the list limited which connectors an agent could discover, not which ones it could run. Check these agents and assign any connectors they still need.
:::

## Authorize connector access from chat

```{applies_to}
stack: preview 9.5+
serverless: preview
```

When an agent needs access to an OAuth connector, the chat pauses and displays an authorization prompt. Select **Authorize** to open the provider's sign-in flow in a new browser tab. After authorization succeeds, return to the chat, where the agent retries the connector call and continues. Select **Deny** to cancel the call.

If authorization fails or the provider does not return you to {{kib}}, close the provider tab and select **Deny** in the chat. Correct the connector or OAuth configuration, then retry your request. To learn more about this prompt, refer to [Authorize a connector](chat.md#authorize-a-connector).

## Related pages

- [Tools in {{agent-builder}}](tools.md)
- [Skills in {{agent-builder}}](skills.md)
- [Plugins in {{agent-builder}}](plugins.md)
- [Custom agents](custom-agents.md)

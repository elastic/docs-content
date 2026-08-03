---
navigation_title: Use natural language
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Create and edit Elastic Workflows by describing what you want in natural language in Kibana, without writing YAML by hand.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Author workflows with natural language [workflows-natural-language]

Create and edit workflows by describing what you want in plain language. {{kib}} generates and updates the workflow YAML for you, so you can automate outcomes without memorizing step types or Liquid syntax. You can still open the [YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) at any time if you prefer to write definitions by hand.

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

Natural language authoring also requires {{agent-builder}} access and a configured LLM. Refer to [Get started with {{agent-builder}}](/explore-analyze/ai-features/agent-builder/get-started.md) and [Model configuration](/explore-analyze/ai-features/agent-builder/models.md).
::::

Both authoring paths use {{agent-builder}}, but they differ in where you work:

- **In the workflow editor**: A chat sidebar sits beside the YAML. The agent proposes changes directly in the editor, and you accept or decline them before saving.
- **In Agent Chat**: You work in a full-page {{agent-builder}} conversation and save the generated workflow from a preview.

## Author in the workflow editor [workflows-nl-editor]

1. Open **Workflows** from the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then either select **Create workflow** to start a new workflow, or select an existing workflow to change it.
2. For a new workflow, the **Elastic AI Agent** chat sidebar opens automatically beside the YAML editor. For an existing workflow, select the **AI Agent** button in the {{kib}} header to open the sidebar.
3. Describe what you want in the chat sidebar. To build a workflow, name the trigger, data sources, conditions, and any connectors or notifications when you know them, for example: "When a critical alert fires, search for other alerts on the same host in the last hour and post a summary to Slack." To change an existing workflow, describe the change, for example: "Add a `console` step that logs the search hit count."
4. Review the generated YAML. Ask for changes in natural language until the definition matches what you need.
5. Ask the agent to run the workflow draft. You don't need to save first: a prompt such as "run this and show me the output" executes the draft, and "test just the search step" runs a single step against your real data. Ask for a fix if a step fails, and the agent will update the definition in place.
6. Accept or decline each proposed change (or all of them), then select **Save**.

The sidebar runs an {{agent-builder}} conversation, so the exchange is saved to your [conversation history](/explore-analyze/ai-features/agent-builder/chat.md#find-conversation-history) alongside conversations you start elsewhere. When the agent tests a step that has a side effect, such as posting to a connector or writing to an index, it asks you to confirm first. Refer to [Confirm a change](/explore-analyze/ai-features/agent-builder/chat.md#confirm-a-change).

## Create a workflow from Agent Chat [workflows-nl-agent-chat]

You can also create a workflow without opening **Workflows** first. Describe the automation in a full-page {{agent-builder}} conversation, refine the draft, then open **Preview** and select **Save** (or **Override** if you are replacing an existing workflow).

For the full Agent Chat procedure, refer to [Create skills and workflows in chat](/explore-analyze/ai-features/agent-builder/chat.md#create-skills-and-workflows-directly-from-chat).

## Next steps [workflows-nl-next]

- Start a [test run](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md#workflows-test-vs-production-runs) from the workflow editor to verify the workflow before you enable production triggers.
- [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md) to review runs and troubleshoot failures.
- Explore [AI-augmented workflows](/explore-analyze/workflows/use-cases/ai-augmented-workflows.md) for patterns that combine workflows with agents at runtime.

## Related pages [workflows-nl-related]

- [Use the YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md): Editor layout, validation, and test versus production runs.
- [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md): Hands-on tutorial with sample data.
- [Create skills and workflows in chat](/explore-analyze/ai-features/agent-builder/chat.md#create-skills-and-workflows-directly-from-chat): Agent Chat creation flow.
- [Connect agents and workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): How {{agent-builder}} and Elastic Workflows work together.
- [Manage and organize workflows](/explore-analyze/workflows/authoring-techniques/manage-workflows.md): Find, edit, enable, and run workflows from the **Workflows** page.

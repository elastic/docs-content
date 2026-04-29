---
navigation_title: AI-augmented workflows
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Combine Elastic Workflows with Agent Builder to build AI-augmented workflows that pair deterministic steps with agent reasoning.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# AI-augmented workflows [workflows-build-ai-automation]

Workflows and {{agent-builder}} are complementary. Workflows give you deterministic, auditable, event-driven automation: the steps always run in the same order and produce the same kind of result. {{agent-builder}} agents give you reasoning: the ability to interpret unstructured context, classify signals, and generate natural-language summaries. Combining the two lets you build automation that's both reliable and intelligent.

The integration runs in both directions: a workflow can call an agent as a step, and an agent can trigger a workflow as a tool.

## What you can build [workflows-ai-patterns]

- **Call an agent from a workflow.** Use the [`ai.agent` step](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) to invoke any agent built in {{agent-builder}}. The agent sees the workflow's data through template variables, performs its reasoning, and returns a response that subsequent steps can act on. Refer to [Call {{agent-builder}} agents from Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md) for the full `ai.agent` reference and examples.
- **Trigger a workflow from an agent.** Create a [workflow tool](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md) in {{agent-builder}} and assign it to an agent. The agent can then invoke the workflow from a conversation, extracting the needed inputs from the user's message and surfacing the workflow's output in chat.
- **Classify and route with AI.** Pair [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify) with [`switch`](/explore-analyze/workflows/steps/switch.md) to send each alert, ticket, or signal down a different branch based on a model's categorization.
- **Summarize evidence before action.** Use [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) to turn gathered evidence into a concise summary for a case description, notification body, or reviewer prompt.
- **Gate AI decisions on human review.** Pair AI classification with [human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md) to show the model's output to an analyst before the workflow takes action.
- **Send structured prompts to an LLM.** Use the [`ai.prompt` step](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) with any [configured AI connector](/deploy-manage/manage-connectors.md) to run classification, extraction, or summarization without going through an agent.
- **Compose reusable AI building blocks.** Extract repeated AI step sequences into a [child workflow](/explore-analyze/workflows/steps/composition.md) that parent workflows invoke with `workflow.execute`.

## When to use each direction [workflows-ai-when-to-use]

- Use **agent-from-workflow** when the workflow already knows what it's doing and needs AI only to reason over a specific data set. For example, summarizing an alert, classifying severity, or extracting fields from unstructured text.
- Use **workflow-from-agent** when the user (or another agent) is in a conversation and wants to trigger a deterministic procedure. For example, isolating a host, opening a case, or running a set of enrichment queries.

## Learn more

- [AI steps reference](/explore-analyze/workflows/steps/ai-steps.md): `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent` parameters and output structure.
- [Composition steps](/explore-analyze/workflows/steps/composition.md): Invoke child workflows and emit outputs.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Pause a workflow for reviewer input.
- [Call {{agent-builder}} agents from Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): End-to-end guide for invoking agents from workflow steps.
- [Workflow tools in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/tools/workflow-tools.md): Configure an agent to trigger a workflow.
- [{{agent-builder}} overview](/explore-analyze/ai-features/elastic-agent-builder.md): Concepts, tools, and agent types.

% Ben Ironside Goldstein, 2026-04-16: Planned child pages per Vision doc Section 4.2:
% - "Calling an agent from a workflow" (workflow-author how-to, distinct from Agent Builder's existing page)
% - "Designing a workflow for agent invocation" (how-to for workflow authors building tools)
% - Pattern A tutorial: workflow calls an Agent Builder agent for alert triage
%   (specific agent/skill to be confirmed once the 9.4 skills model in PR #5904 lands)
% - Pattern B tutorial: agent triggers workflow from chat
% - Pattern C tutorial (observability-specific) deferred pending Obs team engagement

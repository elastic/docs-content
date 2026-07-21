---
navigation_title: Run from Agent Builder
description: "For SOC analysts who investigate in chat: run Attack Discovery from an Agent Builder conversation."
applies_to:
  stack: ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery from {{agent-builder}} [run-attack-discovery-from-agent-builder]

When you investigate in chat with the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent), the `attack-discovery-generator` skill can run Attack Discovery as part of the answer. The skill gathers and cross-checks evidence from other Security skills, then runs the same Attack Discovery analysis used by manual, scheduled, and workflow triggers, and returns a report in the conversation.

This page covers prerequisites, a first chat flow, what the report can include, and how gap closure and run status checks work. For example prompts and how this skill fits other Security use cases, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md#attack-discovery-generation). If you are building automation that runs without a person in the loop, use [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md).

## Before you begin [run-ad-conversation-before-you-begin]

To run Attack Discovery from {{agent-builder}}, you need:

* [{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) available in {{elastic-sec}}. {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` It is the default chat experience.
* The [`securitySolution:enableAttackDiscoveryWorkflows`](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
* The `attack-discovery-generator` skill enabled on the Elastic AI Agent. For how to assign skills, refer to [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md) and [Elastic AI Agent, skills, and tools in {{elastic-sec}}](/solutions/security/ai/agent-builder/skills-model.md).
* The privileges described in [Grant access to Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md).

Conversations and their results are private to the person who started them. There is no cross-user sharing or visibility control yet.

## Try it [run-ad-conversation-try-it]

Skills can activate automatically from your prompt, when you invoke one with a slash command, or when you attach context that matches a skill. These steps assume the agent selects `attack-discovery-generator` from your prompt.

1. Open {{agent-builder}} in {{elastic-sec}} and chat with the Elastic AI Agent.
2. Ask the agent to investigate, for example: `Investigate lateral movement involving host-12 over the last 24 hours.`
3. Review the report in the conversation. It can include summary statistics, a narrative for each discovery, supporting evidence, an attack-flow graph, and a link to the saved discovery.
4. Open the saved discovery from that link, or continue triage in the [Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

More example prompts, including run status and detection-gap approval, are in [Attack Discovery generation](/solutions/security/ai/agent-builder/skills-use-cases.md#attack-discovery-generation).

## How it works [run-ad-conversation-how-it-works]

The `attack-discovery-generator` skill first gathers and cross-checks evidence on its own. It can pull from other skills such as threat hunting, entity analytics, alert analysis, threat intelligence, and the knowledge base. Only then does it run the same analysis steps used by every other Attack Discovery trigger.

Each time the Attack Discovery skill runs, {{agent-builder}} opens a **new** conversation for that run. Manual and scheduled runs from the Attacks view do the same when the skill is involved.

Separate skills power AI-assisted query editing and [run troubleshooting](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md) on the Attacks view. Those skills diagnose or refine configuration. They do not replace `attack-discovery-generator`.

## Close detection gaps [run-ad-conversation-gap-closure]

If the skill finds a gap, such as an important event in a confirmed attack that had no matching alert, it proposes a specific detection rule. It waits for your explicit approval in the chat before creating anything. For example: `The skill proposed a detection rule for a gap. Create it.`

## Check on a run [run-ad-conversation-check-status]

You can ask about the status of a run using its execution ID without starting a new one, for example: `What's the status of Attack Discovery run <execution-id>?`

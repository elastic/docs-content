---
navigation_title: Run from Agent Builder
description: "Run Attack Discovery from an Agent Builder conversation."
applies_to:
  stack: ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery from {{agent-builder}} [run-attack-discovery-from-agent-builder]

When you chat with the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent), the `attack-discovery-generator` skill can run Attack Discovery as part of the answer. The skill gathers and cross-checks evidence from other Security skills, then runs the same analysis used by other Attack Discovery triggers and returns a report in the conversation.

For example prompts, refer to [Security use cases for {{agent-builder}}](/solutions/security/ai/agent-builder/skills-use-cases.md#attack-discovery-generation). For automation without a person in the loop, use [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md).

## Before you begin [run-ad-conversation-before-you-begin]

To run Attack Discovery from {{agent-builder}}, you need:

* The [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
* A role with the [index privileges](/solutions/security/ai/attack-discovery/grant-access.md#ad-index-privileges) required to generate and read discoveries, and these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) at minimum:
  * **Security > Attack discovery**: `All`
  * **Security > Rules and Exceptions**: `Read`
  * **Security > Alerts**: `Read`

:::{note}
Conversations and their results are private to the person who started them.
:::


## Start an investigation in chat [run-ad-conversation-try-it]

Skills can activate automatically from your prompt, when you invoke one with a slash command, or when you attach matching context. These steps assume the agent selects `attack-discovery-generator` from your prompt.

1. Open {{agent-builder}}.
2. Ask the agent to investigate: `Investigate lateral movement involving host-12 over the last 24 hours.`
3. Review the report in the conversation. It can include summary statistics, a narrative for each discovery, supporting evidence, an attack-flow graph, and a link to the saved discovery.
4. Open the saved discovery, or continue triage in the [Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

More example prompts are in [Attack Discovery generation](/solutions/security/ai/agent-builder/skills-use-cases.md#attack-discovery-generation).

## How the `attack-discovery-generator` skill works [run-ad-conversation-how-it-works]

The `attack-discovery-generator` skill first gathers and cross-checks evidence. It can pull from other skills such as threat hunting, entity analytics, alert analysis, threat intelligence, and the knowledge base. Then it runs the same analysis steps used by every other Attack Discovery trigger.

Runs started from chat stay in the current conversation. Manual, scheduled, and workflow-triggered runs open a separate {{agent-builder}} conversation you can audit later.

Related skills on the Attacks view do not replace `attack-discovery-generator`:

* `attack-discovery-alert-retrieval-builder` powers **Edit with AI** in Attack Discovery settings.
* `attack-discovery-workflow-troubleshooting` powers [AI troubleshooting](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md) for failed runs.

## Approve detection rule proposals for gaps [run-ad-conversation-gap-closure]

If the skill finds a gap, such as an important event in a confirmed attack that had no matching alert, it proposes a detection rule in the conversation and waits for your approval before creating anything. Reply in chat to approve (for example, `create the rule`) or to refine the proposal first. The agent uses the `detection-rule-edit` skill only after you approve.

The same gap-closure flow is available from the {{agent-builder}} conversation that manual and scheduled runs open. From **Workflow execution details**, select **Open conversation**.

## Check the status of an Attack Discovery run [run-ad-conversation-check-status]

To check an existing run without starting a new Attack Discovery analysis, ask about it by execution ID, for example: `What's the status of Attack Discovery run <execution-id>?`

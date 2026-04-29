---
navigation_title: Agents, skills, and tools
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Understand how the Elastic AI Agent, Security skills, and tools work together in Elastic Agent Builder for Elastic Security.
---

# Elastic AI Agent, skills, and tools in {{elastic-sec}} [elastic-ai-agent-skills-model]

Starting in version 9.4, {{elastic-sec}} centers on a single default [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) that you extend with modular *skills*. Each skill packages domain-specific instructions, a curated set of [tools](/explore-analyze/ai-features/agent-builder/tools.md), and context for a SOC workflow so you don't switch between separate agents for hunting, triage, or response.

## How the pieces fit together

| Layer | What it is | In {{elastic-sec}} |
|-------|------------|-------------------|
| Agent | The AI you chat with. It reasons, follows instructions, and uses tools. | The default is the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent). |
| Skill | Specialized instructions, tools, and context for one domain. | Security skills you can enable, such as threat hunting or alert triage. |
| Tool | A specific action the agent can run, such as querying data, opening a case, or running a workflow. | [Built-in tools](/explore-analyze/ai-features/agent-builder/tools/builtin-tools-reference.md) shared across skills — the same tool can appear in more than one skill. |

You talk to the agent in natural language. The agent picks tools based on your request, the skills you turned on, and its instructions. You don't invoke tools directly.

## Where to manage skills

Refer to [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md) and [Agents](/explore-analyze/ai-features/agent-builder/agent-builder-agents.md) for how to assign skills to an agent in the {{kib}} UI or via the Skills APIs.

## Relationship to the standalone Threat Hunting Agent

In {{stack}} 9.3 and earlier {{agent-builder}} documentation, {{elastic-sec}} documented a separate Threat Hunting Agent built-in agent. That standalone agent is deprecated starting in 9.4. Threat hunting workflows now use the Elastic AI Agent with the Threat Hunting skill enabled. For migration guidance, refer to the [Threat Hunting Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#threat-hunting-agent) section in the built-in agents reference.

## Frequently asked questions

### How is this different from Elastic AI Assistant?

[Elastic AI Assistant](/solutions/security/ai/ai-assistant.md) is the legacy in-product assistant embedded across {{elastic-sec}} workflows. {{agent-builder}} is the platform for configurable agents, tools, and skills. Skills and tools in {{agent-builder}} replace the older split between broad capabilities and one-off workflows. For how skills relate to tools and prompts, refer to [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md).

### Can I use more than one skill in a conversation?

You can enable multiple skills for the agent. The agent decides which skill context and tools apply based on your request.

### Can I create custom Security skills?

Yes. For supported deployment tiers and how to author your own skill, refer to [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md) and the [Skill creation guidelines](/explore-analyze/ai-features/agent-builder/skill-creation-guidelines.md).

## Related pages

- [Agent Builder for {{elastic-sec}}](agent-builder.md)
- [Security skills use cases](skills-use-cases.md)
- [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md)
- [Built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md)
- [Skill creation guidelines](/explore-analyze/ai-features/agent-builder/skill-creation-guidelines.md)
- [Built-in agents reference](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md)
- [Tools in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/tools.md)

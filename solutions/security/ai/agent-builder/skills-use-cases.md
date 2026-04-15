---
navigation_title: Security skills use cases
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Example prompts and outcomes for Elastic AI Agent skills in Elastic Security, with links to the skills model and built-in reference.
---

# Security skills use cases [security-skills-use-cases]

This page gives example conversations for out-of-the-box Security skills on the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent). For definitions of agents, skills, and tools, start with [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md). For skill IDs, tooling, and lifecycle badges, see the built-in skills reference in {{agent-builder}} when that page publishes (in progress).

% [Built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md)

:::{note}
Names and availability of built-in skills can change between releases. Confirm the exact labels in the Agent Builder UI and with @dhru42 before publishing customer-facing announcements.
:::

## Threat Hunting

| Example prompt | What the agent can do |
|----------------|----------------------|
| Hunt for lateral movement from `srv-01` in the last 7 days | Run {{esql}} and pivots across authentication and network data, relate entities, and enrich with threat intelligence. |
| Sweep for a file hash or indicator across recent events | Search relevant indices, summarize hits, and suggest next pivots. |

## Detection Engineering

| Example prompt | What the agent can do |
|----------------|----------------------|
| Create a rule to detect PowerShell downloading from external URLs | Draft or refine {{esql}} detection logic, sanity-check fields, and map to [MITRE ATT&CK](https://attack.mitre.org/){:target="_blank"} where appropriate. |
| Find coverage gaps for technique T1059 | Compare existing rules to MITRE coverage and suggest additions. |

## Alert Triage

| Example prompt | What the agent can do |
|----------------|----------------------|
| What's the context on this critical alert? | Pull alert details, entity risk, related intel, and baseline context; suggest triage outcomes. |
| Should we escalate this alert? | Summarize evidence and recommend escalate, investigate further, or close. |

## Case Management

| Example prompt | What the agent can do |
|----------------|----------------------|
| Open a case for this incident and attach evidence | Create or update a [case](/explore-analyze/cases.md), set severity, and link alerts or artifacts. |
| Add the last 24 hours of related alerts to the case | Gather context and attach it to the case record. |

## Incident Response

| Example prompt | What the agent can do |
|----------------|----------------------|
| Isolate this host and document what we know | Confirm high-impact actions (such as host isolation), capture steps, and align with response playbooks. |
| Notify the team and open a war-room case | Create cases, summarize findings, and suggest notifications or escalations. |

## Rule Management

| Example prompt | What the agent can do |
|----------------|----------------------|
| Disable rules with more than 50% false positives this week | Use rule metrics and bulk actions where available; document changes. |
| List exceptions that might be too broad | Review exception lists and highlight risk. |

## Reverse Engineering

| Example prompt | What the agent can do |
|----------------|----------------------|
| Summarize what this binary is doing based on these fields | Interpret artifacts and logs, tie behavior to MITRE techniques, and suggest collection gaps. |
| What IOCs should we extract from this sample? | List indicators and enrichment paths. |

## Related pages

- [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md)
- [Agent Builder for {{elastic-sec}}](agent-builder.md)
% [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md)

% @dhru42: Confirm final OOTB skill names, preview vs GA per skill, Enterprise custom-skills messaging, and skill selector screenshots before GA.

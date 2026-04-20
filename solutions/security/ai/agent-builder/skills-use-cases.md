---
navigation_title: Security use cases
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Example prompts for common Elastic Security workflows in Agent Builder, with the built-in skills each workflow uses.
---

# Security use cases for {{agent-builder}} [security-skills-use-cases]

This page shows example conversations with the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) for common {{elastic-sec}} workflows. Each section names the built-in Security skill (or skills) to enable for that workflow and gives example prompts. For what each skill does, refer to the [Built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md). For how agents, skills, and tools fit together, start with [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md).

Skills can be activated three ways: the agent selects one automatically from your prompt, you invoke one explicitly with a slash command (for example, `/threat-hunting`), or you attach context (such as an alert from the alert flyout) that activates the matching skill. These examples assume the agent is selecting automatically unless otherwise noted.

## Alert triage and investigation

**Enable:** `alert-analysis` (optionally combine with `entity-analytics` for deeper entity context)

Use this workflow to triage a specific alert or work through an alert queue. The agent fetches the alert, finds related alerts that share entities, correlates with {{elastic-sec}} Labs threat intelligence, and recommends a disposition (true positive, benign true positive, false positive, or needs more data).

| Example prompt | What the agent can do |
|----------------|----------------------|
| What's the context on this critical alert? | Pull alert details, find alerts that share host, user, or IP entities within a time window, and correlate with threat intelligence. |
| Find alerts related to this one over the last 7 days | Search for alerts sharing `host.name`, `user.name`, `source.ip`, or `destination.ip` with the source alert. |
| Should we escalate this alert? | Summarize evidence, check entity risk scores for involved hosts and users, and recommend a disposition with supporting reasoning. |

:::{tip}
You can also trigger this skill by attaching an alert from the alert flyout — the agent activates `alert-analysis` automatically based on the attachment.
:::

## Entity risk investigation

**Enable:** `entity-analytics`

Use this workflow to find risky entities or profile specific hosts, users, services, or generic entities. The agent returns normalized risk scores (0-100), risk levels, asset criticality, watchlists, and behavioral history, and can analyze changes over time.

| Example prompt | What the agent can do |
|----------------|----------------------|
| Which users have the highest risk scores? | Return top N users sorted by normalized risk score, with risk level and asset criticality. |
| Has `host-12`'s risk score changed significantly in the last 90 days? | Compare current and historical risk scores, flag changes greater than 20 points as significant, and summarize what drove the change. |
| What are the riskiest hosts that are high-impact assets? | Filter for entities with criticality `high_impact` or `extreme_impact` and sort by risk score. |

## Threat hunting

**Enable:** `threat-hunting` (optionally combine with `entity-analytics` and `find-security-ml-jobs`)

Use this workflow for hypothesis-driven hunts. The agent runs iterative {{esql}} queries, establishes baselines, searches for IOCs, and flags anomalies. It ships with query templates for lateral movement, C2 beaconing, brute force, and rare process starts.

| Example prompt | What the agent can do |
|----------------|----------------------|
| Hunt for lateral movement from `srv-01` in the last 7 days | Run {{esql}} queries across process, authentication, and network data; identify pivots; and enrich with threat intelligence. |
| Sweep for file hash `abc123...` across recent events | Search relevant indices for IOCs, summarize matches, and suggest next pivots. |
| Look for C2 beaconing from hosts in the DMZ | Apply the C2 beaconing template — periodic connection analysis, rare DNS queries — over a 7-day window. |

## Anomaly investigation with {{ml-app}}

**Enable:** `find-security-ml-jobs`

Use this workflow to investigate anomalies surfaced by Security {{ml-app}} jobs: abnormal access patterns, lateral movement, unexpected logins from new geographies, suspicious external domain activity, and large data transfers. The agent identifies relevant active jobs, queries `.ml-anomalies-*`, and summarizes findings.

| Example prompt | What the agent can do |
|----------------|----------------------|
| Any unusual logins or access patterns in the last 24 hours? | Find relevant active {{ml-app}} jobs, query for anomalies that exceed the configured score threshold, and summarize with entity context. |
| Show users who downloaded unusually large amounts of data | Use data exfiltration-related jobs (for example, `high_sent_bytes_destination_ip`, `high_bytes_written_to_external_device`), query anomaly records, and present results in a table. |
| Which {{ml-app}} jobs should I turn on for lateral movement detection? | Recommend relevant jobs that aren't currently running for the requested investigation. |

## Detection engineering

**Enable:** `detection-rule-edit`

Use this workflow to create or edit detection rules. The skill supports **{{esql}} rules only**. It creates rules from natural language and edits fields such as severity, tags, MITRE ATT&CK mappings, schedule, query, and index patterns. Edits are applied to a rule attachment in the conversation — the agent modifies the attachment rather than describing the change.

| Example prompt | What the agent can do |
|----------------|----------------------|
| Create an {{esql}} rule that detects PowerShell downloading from external URLs | Draft the rule with query, severity, risk score, and MITRE ATT&CK mappings, then render it as an attachment. |
| Raise the severity on this rule to critical and add the T1059 tag | Update the attached rule's `severity`, `risk_score`, and `tags` fields and re-render the attachment. |
| Add the Execution tactic (TA0002) and technique T1059.001 to this rule | Append entries to the rule's `threat` array with correct tactic, technique, and subtechnique IDs. |

## Elastic Defend troubleshooting

```{applies_to}
stack: preview 9.4
serverless:
  security: preview
```

**Enable:** `automatic_troubleshooting`

Use this workflow to diagnose [Elastic Defend](/solutions/security/configure-elastic-defend.md) configuration issues: endpoints not reporting, policy response failures, agent enrollment problems, or incompatible antivirus. The agent queries endpoint data, inspects Elastic Defend package configuration, and produces structured findings with specific endpoint IDs and remediation steps.

| Example prompt | What the agent can do |
|----------------|----------------------|
| Why isn't this endpoint showing up in my endpoint list? | Query agent and endpoint indices for enrollment and check-in evidence; flag the root cause and remediation. |
| Which endpoints are reporting policy response failures? | Search for policy response errors or warnings across endpoints and summarize affected endpoint IDs. |
| Is there any incompatible antivirus on my managed hosts? | Inspect endpoint data for known antivirus conflicts and recommend resolution steps. |

## Related pages

- [Elastic AI Agent, skills, and tools in {{elastic-sec}}](skills-model.md)
- [Agent Builder for {{elastic-sec}}](agent-builder.md)
- [Built-in skills reference](/explore-analyze/ai-features/agent-builder/builtin-skills-reference.md)
- [Skills in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/skills.md)

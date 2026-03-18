---
navigation_title: Investigation tools
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/investigations-tools.html
  - https://www.elastic.co/guide/en/serverless/current/security-investigate-events.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Use Elastic Security investigation tools to triage alerts, trace threats to their root cause, interrogate live hosts, and coordinate your SOC team's incident response.
---

# Investigate security events [security-investigate-events]

When {{elastic-sec}}'s [detection engine](/solutions/security/detect-and-alert.md) creates an alert, you need to understand what happened: the threat's scope, root cause, and impact. {{elastic-sec}} provides a range of tools for this purpose, from an interactive event workspace and forensic visualizers to live host interrogation and collaborative case management.

Together, these tools let you move from a single alert to a complete picture of an incident without leaving {{kibana}}. You can correlate events across data sources in [Timeline](/solutions/security/investigate/timeline.md), trace process execution chains with the [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md), inspect running hosts with [Osquery](/solutions/security/investigate/osquery.md), and document findings in [Cases](/solutions/security/investigate/security-cases.md) and [Notes](/solutions/security/investigate/notes.md). [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) can help you interpret alerts, generate queries, and suggest next steps throughout your investigations.

## Where to start [investigation-where-to-start]

| Your goal | Start here |
|---|---|
| Investigate an alert or hunt for threats | [Timeline](/solutions/security/investigate/timeline.md) |
| Trace a process to its root cause | [Visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md) |
| Review a Linux session for suspicious activity | [Session View](/solutions/security/investigate/session-view.md) |
| Audit live host state during an incident | [Osquery](/solutions/security/investigate/osquery.md) → [Run live queries from alerts](/solutions/security/investigate/run-osquery-from-alerts.md) |
| Correlate alerts with known threat intelligence | [Indicators of compromise](/solutions/security/investigate/indicators-of-compromise.md) |
| Track and coordinate an incident across your team | [Cases](/solutions/security/investigate/security-cases.md) |
| Identify coordinated attacks across many alerts | [Attack discovery](/solutions/security/ai/attack-discovery.md) |
| Use AI to accelerate your investigation | [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md)  |

## How investigation tools work together [investigation-workflow]

Investigation typically follows a progression from initial triage to documented resolution:

1. **Triage the alert.** The detection engine generates an alert. You open it to review the alert details, severity, and affected entities. [Attack discovery](/solutions/security/ai/attack-discovery.md) can help you prioritize by identifying coordinated attacks that span multiple alerts.
2. **Explore context in Timeline.** Add the alert to a Timeline and query related events using KQL, EQL, or {{esql}}. Correlate data across hosts, users, and network activity to understand the broader event sequence.
3. **Dive into forensic detail.** Use the visual event analyzer to inspect the process tree that led to the alert, or use Session View to review full Linux sessions, including terminal output and user activity.
4. **Interrogate the live environment.** Run Osquery against affected hosts to check running processes, open ports, installed software, and other OS-level context that helps confirm or rule out compromise.
5. **Cross-reference threat intelligence.** Check indicators of compromise to learn whether observed artifacts (IPs, domains, file hashes) match known threats.
6. **Document and collaborate.** Attach your findings to Notes on alerts and events, and organize everything in a Case. Cases integrate with external ticketing systems like Jira and ServiceNow for cross-team coordination.

[Chatting with AI](/explore-analyze/ai-features/ai-chat-experiences.md) can accelerate any stage of this workflow by helping you interpret alert data, generate queries, and suggest next steps.

## Investigation tools [investigation-tools-overview]

### Timeline [investigation-timeline]

[Timeline](/solutions/security/investigate/timeline.md) is the central workspace for investigations and threat hunting. You can add alerts from multiple indices, drag fields from tables and histograms across the {{security-app}}, and build complex queries using KQL, EQL, or {{esql}}. Use the **Correlation** tab to write EQL sequence queries that reveal ordered attack patterns across event categories, or use the **{{esql}}** tab for flexible, pipe-based data exploration.

You can also create [Timeline templates](/solutions/security/investigate/timeline-templates.md) and attach them to detection rules so that alerts automatically open with the right filters applied.

### Attack discovery [investigation-attack-discovery]

[Attack discovery](/solutions/security/ai/attack-discovery.md) uses large language models to analyze alerts in your environment and identify threats spanning multiple alerts. Each discovery describes relationships among alerts, maps them to the MITRE ATT&CK matrix, identifies involved users and hosts, and suggests which threat actor might be responsible. Use Attack discovery to cut through alert fatigue, prioritize the incidents that matter most, and reduce your mean time to respond.

### Visual event analyzer [investigation-visual-analyzer]

The [visual event analyzer](/solutions/security/investigate/visual-event-analyzer.md) displays a graphical, process-based timeline of the events that led up to an alert and the events that followed it. Each node represents a process, and you can expand the tree to examine child processes, associated alerts, and related events. This is particularly useful for understanding lateral movement, privilege escalation, and multi-stage attacks.

### Session View [investigation-session-view]

[Session View](/solutions/security/investigate/session-view.md) presents Linux process data in a terminal-inspired, tree-like display organized by parentage and execution time. It shows interactive and non-interactive processes, user information (including privilege escalation), process and network alerts in context, and captured terminal output. 

### Osquery [investigation-osquery]

[Osquery](/solutions/security/investigate/osquery.md) lets you query operating systems like a database using SQL. Run live queries against one or more hosts to inspect processes, files, network connections, installed packages, and hundreds of other OS-level attributes. You can also schedule query packs to capture changes over time, save queries to build a reusable library, and [run live queries directly from alerts](/solutions/security/investigate/run-osquery-from-alerts.md) or [investigation guides](/solutions/security/investigate/run-osquery-from-investigation-guides.md) to streamline triage.

### Indicators of compromise [investigation-indicators]

The [Indicators](/solutions/security/investigate/indicators-of-compromise.md) page collects data from your enabled threat intelligence feeds and provides a centralized view of indicators of compromise (IoCs). Use it to search, filter, and examine indicator details, then cross-reference them with your investigation data. Indicators integrate with [indicator match rules](/solutions/security/detect-and-alert/indicator-match.md) in the detection engine to automatically surface alerts when known threats appear in your environment.

### Cases [investigation-cases]

[Cases](/solutions/security/investigate/security-cases.md) let you track incidents, attach alerts and events, document findings, and collaborate with your SOC team in one place. You can link Timelines to preserve investigation context, attach threat intelligence indicators, and view metrics that summarize alert scope and response times. Cases integrate with Jira, ServiceNow, and IBM Resilient so you can escalate and track incidents across your security workflow.

### Notes [investigation-notes]

[Notes](/solutions/security/investigate/notes.md) let you attach written findings to individual alerts, events, and Timelines. Use notes to document what you've observed, coordinate with other analysts, and build a record of investigative reasoning that persists alongside your data. You can manage all notes from the Notes page, where you can search, filter, and review notes across your investigations.

## Related capabilities [investigation-related]

Several other {{elastic-sec}} features complement the investigation tools described on this page:

* [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) helps you interpret alerts, generate queries, and get contextual guidance throughout your investigation.
* [Entity analytics](/solutions/security/advanced-entity-analytics.md) provides risk scores and behavioral anomaly detection for hosts, users, and services, giving you additional context when evaluating the significance of an alert.
* [{{esql}} for security](/solutions/security/esql-for-security.md) describes how to use the Elasticsearch Query Language across the {{security-app}}, including in Timeline.

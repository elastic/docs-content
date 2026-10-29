---
navigation_title: Glossary
description: Reference of terms used across AlertZero documentation, with links to the pages that explain them.
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# {{alertzero}} glossary [alertzero-glossary]

This glossary defines the terms you see in {{alertzero}} and its documentation. Each entry links to the page that explains it in more detail, where one exists.

## A-B [alertzero-glossary-a-b]

### {{alertzero}} [alertzero-glossary-alertzero]

The agentic layer of {{elastic-sec}}. AI-powered [{{az-workers}}](#alertzero-glossary-worker), grouped into [{{az-watches}}](#alertzero-glossary-watch), triage alerts, hunt for threats, tune detection rules, and investigate attacks, then bring you the [{{az-proposed-actions}}](#alertzero-glossary-proposed-action) that need a person to decide. Refer to [](index.md).

### {{az-assisted}} ({{az-autonomy}}) [alertzero-glossary-assisted]

An [{{az-autonomy}}](#alertzero-glossary-autonomy) level at which a {{az-worker}} starts its analysis on its own, without asking you first, but still waits for your approval before it makes any change. For example, {{az-rule-tuning}} analyzes a noisy rule on its own and drafts a tuning change, then waits for you to approve the change. Refer to [](configure-worker-settings.md).

### Attack Discovery [alertzero-glossary-attack-discovery]

An {{elastic-sec}} feature that uses large language models (LLMs) to group related alerts into attack narratives. In {{alertzero}}, {{az-attack-discovery}} is also the name of a [{{az-worker}}](#alertzero-glossary-worker) in the [{{az-triage-watch}}](#alertzero-glossary-triage-watch). It runs on a schedule, opens an [{{az-investigation}}](#alertzero-glossary-investigation) for each candidate attack, and proposes handing attacks it confirms, or can't rule out, to the [{{az-forensics-watch}}](#alertzero-glossary-forensics-watch). Refer to [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) and [](watches-and-workers.md#alertzero-triage-watch).

### {{az-autonomy-cap}} [alertzero-glossary-autonomy]

A {{az-worker}} setting that controls how far the {{az-worker}} goes on its own before it waits for a person. Each {{az-worker}} offers some of these levels: [{{az-manual}}](#alertzero-glossary-manual), [{{az-assisted}}](#alertzero-glossary-assisted), and [{{az-supervised}}](#alertzero-glossary-supervised). Every {{az-worker}} starts at {{az-manual}}. Refer to [](configure-worker-settings.md).

### {{az-balanced-models}} [alertzero-glossary-balanced-models]

A model setting in **Feature Settings** for {{alertzero}} calls where accuracy matters, but that run often or use tools over many steps, such as triaging alerts or diagnosing a noisy rule. Choose a strong mid-size model. Refer to [{{az-efficient-models}}](#alertzero-glossary-efficient-models) and [{{az-frontier-models}}](#alertzero-glossary-frontier-models).

## C-D [alertzero-glossary-c-d]

### {{az-cyber-domain-models}} [alertzero-glossary-cyber-domain-models]

An optional model setting in **Feature Settings** for cyber-specific models. A model you save here replaces the [Efficient](#alertzero-glossary-efficient-models) or [Frontier](#alertzero-glossary-frontier-models) model that Attack Discovery and alert triage calls would otherwise use. If you leave it empty, those calls keep using their usual models.

### {{az-detection-watch}} [alertzero-glossary-detection-watch]

The [{{az-watch}}](#alertzero-glossary-watch) that handles detection engineering, improving your detection rules at the source instead of handling the alerts they produce one by one. Its {{az-rule-tuning}} {{az-worker}} diagnoses noisy or under-covering rules and proposes tuning changes. Its {{az-rule-coverage}} {{az-worker}} assesses detection gaps that {{az-hunt-watch}} finds and proposes new or existing rules to close them. Refer to [](watches-and-workers.md#alertzero-detection-watch).

## E-F [alertzero-glossary-e-f]

### {{az-efficient-models}} [alertzero-glossary-efficient-models]

A model setting in **Feature Settings** for {{alertzero}} calls that need quick, lightweight judgment and run often, such as checking detection coverage. Choose a small, low-cost model. Refer to [{{az-balanced-models}}](#alertzero-glossary-balanced-models) and [{{az-frontier-models}}](#alertzero-glossary-frontier-models).

### {{az-escalation-cap}} [alertzero-glossary-escalation]

A coordinated response that you create from an [{{az-investigation}}](#alertzero-glossary-investigation) to work on it with other people, privately if needed. An {{az-escalation}} can link related {{az-investigations}}, and it has an owner, assignees, and a visibility of **Public** or **Private**. Closing an {{az-escalation}} also closes its linked {{az-investigations}}. Refer to [](escalate-investigation.md) and [](track-escalations.md).

### {{az-forensics-watch}} [alertzero-glossary-forensics-watch]

The [{{az-watch}}](#alertzero-glossary-watch) that does deep research on threats and exploits, running forensics on an attack. Its {{az-endpoint-analysis}} {{az-worker}} reconstructs the attack timeline on the affected hosts and proposes response actions. It runs only on attacks handed off by the {{az-attack-discovery}} {{az-worker}}, and it needs {{elastic-defend}} data. Refer to [](watches-and-workers.md#alertzero-forensics-watch).

### {{az-frontier-models}} [alertzero-glossary-frontier-models]

A model setting in **Feature Settings** for complex, single-pass {{alertzero}} work where output quality matters most, such as generating attack discoveries or drafting a detection rule. Choose your most capable model. Refer to [{{az-efficient-models}}](#alertzero-glossary-efficient-models) and [{{az-balanced-models}}](#alertzero-glossary-balanced-models).

## H-I [alertzero-glossary-h-i]

### {{az-hunt-finding-cap}} [alertzero-glossary-hunt-finding]

A result from the [{{az-hunt-watch}}](#alertzero-glossary-hunt-watch): activity in your environment that matches a [{{az-threat-report}}](#alertzero-glossary-threat-report). Each {{az-hunt-finding}} opens an [{{az-investigation}}](#alertzero-glossary-investigation) and shows its supporting evidence, such as matching events, indicators, and techniques. In an {{az-investigation}}, a {{az-hunt-finding}} appears as a **Significant Security Event**. Refer to [](act-on-hunt-finding.md).

### {{az-hunt-watch}} [alertzero-glossary-hunt-watch]

The [{{az-watch}}](#alertzero-glossary-watch) that proactively hunts your environment for threats, without waiting for an alert. Its {{az-continuous-threat-hunt}} {{az-worker}} searches your data for activity that matches {{az-threat-reports}} and for detection coverage gaps. This {{az-worker}} runs on a fixed schedule and always uses [{{az-manual}}](#alertzero-glossary-manual) {{az-autonomy}}. Refer to [](watches-and-workers.md#alertzero-hunt-watch).

### {{az-investigation-cap}} [alertzero-glossary-investigation]

A record of an {{alertzero}} {{az-worker}}'s inquiry into a potential threat, such as a candidate attack or a [{{az-hunt-finding}}](#alertzero-glossary-hunt-finding). An {{az-investigation}} collects the {{az-worker}}'s evidence, its conclusion, and any [{{az-proposed-actions}}](#alertzero-glossary-proposed-action). You can assign an {{az-investigation}}, close it, or [escalate](#alertzero-glossary-escalation) it. Refer to [](escalate-investigation.md).

## M-P [alertzero-glossary-m-p]

### {{az-manual}} ({{az-autonomy}}) [alertzero-glossary-manual]

The default [{{az-autonomy}}](#alertzero-glossary-autonomy) level. At this level, every action the {{az-worker}} proposes waits for your approval, and some {{az-workers}} also ask for your approval before they start analyzing. For example, {{az-alert-triage}} waits for you to approve closing false-positive alerts, {{az-attack-discovery}} waits for you to approve handing an attack to the {{az-forensics-watch}}, and {{az-endpoint-analysis}} waits for you to approve each response action. Refer to [](configure-worker-settings.md).

### {{az-proposed-action-cap}} [alertzero-glossary-proposed-action]

A recommendation from a {{az-worker}} that waits for your decision, such as closing false-positive alerts, isolating a host, or changing a detection rule. You review the details, then approve or decline it. Depending on the {{az-worker}}'s [{{az-autonomy}}](#alertzero-glossary-autonomy) level, some {{az-proposed-actions}} run without waiting for you. Statuses include **Needs review**, **Applying**, **Applied**, **Declined**, **Failed**, and **Expired**. Refer to [](decide-proposed-action.md).

## R-S [alertzero-glossary-r-s]

### {{az-supervised}} ({{az-autonomy}}) [alertzero-glossary-supervised]

The highest [{{az-autonomy}}](#alertzero-glossary-autonomy) level. At this level, the {{az-worker}} approves its own {{az-proposed-actions}} instead of waiting for you, and you review the results afterward. For example, {{az-alert-triage}} closes false-positive alerts, which you can reopen, {{az-attack-discovery}} hands attacks to the {{az-forensics-watch}}, and {{az-endpoint-analysis}} runs its response actions. Refer to [](configure-worker-settings.md).

## T-W [alertzero-glossary-t-w]

### {{az-threat-intel-supply-cap}} [alertzero-glossary-threat-intel-supply]

The set of workflows that feed threat intelligence to the [{{az-hunt-watch}}](#alertzero-glossary-hunt-watch). **Ingest** collects threat feeds, **Enrich** builds out {{az-threat-reports}}, and **Attribute alerts to reports** connects alerts to those reports. {{alertzero}} turns them on when you turn on the {{az-continuous-threat-hunt}} {{az-worker}}, and off again when you turn it off. Ingest and Enrich are shared across all spaces. Refer to [](configure-worker-settings.md).

### {{az-threat-report-cap}} [alertzero-glossary-threat-report]

A report of threat activity, built from ingested threat intelligence, that the [{{az-hunt-watch}}](#alertzero-glossary-hunt-watch) searches your data for. A [{{az-hunt-finding}}](#alertzero-glossary-hunt-finding) links back to its source report.

### {{az-triage-watch}} [alertzero-glossary-triage-watch]

The [{{az-watch}}](#alertzero-glossary-watch) that works as your first line of defense, reviewing incoming alerts and routing the ones that still need a person. Its {{az-alert-triage}} {{az-worker}} classifies alerts as true or false positives, then proposes closing the false positives. Its {{az-attack-discovery}} {{az-worker}} finds candidate attacks and opens an {{az-investigation}} for each. Refer to [](watches-and-workers.md#alertzero-triage-watch).

### {{az-watch}} [alertzero-glossary-watch]

A named group of [{{az-workers}}](#alertzero-glossary-worker) with one area of expertise. {{alertzero}} includes the following {{az-watches}}: [{{az-triage-watch}}](#alertzero-glossary-triage-watch), [{{az-hunt-watch}}](#alertzero-glossary-hunt-watch), [{{az-detection-watch}}](#alertzero-glossary-detection-watch), and [{{az-forensics-watch}}](#alertzero-glossary-forensics-watch). Each {{az-watch}} has its own page where you turn its {{az-workers}} on or off and change their settings. Refer to [](watches-and-workers.md).

### {{az-worker}} [alertzero-glossary-worker]

An AI-powered unit of work that belongs to a [{{az-watch}}](#alertzero-glossary-watch). A {{az-worker}} runs in the background, either on a schedule or in response to events such as new alerts. It analyzes your data and brings you [{{az-proposed-actions}}](#alertzero-glossary-proposed-action). Each {{az-worker}} has its own settings, including whether it's turned on, its trigger, and its [{{az-autonomy}}](#alertzero-glossary-autonomy) level. Refer to [](watches-and-workers.md) and [](configure-worker-settings.md).

## Related [alertzero-glossary-related]

- [](index.md): What {{alertzero}} is and how its parts fit together.
- [](watches-and-workers.md): Reference for every {{az-watch}} and {{az-worker}}.
- [](use-alertzero.md): Read the {{alertzero}} home page and decide on {{az-proposed-actions}}.
- [](manage-alertzero.md): What you can and can't configure in {{alertzero}}.

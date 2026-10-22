---
navigation_title: Glossary
description: "Reference of terms used across AlertZero documentation, with links to the pages that explain them."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# AlertZero glossary [alertzero-glossary]

Every term used in the AlertZero documentation. Terms match the labels you see in the product. Each entry links to the page that explains it in more detail, where one exists.

## A-B [alertzero-glossary-a-b]

### AlertZero [alertzero-glossary-alertzero]

An {{elastic-sec}} feature that runs agentic security work for your SOC. AI-powered [Workers](#alertzero-glossary-worker), grouped into [Watches](#alertzero-glossary-watch), triage alerts, hunt for threats, tune noisy detection rules, and investigate on their own, then bring you the [proposed actions](#alertzero-glossary-proposed-action) that need a person to decide. Refer to [](index.md).

### Assisted [alertzero-glossary-assisted]

An [autonomy](#alertzero-glossary-autonomy) level at which a Worker skips the approval it asks for at [Manual](#alertzero-glossary-manual) before it starts analyzing or drafting. Every proposed rule change still waits for you. Refer to [](configure-worker-settings.md).

### Attack Discovery [alertzero-glossary-attack-discovery]

An {{elastic-sec}} feature that uses large language models (LLMs) to group related alerts into attack narratives. In AlertZero, Attack Discovery is also the name of a [Worker](#alertzero-glossary-worker) in the [Triage Watch](#alertzero-glossary-triage-watch). It runs on a schedule, opens an [investigation](#alertzero-glossary-investigation) for each candidate attack, and proposes handing attacks it confirms, or can't rule out, to the [Forensics Watch](#alertzero-glossary-forensics-watch). Refer to [Attack Discovery](/solutions/security/ai/attack-discovery/index.md) and [](watches-and-workers.md#alertzero-triage-watch).

### Autonomy [alertzero-glossary-autonomy]

A Worker setting that controls how far the Worker goes on its own before it waits for a person. Each Worker offers some of these levels: [Manual](#alertzero-glossary-manual), [Assisted](#alertzero-glossary-assisted), and [Supervised](#alertzero-glossary-supervised). Every Worker starts at Manual. Refer to [](configure-worker-settings.md).

### Balanced models [alertzero-glossary-balanced-models]

A model setting in **Feature Settings** for AlertZero calls where accuracy matters, but that run often or use tools over many steps, such as triaging alerts or diagnosing a noisy rule. Choose a strong mid-size model. Refer to [Efficient models](#alertzero-glossary-efficient-models) and [Frontier models](#alertzero-glossary-frontier-models).

## C-D [alertzero-glossary-c-d]

### Closed actions [alertzero-glossary-closed-actions]

The section of the AlertZero home page that lists proposed actions that are no longer waiting for a decision, including ones that expired or that a Worker resolved without you. Refer to [](review-closed-proposed-actions.md).

### Configure [alertzero-glossary-configure]

A section of the AlertZero home page that groups proposed actions about your detection rules, such as reviewing a detection gap, creating, editing, or enabling a rule, or adding a rule exception. Refer to [](decide-detection-change.md).

### Cyber domain models [alertzero-glossary-cyber-domain-models]

An optional model setting in **Feature Settings** for cyber-specific models. A model you save here replaces the [Efficient](#alertzero-glossary-efficient-models) or [Frontier](#alertzero-glossary-frontier-models) model that Attack Discovery and alert triage calls would otherwise use. If you leave it empty, those calls keep using their usual models.

### Detection Watch [alertzero-glossary-detection-watch]

The [Watch](#alertzero-glossary-watch) that improves your detection rules. Its Rule Tuning Worker diagnoses noisy or under-covering rules and proposes tuning changes. Its Rule Coverage Worker assesses detection gaps that Hunt Watch finds and proposes new or existing rules to close them. Refer to [](watches-and-workers.md#alertzero-detection-watch).

## E-F [alertzero-glossary-e-f]

### Efficient models [alertzero-glossary-efficient-models]

A model setting in **Feature Settings** for AlertZero calls that need quick, lightweight judgment and run often, such as checking detection coverage. Choose a small, low-cost model. Refer to [Balanced models](#alertzero-glossary-balanced-models) and [Frontier models](#alertzero-glossary-frontier-models).

### Escalation [alertzero-glossary-escalation]

A coordinated response that you create from an [investigation](#alertzero-glossary-investigation) when it needs a human decision. An escalation links one or more investigations, and has an owner, assignees, and a visibility of **Public** or **Private**. Closing an escalation also closes its linked investigations. Refer to [](escalate-investigation.md) and [](track-escalations.md).

### Forensics Watch [alertzero-glossary-forensics-watch]

The [Watch](#alertzero-glossary-watch) that runs deeper forensics on an attack. Its Endpoint Analysis Worker reconstructs the attack timeline on the affected hosts and proposes response actions. It runs only on attacks handed off by the Attack Discovery Worker, and it needs {{elastic-defend}} data. Refer to [](watches-and-workers.md#alertzero-forensics-watch).

### Frontier models [alertzero-glossary-frontier-models]

A model setting in **Feature Settings** for complex, single-pass AlertZero work where output quality matters most, such as generating attack discoveries or drafting a detection rule. Choose your most capable model. Refer to [Efficient models](#alertzero-glossary-efficient-models) and [Balanced models](#alertzero-glossary-balanced-models).

## H-I [alertzero-glossary-h-i]

### Hunt finding [alertzero-glossary-hunt-finding]

A result from the [Hunt Watch](#alertzero-glossary-hunt-watch): activity in your environment that matches a [threat report](#alertzero-glossary-threat-report). Each hunt finding opens an [investigation](#alertzero-glossary-investigation) and shows its supporting evidence, such as matching events, indicators, and techniques. In an investigation, a hunt finding appears as a **Significant Security Event**. Refer to [](act-on-hunt-finding.md).

### Hunt Watch [alertzero-glossary-hunt-watch]

The [Watch](#alertzero-glossary-watch) that hunts for threats before anyone reports them. Its Continuous Threat Hunt Worker searches your data for activity that matches threat reports and for detection coverage gaps. This Worker runs on a fixed schedule and always uses [Manual](#alertzero-glossary-manual) autonomy. Refer to [](watches-and-workers.md#alertzero-hunt-watch).

### Impact [alertzero-glossary-impact]

The row on the AlertZero home page that lists the hosts, users, and other entities involved in your [proposed actions](#alertzero-glossary-proposed-action). Each entry shows an entity and the number of proposed actions that involve it, including closed ones. Select an entry to filter the home page to that entity. Impact is also the severity of a single proposed action: critical, high, medium, or low. Refer to [](use-alertzero.md).

### Investigate [alertzero-glossary-investigate]

A section of the AlertZero home page that groups proposed actions that help you look further into a threat, such as closing alerts as false positives or running a deep forensics investigation. Refer to [](decide-proposed-action.md).

### Investigation [alertzero-glossary-investigation]

A record of an AlertZero Worker's inquiry into a potential threat, such as a candidate attack or a [hunt finding](#alertzero-glossary-hunt-finding). An investigation collects the Worker's evidence, its conclusion, and any [proposed actions](#alertzero-glossary-proposed-action). You can assign an investigation, close it, or [escalate](#alertzero-glossary-escalation) it. Refer to [](escalate-investigation.md).

## M-P [alertzero-glossary-m-p]

### Manual [alertzero-glossary-manual]

The default [autonomy](#alertzero-glossary-autonomy) level. At this level, the Worker still runs and analyzes on its own, but the actions it proposes wait for your approval. For example, Alert Triage waits for you to approve closing false-positive alerts, Attack Discovery waits for you to approve handing an attack to the Forensics Watch, and Endpoint Analysis waits for you to approve each response action. Rule Tuning and Rule Coverage also ask for your approval before they start analyzing a rule or a detection gap. Refer to [](configure-worker-settings.md).

### Proposed action [alertzero-glossary-proposed-action]

A recommendation from a Worker that waits for your decision, such as closing false-positive alerts, isolating a host, or changing a detection rule. You review the details, then approve or decline it. Depending on the Worker's [autonomy](#alertzero-glossary-autonomy) level, some proposed actions run without waiting for you. Statuses include **Needs review**, **Applying**, **Applied**, **Declined**, **Failed**, and **Expired**. Refer to [](decide-proposed-action.md).

## R-S [alertzero-glossary-r-s]

### Respond [alertzero-glossary-respond]

A section of the AlertZero home page that groups proposed actions that contain a threat, such as isolating a host, killing a process, or suspending a process. Refer to [](respond-to-attack.md).

### Supervised [alertzero-glossary-supervised]

The highest [autonomy](#alertzero-glossary-autonomy) level. At this level, the Worker approves its own proposed actions instead of waiting for you, and you review the results afterward. For example, Alert Triage closes false-positive alerts, which you can reopen, Attack Discovery hands attacks to the Forensics Watch, and Endpoint Analysis runs its response actions. Refer to [](configure-worker-settings.md).

## T-W [alertzero-glossary-t-w]

### Threat intel supply [alertzero-glossary-threat-intel-supply]

The set of workflows that feed threat intelligence to the [Hunt Watch](#alertzero-glossary-hunt-watch). **Ingest** collects threat feeds, **Enrich** builds out threat reports, and **Attribute alerts to reports** connects alerts to those reports. AlertZero turns them on when you turn on the Continuous Threat Hunt Worker, and off again when you turn it off. Ingest and Enrich are shared across all spaces. Refer to [](configure-worker-settings.md).

### Threat report [alertzero-glossary-threat-report]

A report of threat activity, built from ingested threat intelligence, that the [Hunt Watch](#alertzero-glossary-hunt-watch) searches your data for. A [hunt finding](#alertzero-glossary-hunt-finding) links back to its source report.

### Triage Watch [alertzero-glossary-triage-watch]

The [Watch](#alertzero-glossary-watch) that reduces alert volume and routes what still needs a person. Its Alert Triage Worker classifies each batch of alerts. Its Attack Discovery Worker finds candidate attacks and opens an investigation for each. Refer to [](watches-and-workers.md#alertzero-triage-watch).

### Watch [alertzero-glossary-watch]

A named group of related [Workers](#alertzero-glossary-worker) that handle one kind of security work. The following Watches are available: [Triage Watch](#alertzero-glossary-triage-watch), [Hunt Watch](#alertzero-glossary-hunt-watch), [Detection Watch](#alertzero-glossary-detection-watch), and [Forensics Watch](#alertzero-glossary-forensics-watch). Each Watch has its own page where you turn its Workers on or off and change their settings. Refer to [](watches-and-workers.md).

### Worker [alertzero-glossary-worker]

An AI-powered unit of work that belongs to a [Watch](#alertzero-glossary-watch). A Worker runs in the background, either on a schedule or in response to events such as new alerts. It analyzes your data and brings you [proposed actions](#alertzero-glossary-proposed-action). Each Worker has its own settings, including whether it's turned on, its trigger, and its [autonomy](#alertzero-glossary-autonomy) level. Refer to [](watches-and-workers.md) and [](configure-worker-settings.md).

## Related [alertzero-glossary-related]

- [](index.md): What AlertZero is and how its parts fit together.
- [](watches-and-workers.md): Reference for every Watch and Worker.
- [](use-alertzero.md): Read the AlertZero home page and decide on proposed actions.
- [](manage-alertzero.md): What you can and can't configure in AlertZero.

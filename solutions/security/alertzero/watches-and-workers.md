---
description: "Reference for every AlertZero Watch and Worker."
applies_to:
  stack: preview 9.6
  serverless:
    security: preview
products:
  - id: security
  - id: cloud-serverless
---

# Watches and Workers

A {{az-watch}} covers one area of security work and includes one or more {{az-workers}}. {{az-workers}} in different {{az-watches}} often depend on each other. Refer to [](#alertzero-workers-together).

A {{az-worker}} also needs certain features and integrations to be set up. Without them, a {{az-worker}} can't work, or works only in part, so set them up before you turn the {{az-worker}} on. To change a {{az-worker}}'s settings, refer to [](configure-worker-settings.md).

## How {{az-workers}} work together [alertzero-workers-together]

Some {{az-workers}} use what other {{az-workers}} produce, so turning one off can leave another with nothing to work on. Use the following table to decide which {{az-workers}} to keep on.

| {{az-worker}} | {{az-watch}} | What it does | Works with |
| --- | --- | --- | --- |
| [{{az-alert-triage}}](#alertzero-alert-triage) | {{az-triage-watch}} | Classifies alerts and proposes closing false positives. | {{az-rule-tuning}}, which learns from the alerts that {{az-alert-triage}} classifies as false positives. |
| [{{az-attack-discovery}}](#alertzero-attack-discovery) | {{az-triage-watch}} | Groups related alerts into potential attacks and proposes handing them off for a deeper investigation. | {{az-endpoint-analysis}}, which investigates the attacks that {{az-attack-discovery}} hands off. |
| [{{az-continuous-threat-hunt}}](#alertzero-continuous-threat-hunt) | {{az-hunt-watch}} | Hunts your data for activity that matches {{az-threat-reports}} and records the detection gaps it finds. | {{az-rule-coverage}}, which reviews the gaps that {{az-continuous-threat-hunt}} records. |
| [{{az-rule-tuning}}](#alertzero-rule-tuning) | {{az-detection-watch}} | Proposes tuning changes for rules that produce many false positives. | {{az-alert-triage}}. Without it, {{az-rule-tuning}} still works, but has fewer alerts to learn from. |
| [{{az-rule-coverage}}](#alertzero-rule-coverage) | {{az-detection-watch}} | Proposes a fix for each detection gap, such as turning on an existing rule, installing a prebuilt rule, or drafting a new one. | {{az-continuous-threat-hunt}}. Without it, {{az-rule-coverage}} has no gaps to review. |
| [{{az-endpoint-analysis}}](#alertzero-endpoint-analysis) | {{az-forensics-watch}} | Reconstructs the attack timeline on an affected host and proposes response actions. | {{az-attack-discovery}}. Without it, {{az-endpoint-analysis}} has no attacks to investigate. |

## {{az-triage-watch}} [alertzero-triage-watch]

The {{az-triage-watch}} is your first line of defense. It reviews incoming alerts and finds potential attacks.

### {{az-alert-triage}} [alertzero-alert-triage]

The {{az-alert-triage}} {{az-worker}} reviews alerts that are waiting to be triaged. It classifies each alert as a true positive, a false positive, or, if the false positive confidence score is below the threshold set in the [**Minimum confidence score** setting](configure-worker-settings.md#configure-worker-settings-alert-triage), inconclusive. It adds its classification to the alert as a tag and a note, and proposes closing the false positives.

{{az-alert-triage}} relies on the [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) to analyze alerts, so make sure that workflow is turned on.

Each proposed closure appears as a {{az-proposed-action}} on the **{{az-proposed-actions-cap}}** page. To find it, refer to [](work-in-alertzero.md), and to decide what to do with it, refer to [](close-false-positive-alerts.md).

### {{az-attack-discovery}} [alertzero-attack-discovery]

The {{az-attack-discovery}} {{az-worker}} groups related alerts into potential attacks and opens an {{az-investigation}} for each one. For each attack that it confirms as a true positive or can't rule out, it proposes handing the attack to the {{az-forensics-watch}} for a deeper investigation. It doesn't hand off false positives.

To generate discoveries, {{az-attack-discovery}} needs the [**Attack Discovery Workflows**](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting turned on in the current space. It also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that the attacks it hands off can reach the {{az-endpoint-analysis}} {{az-worker}} in the {{az-forensics-watch}}.

The handoff appears in the attack's {{az-investigation}} as a {{az-proposed-action}}. To decide whether to hand off the attack, refer to [](respond-to-attack.md).

## {{az-hunt-watch}} [alertzero-hunt-watch]

The {{az-hunt-watch}} proactively looks for threats in your data without waiting for an alert.

### {{az-continuous-threat-hunt}} [alertzero-continuous-threat-hunt]

The {{az-continuous-threat-hunt}} {{az-worker}} searches your data for activity that matches {{az-threat-reports}}, opens an {{az-investigation}} for each {{az-threat-report}} it hunts, and proposes response actions for the threats it finds, such as isolating a host. It also records the detection gaps that it finds, so the {{az-rule-coverage}} {{az-worker}} in the {{az-detection-watch}} can review them.

{{az-continuous-threat-hunt}} works from {{az-threat-reports}}, which {{alertzero}} [builds for you from public threat feeds](threat-reports.md). It can't start hunting until the workflows that build reports have run. Building reports needs outbound network access to the feeds, models configured in the default space, and your cluster's default embedding endpoint. {{az-continuous-threat-hunt}} also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that it can record detection gaps for {{az-rule-coverage}}.

Each {{az-hunt-finding}} appears in its {{az-investigation}}, with the finding's severity, confidence, and the evidence behind it. To decide what to do with a finding, refer to [](act-on-hunt-finding.md).

## {{az-detection-watch}} [alertzero-detection-watch]

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one. Its {{az-workers}} find noisy rules and gaps in detection coverage, and propose changes to fix them.

### {{az-rule-tuning}} [alertzero-rule-tuning]

The {{az-rule-tuning}} {{az-worker}} finds rules that produce many false positives, diagnoses why, and proposes a tuning change.

{{az-rule-tuning}} needs alerts that are marked as false positives. It counts the alerts that {{az-alert-triage}} in the {{az-triage-watch}} classified as false positives, and the alerts that human users closed as false positives. {{az-rule-tuning}} can still work without {{az-alert-triage}}, but it then has fewer alerts to learn from.

Each rule that {{az-rule-tuning}} reviews has its own {{az-investigation}}, with the tuning change as a {{az-proposed-action}}. To decide on a tuning change, refer to [](decide-detection-change.md).

### {{az-rule-coverage}} [alertzero-rule-coverage]

The {{az-rule-coverage}} {{az-worker}} reviews the detection gaps that {{az-continuous-threat-hunt}} in the {{az-hunt-watch}} records. For each gap, it checks whether a rule already covers it, and proposes the simplest fix, such as enabling a disabled rule or installing a prebuilt rule. If no rule fits, it drafts a new one.

{{az-rule-coverage}} depends on the gaps that {{az-continuous-threat-hunt}} records, so if that {{az-worker}} is off, {{az-rule-coverage}} has nothing to review. It also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that it can process the recorded gaps.

Each gap has its own {{az-investigation}}, with the fix as a {{az-proposed-action}}. To decide on a fix, refer to [](decide-detection-change.md).

## {{az-forensics-watch}} [alertzero-forensics-watch]

The {{az-forensics-watch}} does deep research on an attack. It works on attacks that {{az-attack-discovery}} in the {{az-triage-watch}} hands off.

### {{az-endpoint-analysis}} [alertzero-endpoint-analysis]

The {{az-endpoint-analysis}} {{az-worker}} reconstructs the attack timeline on the affected host, extracts indicators of compromise, and proposes response actions, such as isolating a host or terminating a process.

{{az-endpoint-analysis}} works only on the attacks that {{az-attack-discovery}} hands off, and it doesn't look for attacks on its own. It also needs {{elastic-defend}} to be set up so that it can investigate hosts, and it analyzes only hosts that have {{elastic-defend}} data from around the time of the attack. 

To read and update {{az-investigations}}, {{az-endpoint-analysis}} also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md).

{{az-endpoint-analysis}} adds its findings to the {{az-investigation}} that {{az-attack-discovery}} opened for the attack, and the response actions appear there as {{az-proposed-actions}}. To decide on them, refer to [](respond-to-attack.md).

When no response actions are waiting for your decision, {{az-endpoint-analysis}} proposes closing the {{az-investigation}}. If you approve, {{alertzero}} closes the {{az-investigation}}, the attack, and the attack's alerts.

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

A {{az-watch}} covers one area of security work and includes one or more {{az-workers}}. {{az-workers}} in different {{az-watches}} often depend on each other. For example, the {{az-forensics-watch}} analyzes the attacks that the {{az-triage-watch}} finds, so turn on the {{az-workers}} in both {{az-watches}} if you want {{alertzero}} to take an attack from discovery to a response.

A {{az-worker}} also needs certain features and integrations to be set up. Without them, a {{az-worker}} can't work, or works only in part, so set them up before you turn the {{az-worker}} on. To change a {{az-worker}}'s settings, refer to [](configure-worker-settings.md).

## {{az-triage-watch}} [alertzero-triage-watch]

The {{az-triage-watch}} is your first line of defense. It reviews incoming alerts and finds candidate attacks.

### {{az-alert-triage}} [alertzero-alert-triage]

The {{az-alert-triage}} {{az-worker}} reviews alerts that are waiting to be triaged. It classifies each alert as a true positive or a false positive, adds its classification to the alert as a tag and a note, and proposes closing the false positives.

{{az-alert-triage}} relies on the [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) to analyze alerts, so make sure that workflow is turned on.

Each proposed closure appears as a {{az-proposed-action}} on the **{{az-proposed-actions-cap}}** page. To find it, refer to [](use-alertzero.md), and to decide what to do with it, refer to [](decide-proposed-action.md).

### {{az-attack-discovery}} [alertzero-attack-discovery]

The {{az-attack-discovery}} {{az-worker}} groups related alerts into candidate attacks and opens an {{az-investigation}} for each one. For each attack that it confirms or can't rule out, it proposes handing the attack to the {{az-forensics-watch}} for a deeper investigation.

To generate discoveries, {{az-attack-discovery}} needs the [**Attack Discovery Workflows**](kibana://reference/advanced-settings.md#kibana-siem-settings) advanced setting turned on in the current space. It also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that the attacks it hands off can reach the {{az-endpoint-analysis}} {{az-worker}} in the {{az-forensics-watch}}.

The handoff appears in the attack's {{az-investigation}} as a {{az-proposed-action}}. To decide whether to hand off the attack, refer to [](respond-to-attack.md).

## {{az-hunt-watch}} [alertzero-hunt-watch]

The {{az-hunt-watch}} proactively looks for threats in your data without waiting for an alert.

### {{az-continuous-threat-hunt}} [alertzero-continuous-threat-hunt]

The {{az-continuous-threat-hunt}} {{az-worker}} searches your data for activity that matches {{az-threat-reports}}, opens an {{az-investigation}} for each {{az-hunt-finding}}, and proposes response actions, such as isolating a host. It also records the detection gaps that it finds, so the {{az-rule-coverage}} {{az-worker}} in the {{az-detection-watch}} can review them.

{{az-continuous-threat-hunt}} works from {{az-threat-reports}}, which {{alertzero}} builds from public threat intelligence feeds. It searches only reports that have been fully processed, so it can't start hunting until the workflows that collect and process reports have run. Refer to [](#alertzero-threat-reports). It also needs [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that it can record detection gaps for {{az-rule-coverage}}.

Each {{az-hunt-finding}} appears in its {{az-investigation}}, with the finding's severity, confidence, and the evidence behind it. To decide what to do with a finding, refer to [](act-on-hunt-finding.md).

#### How {{alertzero}} builds {{az-threat-reports}} [alertzero-threat-reports]

{{alertzero}} builds {{az-threat-reports}} for you from public threat feeds, so you don't need to set up the feeds yourself. When you turn on {{az-continuous-threat-hunt}}, {{alertzero}} turns on two threat intelligence workflows that run every 4 hours, in this order.

1. **Ingest threat feeds** collects new articles from the [supported threat feeds](#alertzero-threat-feeds) and saves each one as a {{az-threat-report}}. It skips articles more than 30 days old and articles it already collected in the last 90 days.
2. **Enrich threat report** checks that each report contains threat intelligence, then extracts details such as indicators of compromise (IOCs), attacker behaviors, and severity. {{az-continuous-threat-hunt}} ignores reports that fail the check.

:::{dropdown} What Enrich threat report adds to each report
* IOCs, including file hashes, IP addresses and ranges, domains, URLs, email addresses, and cryptocurrency wallet addresses.
* A classification of the threat, including its categories, attacker behaviors, affected regions, and severity.
* A description of the adversary, including their capabilities, infrastructure, and victims, if the report has enough detail.
* Links to other reports that share its IOCs.
:::

All spaces in your deployment share both workflows, so every space gets the same reports. A third workflow, **Attribute alerts to reports**, then counts the alerts in each space that match each report.

:::{tip}
After you first turn on {{az-continuous-threat-hunt}}, **Enrich threat report** might need several runs to process all the collected reports. It processes up to 50 reports per run, oldest first. Until then, {{az-continuous-threat-hunt}} hunts with only the reports processed so far.
:::

#### Supported threat feeds [alertzero-threat-feeds]

**Ingest threat feeds** checks these public feeds for new articles. You can't add your own feeds or change this list.

| Feed | Publisher |
| --- | --- |
| Elastic Security Labs | Elastic |
| CISA Alerts and Advisories | U.S. Cybersecurity and Infrastructure Security Agency (CISA) |
| UK National Cyber Security Centre | UK National Cyber Security Centre (NCSC) |
| CERT-FR Security Alerts | French national CERT (CERT-FR) |
| CERT-FR Threats and Incidents | CERT-FR |
| CERT-EU Security Advisories | CERT for the EU institutions (CERT-EU) |
| CERT-EU Threat Intelligence | CERT-EU |

#### What the threat intelligence workflows need [alertzero-threat-reports-requirements]

To build reports for {{az-continuous-threat-hunt}}, the threat intelligence workflows need network access to the threat feeds and a model to process reports. **Enrich threat report** runs in the default space, so it uses the default space's model settings for every report, even if you hunt in another space. It calls the model for every new report.

| Workflow | Needs | What happens without it |
| --- | --- | --- |
| Ingest threat feeds | Outbound HTTPS access from {{kib}} to `www.elastic.co`, `www.cisa.gov`, `www.ncsc.gov.uk`, `cert.cyber.gouv.fr`, and `cert.europa.eu`. | The workflow runs, but it collects no reports from the feeds it can't reach. |
| Enrich threat report | Reports from **Ingest threat feeds**. | It has nothing to process, so {{az-continuous-threat-hunt}} has no reports to search for. |
| Enrich threat report | A model selected for **Efficient models** and **Frontier models** in **Feature Settings**, in the default space. Refer to [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). | Reports stay unprocessed, and {{az-continuous-threat-hunt}} can't search for them. The workflow retries them on its next run. |

## {{az-detection-watch}} [alertzero-detection-watch]

The {{az-detection-watch}} improves your detection rules at the source, instead of handling the alerts they produce one by one. Its {{az-workers}} build on what other {{az-watches}} produce.

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

{{az-endpoint-analysis}} works only on the attacks that {{az-attack-discovery}} hands off, and it doesn't look for attacks on its own. It also needs {{elastic-defend}} to be set up so that it can investigate hosts, and [{{context-engine}}](/explore-analyze/ai-features/context-engine.md) so that it can read and update {{az-investigations}}.

{{az-endpoint-analysis}} adds its findings to the {{az-investigation}} that {{az-attack-discovery}} opened for the attack, and the response actions appear there as {{az-proposed-actions}}. To decide on them, refer to [](respond-to-attack.md).

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

#### How {{az-threat-reports}} are built [alertzero-threat-reports]

Two workflows build the {{az-threat-reports}} that {{az-continuous-threat-hunt}} searches for. They run in this order:

1. **Ingest threat feeds** collects new articles from the [supported threat feeds](#alertzero-threat-feeds) and saves each one as a {{az-threat-report}}. It runs every 4 hours. It skips articles published more than 30 days ago, and articles it already collected in the last 90 days.
2. **Enrich threat report** processes the reports that **Ingest threat feeds** saved. For each report, it:

   * Checks that the report contains threat intelligence. {{az-continuous-threat-hunt}} never searches for reports that fail this check.
   * Extracts indicators of compromise (IOCs): file hashes, IP addresses and ranges, domains, URLs, email addresses, and cryptocurrency wallet addresses.
   * Classifies the threat, including its categories, the attacker behaviors it describes, the regions it affects, and its severity.
   * Describes the adversary, their capabilities, their infrastructure, and their victims, when the report has enough detail.
   * Links the report to other reports that share its IOCs.

   It runs every 4 hours and processes up to 50 reports per run, oldest first. After you first turn it on, it can take several runs to work through the reports that **Ingest threat feeds** collected.

{{alertzero}} turns on both workflows when you turn on {{az-continuous-threat-hunt}}, so you don't need to set up the feeds yourself. Both workflows run once for your whole deployment, and the reports they build are available in every space. A third workflow, **Attribute alerts to reports**, then counts the alerts in each space that match each report.

#### Supported threat feeds [alertzero-threat-feeds]

**Ingest threat feeds** collects from the following public feeds. The list is fixed, so you can't add your own feeds or change these.

| Feed | Publisher | Fetched from |
| --- | --- | --- |
| Elastic Security Labs | Elastic | `www.elastic.co` |
| CISA Alerts and Advisories | U.S. Cybersecurity and Infrastructure Security Agency (CISA) | `www.cisa.gov` |
| UK National Cyber Security Centre | UK National Cyber Security Centre (NCSC) | `www.ncsc.gov.uk` |
| CERT-FR Security Alerts | French national CERT (CERT-FR) | `cert.cyber.gouv.fr` |
| CERT-FR Threats and Incidents | CERT-FR | `cert.cyber.gouv.fr` |
| CERT-EU Security Advisories | CERT for the EU institutions (CERT-EU) | `cert.europa.eu` |
| CERT-EU Threat Intelligence | CERT-EU | `cert.europa.eu` |

#### What the threat intelligence workflows need [alertzero-threat-reports-requirements]

| Workflow | Needs | What happens without it |
| --- | --- | --- |
| **Ingest threat feeds** | Outbound HTTPS access from {{kib}} to the hosts in [Supported threat feeds](#alertzero-threat-feeds). | The workflow runs, but it collects no reports from the feeds it can't reach. |
| **Enrich threat report** | Reports from **Ingest threat feeds**. | It has nothing to process, so {{az-continuous-threat-hunt}} has no reports to search for. |
| **Enrich threat report** | A model selected for **Efficient models** and **Frontier models** in **Feature Settings**, in the default space. Refer to [Manage access to AI features](/explore-analyze/ai-features/manage-access-to-ai-assistant.md). | Reports stay unprocessed, and {{az-continuous-threat-hunt}} can't search for them. The workflow retries them on its next run. |

**Enrich threat report** runs in the default space, so it uses the default space's model settings for every report, even if you hunt in another space. It makes model calls for every new report.

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

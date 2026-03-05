---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/detection-engine-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-detection-engine-overview.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Detections and alerts [security-detection-engine-overview]

{{elastic-sec}}'s detection engine evaluates your data against detection rules and generates alerts when rule criteria are met. Rules can correlate events across all connected data sources to surface threats that no single data stream would reveal on its own. {{elastic-sec}} provides several [rule types](/solutions/security/detect-and-alert/choose-the-right-rule-type.md), from field-value matches to event correlation, {{ml}} anomaly detection, and more.

The detection engine also surfaces alerts from [{{elastic-defend}}'s endpoint protection](/solutions/security/manage-elastic-defend/endpoint-protection-rules.md) (malware, ransomware, memory threats, and malicious behavior) and [external alerts](https://www.elastic.co/docs/reference/security/prebuilt-rules/rules/promotions/external_alerts) from third-party tools like Suricata, giving you a unified view of threats across your security stack.

## Where to start

| Your goal | Start here |
|---|---|
| Set up detection for the first time | [Setup](/solutions/security/detect-and-alert/before-you-begin.md#one-time-setup) → [Install prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) |
| Take over an existing deployment | [MITRE ATT&CK coverage](/solutions/security/detect-and-alert/mitre-attack-coverage.md) → [Monitor rule executions](/solutions/security/detect-and-alert/monitor-rule-executions.md) |
| Build coverage for a specific threat | [Choose the right rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) → [Rule builder](/solutions/security/detect-and-alert/using-the-rule-builder.md) |
| Reduce noise from existing rules | [Tune detection rules](/solutions/security/detect-and-alert/tune-detection-rules.md) → [Exceptions](/solutions/security/detect-and-alert/rule-exceptions.md), [Suppression](/solutions/security/detect-and-alert/alert-suppression.md), or [Snooze](/solutions/security/detect-and-alert/manage-detection-rules.md#snooze-rule-actions) |

## Detection program lifecycle

The following stages represent the suggested path to a functioning detection program. Most deployments move through these stages roughly in order, though the boundaries are not strict: tuning and noise reduction are ongoing rather than a final stage.

1. **Confirm requirements.** Verify infrastructure, privileges, and data availability.
2. **Assess coverage gaps.** Use MITRE ATT&CK coverage to identify priority areas.
3. **Enable prebuilt rules.** Activate Elastic's maintained rule library for priority tactics.
4. **Build custom rules.** Fill remaining gaps with rules tailored to your environment.
5. **Validate before enabling.** Test rule logic against historical data before going live.
6. **Monitor rule health.** Confirm rules are executing correctly and generating alerts.
7. **Reduce noise.** Tune, add exceptions, suppress, or snooze as needed.

A minimal viable detection program (prebuilt rules enabled for your highest-priority tactics, running correctly, with noise managed to an actionable level) is a meaningful outcome at any stage of this workflow. You do not need to complete every stage before your detection program delivers value.

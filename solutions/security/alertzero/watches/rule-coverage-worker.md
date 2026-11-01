---
description: "Find what the AlertZero Rule Coverage Worker does in Elastic Security, the settings that control how many detection gaps it works on, and its limits."
applies_to:
  serverless:
    security: preview
  stack: preview 9.6
products:
  - id: security
  - id: cloud-serverless
---

# {{az-rule-coverage}} {{az-worker}}

The {{az-rule-coverage}} {{az-worker}} is part of the [{{az-detection-watch}}](detection-watch.md). It proposes rules to close the detection gaps that threat hunts find. This page explains when to use the {{az-rule-coverage}} {{az-worker}}, what data it needs, how it works on each gap, where to decide its {{az-proposed-actions}}, and which settings and limits apply.

## When to use the {{az-rule-coverage}} {{az-worker}} [alertzero-rule-coverage-when-to-use]

The {{az-rule-coverage}} {{az-worker}} is the right fit when:

* You use the [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md) and want a rule for each detection gap it finds.
* You want to use existing rules, including Elastic prebuilt rules, before you write new ones.

The {{az-rule-coverage}} {{az-worker}} isn't the best fit when:

* The {{az-hunt-watch}} is off. Without the gaps it records, the {{az-rule-coverage}} {{az-worker}} has nothing to work on.
* You need new rules of a type other than {{esql}}. The new rules it drafts are always {{esql}} rules.

## Data requirements [alertzero-rule-coverage-data]

The {{az-rule-coverage}} {{az-worker}} needs detection gaps that the [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md) recorded within the lookback period.

## How it works [alertzero-rule-coverage-how-it-works]

On each run, the {{az-rule-coverage}} {{az-worker}}:

1. Opens one {{az-investigation}} for each detection gap.
2. Checks whether a rule already covers the gap.
3. Proposes turning on an existing rule, installing a prebuilt rule, or creating a new {{esql}} rule. A new rule comes with a [rule preview](/solutions/security/detect-and-alert/validate-and-test-rules.md#validate-historical-data) that shows how many alerts the rule would have generated. If a rule already covers the gap, it asks you to confirm that instead.

The {{az-rule-coverage}} {{az-worker}} works only on the detection gaps that the [{{az-continuous-threat-hunt}} {{az-worker}}](continuous-threat-hunt-worker.md) in the [{{az-hunt-watch}}](hunt-watch.md) records after each successful hunt.

You review the {{az-rule-coverage}} {{az-worker}}'s proposed rules in the **Configure** section of the **{{az-proposed-actions-cap}}** page. To learn how to approve a rule before it takes effect, refer to [](../decide-detection-change.md).

### Example [alertzero-rule-coverage-example]

A threat hunt finds activity that matches a credential dumping technique, but no enabled rule detects it. The {{az-rule-coverage}} {{az-worker}} opens an {{az-investigation}} for the gap, finds a prebuilt rule that covers it but isn't on, and proposes turning the rule on. If no rule covers a gap, the {{az-rule-coverage}} {{az-worker}} drafts a new {{esql}} rule instead, with a rule preview of how many alerts the rule would have generated.

% After elastic/docs-content#9114 merges, consider linking to ../set-up-alertzero.md#alertzero-requirements-specific-workers from the intro.

## Settings [alertzero-rule-coverage-settings]

**Trigger**
:   How often the {{az-rule-coverage}} {{az-worker}} runs.

    Default: Every hour

**{{az-autonomy-cap}}**
:   How much the {{az-rule-coverage}} {{az-worker}} does without you. You can set it to **{{az-manual}}** or **{{az-assisted}}**, and at either level, you approve each rule before it takes effect. Refer to [what it does at each level](../configure-worker-settings.md#alertzero-worker-autonomy).

    Default: {{az-manual}}

**Models**
:   Opens **Feature settings**, where you select the models that {{alertzero}} uses in the space. The {{az-rule-coverage}} {{az-worker}} has no model setting of its own, so it uses the models you select there.

% Link the model recommendations page once it exists: For help choosing models, refer to [](../model-recommendations.md).

**Lookback (days)**
:   How far back it looks for gaps.

    Default: 14 days, and you can set it from 8 to 90 days.

**Max gaps per run**
:   The most gaps the {{az-rule-coverage}} {{az-worker}} works on each time it runs.

    Default: 5, and you can set it from 1 to 50.

## Limits [alertzero-rule-coverage-limits]

* The {{az-rule-coverage}} {{az-worker}} reviews up to 100 detection gaps at a time in each space. When it reaches that limit, it starts on new gaps only as earlier reviews finish.

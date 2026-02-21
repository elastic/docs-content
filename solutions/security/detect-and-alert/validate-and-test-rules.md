---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Verify rule logic against historical data, assess alert volume, and use shadow deployment before enabling notifications.
---

# Validate and test rules

Before enabling a new detection rule in production, validate that it detects what you intend, at a volume your team can handle, without generating excessive false positives. The steps below apply to any [rule type](/solutions/security/detect-and-alert/rule-types.md).

## Validate against historical data [validate-historical-data]

Use the rule preview feature to test your rule's query against a historical time range before enabling it. This shows you what the rule would have detected without creating actual alerts.

1. While creating or editing a rule, select **Preview** in the rule builder.
2. Select a time range that represents normal activity in your environment. A range of 7 to 14 days captures both weekday and weekend patterns.
3. Review the preview results. Look for:
   - **Expected true positives.** Does the rule detect the activity it's designed to catch? If you have known-good test data (for example, from red team exercises), confirm those events appear in the results.
   - **Obvious false positives.** Do any results represent legitimate activity? If so, refine the query or plan to add [exceptions](/solutions/security/detect-and-alert/rule-exceptions.md) before enabling the rule.
   - **Missing detections.** If the rule produces no results and you expected it to, check that the required data sources are being ingested and that your index patterns are correct.

::::{tip}
If the rule uses [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md), use the rule preview to visualize how suppression affects the alert output. This helps you confirm that suppression is grouping events as expected before the rule goes live.
::::

## Run a manual test [manual-test-run]

For rules that are already enabled, you can [manually run](/solutions/security/detect-and-alert/manage-detection-rules.md#manually-run-rules) them over a specific time range to test behavior against real data. Unlike preview, manual runs create actual alerts and trigger rule actions.

Manual runs are useful when:

- You want to test a rule against a specific incident window where you know what happened.
- You need to fill a gap in rule coverage after a rule was temporarily not running.
- You want to verify that a rule change produces the expected results in production.

::::{important}
Manual runs activate all configured [rule actions](/solutions/security/detect-and-alert/rule-settings-reference.md#rule-notifications) except **Summary of alerts** actions that run at a custom frequency. If you want to test without sending notifications, [snooze the rule's actions](/solutions/security/detect-and-alert/snooze-rule-actions.md) first.
::::

## Estimate alert volume [estimate-alert-volume]

High-volume rules can overwhelm analysts and degrade rule execution performance. Before enabling a rule, estimate its expected alert rate.

1. Review the preview result count from the historical validation step. Divide by the number of days in your preview range to get a daily estimate.
2. Compare this estimate against your team's capacity. A rule generating hundreds of alerts per day may need to be narrowed before it delivers value.
3. If volume is too high, consider:
   - Narrowing the query to be more specific.
   - Adding [alert suppression](/solutions/security/detect-and-alert/alert-suppression.md) to deduplicate repeated alerts for the same entity.
   - Adjusting the rule's schedule interval if a longer interval is acceptable for the threat you're detecting.

## Assess false positive rate [assess-false-positives]

A rule that produces mostly false positives trains analysts to ignore it. Evaluate the signal-to-noise ratio before going live.

1. Sample 20 to 50 results from your preview and classify each as a true positive, false positive, or uncertain.
2. If more than half are false positives, refine the rule before enabling it. Common adjustments include:
   - Adding field constraints to the query (for example, excluding known service accounts or internal IP ranges).
   - Preparing [exceptions](/solutions/security/detect-and-alert/rule-exceptions.md) for specific known-safe cases.
   - Switching to a more targeted [rule type](/solutions/security/detect-and-alert/choose-the-right-rule-type.md) if the current type is too broad for the detection goal.
3. Document the false positive patterns you find. This helps other analysts understand the rule's limitations and speeds up triage.

## Shadow deployment [shadow-deployment]

Shadow deployment means enabling a rule in production but suppressing its notifications so you can observe real alert output before analysts are paged.

1. Create and enable the rule normally.
2. [Snooze the rule's actions](/solutions/security/detect-and-alert/snooze-rule-actions.md) to suppress notifications. The rule runs on its schedule and writes alerts to the index, but no emails, Slack messages, or webhook calls are sent.
3. Let the rule run for a representative period (typically 3 to 7 days).
4. Review the alerts it generates in the **Alerts** table. Evaluate:
   - Is the volume manageable?
   - Are the alerts actionable?
   - Do any patterns suggest the query needs further tuning or exceptions?
5. Once you're confident in the rule's output, unsnooze the actions to begin sending notifications.

::::{tip}
Shadow deployment is especially useful for rules that are difficult to validate with historical data alone, such as [threshold rules](/solutions/security/detect-and-alert/threshold.md) where volume depends on live traffic patterns, or [{{ml}} rules](/solutions/security/detect-and-alert/machine-learning.md) where anomaly baselines evolve over time.
::::

## Post-enablement monitoring [post-enablement-monitoring]

Validation doesn't end when a rule goes live. Monitor newly enabled rules closely during their first weeks in production.

- **Check execution health.** Use the [Rule Monitoring tab](/solutions/security/detect-and-alert/monitor-rule-executions.md) to confirm the rule is executing successfully and not timing out or failing.
- **Track alert volume trends.** A sudden spike or drop in alert volume can indicate a change in the data source, a rule misconfiguration, or an emerging incident.
- **Collect analyst feedback.** Ask the analysts triaging the rule's alerts whether they find them actionable. If a rule consistently produces alerts that are closed without investigation, it needs further tuning.
- **Review after one to two weeks.** Revisit the rule's configuration after it has run through a full operational cycle. Adjust the query, exceptions, suppression, or schedule based on what you've learned.

## Test rules externally with Detection-as-Code [test-rules-dac]

If you manage rules outside of the {{kib}} UI, you can use [Detection-as-Code](https://dac-reference.readthedocs.io/en/latest/dac_concept_and_workflows.html) (DaC) workflows to test rules before deploying them. The Elastic Security Labs team maintains the [detection-rules](https://github.com/elastic/detection-rules) repo, which provides tooling for developing, testing, and releasing detection rules programmatically.

DaC workflows let you:

- Validate rule syntax and schema before deployment.
- Run unit tests against rule logic in a CI/CD pipeline.
- Track rule changes in version control for auditability.

To get started, refer to the [DaC documentation](https://github.com/elastic/detection-rules/blob/main/README.md#detections-as-code-dac). For managing rules through the API, refer to [Using the API](/solutions/security/detect-and-alert/using-the-api.md).

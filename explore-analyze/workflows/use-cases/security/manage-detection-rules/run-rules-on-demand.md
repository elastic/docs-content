---
navigation_title: Run rules on demand
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build a workflow that manually re-runs a set of detection rules over a configurable time range, useful for gap-filling, post-incident review, or scheduled rule-health checks.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Run detection rules on demand [workflows-run-rules-on-demand]

This guide walks through building a workflow that triggers a manual execution of one or more detection rules over a specific time range. Use it for gap-filling after a detection rule change, post-incident review, scheduled health checks, or any time you need to run rules outside their normal cadence.

The workflow is adapted from [`manually-run-rules.yaml`](https://github.com/elastic/workflows/blob/main/workflows/security/detection/manually-run-rules.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first.

## Before you begin [workflows-run-rules-prereqs]

- **Permissions.** `All` on **Analytics > Workflows** and on **Security > Detection rules** in the target space. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **Rule IDs.** The `rule_id` values of the detection rules you want to run. You can copy them from the **Rules** table in {{elastic-sec}} or from a saved-object export.
- **Time range.** The lookback window for this manual run. The default in this workflow is the last 15 minutes, which matches the interval of most default rules.

## How it works [workflows-run-rules-how-it-works]

The workflow runs on demand with a list of rule IDs:

1. **Manual trigger** with a `rule_ids` array input.
2. **`foreach` step** iterates the rule IDs.
3. For each rule, a **`kibana.request` step** calls the detection engine's `POST /api/detection_engine/rules/_bulk_action` endpoint with the `run` action and a configurable time range.

## Build the workflow [workflows-run-rules-build]

:::::{stepper}

::::{step} Declare the rule IDs and time window as inputs

Inputs make the workflow reusable without editing YAML. Declare both the list of rule IDs and the lookback window in minutes.

This example uses the stack 9.5+ and serverless structure, where `inputs` nests under the `manual` trigger. On stack 9.4 and earlier, `inputs` sits at the workflow root. Refer to [Workflow anatomy](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs) for both forms.

```yaml
triggers:
  - type: manual
    inputs:
      - name: rule_ids
        type: array
        description: Detection rule IDs to run.
        required: true
      - name: lookback_minutes
        type: number
        description: How many minutes back to run the rule.
        default: 15
```
::::

::::{step} Loop over the rule IDs

Use a `foreach` step to iterate. Inside the loop, `foreach.item` is the current rule ID:

```yaml
steps:
  - name: for_each_rule
    type: foreach
    foreach: "${{ inputs.rule_ids }}"
    steps:
      # Per-rule step goes here. Use foreach.item for the current rule ID.
```

Note the `${{ inputs.rule_ids }}` form. Use `${{ ... }}` whenever you're passing an array or object to a step parameter, so the value isn't stringified. Refer to [Templating engine](/explore-analyze/workflows/templating.md) for the `{{ }}` vs. `${{ }}` distinction.
::::

::::{step} Trigger the rule run with `kibana.request`

Call the detection engine's bulk action endpoint to run the rule over the lookback window. Build the `start` and `end` timestamps with Liquid date filters:

```yaml
      - name: run_rule
        type: kibana.request
        with:
          method: POST
          path: /api/detection_engine/rules/_bulk_action
          body:
            action: run
            ids:
              - "{{ foreach.item }}"
            run:
              start_date: "{{ 'now' | date: '%s' | minus: inputs.lookback_minutes | times: 60 | date: '%Y-%m-%dT%H:%M:%S' }}.000Z"
              end_date: "{{ 'now' | date: '%Y-%m-%dT%H:%M:%S' }}.000Z"
```

The two Liquid expressions compute ISO timestamps: the start is `now - lookback_minutes minutes`, and the end is `now`. Adjust the expressions if you need a different window shape.
::::

:::::

## Complete workflow [workflows-run-rules-complete]

:::{dropdown} Full workflow YAML

```yaml
name: security--run-rules-on-demand
description: Manually run one or more detection rules over a configurable lookback window.
enabled: true
tags: ["rule-ops", "detection"]

triggers:
  - type: manual
    inputs:
      - name: rule_ids
        type: array
        description: Detection rule IDs to run.
        required: true
      - name: lookback_minutes
        type: number
        description: How many minutes back to run the rule.
        default: 15

steps:
  - name: for_each_rule
    type: foreach
    foreach: "${{ inputs.rule_ids }}"
    steps:
      - name: log_rule
        type: console
        with:
          message: "Running rule {{ foreach.item }}"

      - name: run_rule
        type: kibana.request
        with:
          method: POST
          path: /api/detection_engine/rules/_bulk_action
          body:
            action: run
            ids:
              - "{{ foreach.item }}"
            run:
              start_date: "{{ 'now' | date: '%s' | minus: inputs.lookback_minutes | times: 60 | date: '%Y-%m-%dT%H:%M:%S' }}.000Z"
              end_date: "{{ 'now' | date: '%Y-%m-%dT%H:%M:%S' }}.000Z"
```

:::

## Extend this workflow [workflows-run-rules-extend]

- **Run on a schedule.** Replace the `manual` trigger with a [scheduled trigger](/explore-analyze/workflows/triggers/scheduled-triggers.md) that fires every hour and passes a fixed rule list through `consts`.
- **Audit before you run.** Chain a `kibana.request` `GET /api/detection_engine/rules` step first to fetch each rule's status and skip rules that are disabled or in error.
- **Summarize results.** After the loop, post the number of rules run to Slack or index a summary document with [`elasticsearch.request`](/explore-analyze/workflows/steps/elasticsearch.md) for dashboarding.
- **Stop on first failure.** Replace the per-iteration error handling with a strict `on-failure: abort` so the workflow fails fast if any one rule can't be triggered.

## Related pages [workflows-run-rules-related]

- [Manage detection rules at scale](/explore-analyze/workflows/use-cases/security/manage-detection-rules.md): The outcome this workflow supports.
- [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md): Reference for `kibana.request` and named Kibana actions.
- [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md): Turn this into a recurring job.
- [Detection rule concepts](/solutions/security/detect-and-alert/detection-rule-concepts.md): Background on how detection rules run.
- [Manage detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md): The UI surface this workflow automates.
- [Monitor rule executions](/solutions/security/detect-and-alert/monitor-rule-executions.md): Where to check whether your manual runs succeeded and whether they covered every event.
- [`elastic/workflows` detection folder](https://github.com/elastic/workflows/tree/main/workflows/security/detection): More rule-operations examples.

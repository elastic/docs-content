---
navigation_title: Monitor workflow execution
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Track workflow runs in real time, review execution history, and troubleshoot workflow failures in Kibana.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Monitor workflow execution [workflows-monitor-troubleshoot]

After you run a workflow, you can track its progress in real time, review past executions, and diagnose any failures. This page explains how to use the execution panel and logs on the **Executions tab** to understand what happened during a workflow run.

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](/explore-analyze/workflows/get-started/setup.md) for more information.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

## Monitor execution [workflows-monitor-execution]

When a workflow runs, the execution panel displays:

- **Real-time logs**: Each step appears as it executes.
- **Status indicators**: Green indicates success and red represents failure.
- **Timestamps**: The duration of each step.
- **Expandable details**: Click any step to examine details such as input parameters, output data, and execution timelines.

## See what triggered a run [workflows-execution-trigger-source]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

Every execution begins with a trigger entry that shows how the run started, such as a manual run, a schedule, an alert, or an event. Expand this entry to see the input the workflow received, including the full event payload for [event-driven](/explore-analyze/workflows/triggers/event-driven-triggers.md) runs. This lets you trace an execution back to the event or action that started it, which is especially useful when workflows react to one another through event-driven triggers.

## View execution history [workflows-execution-history]

To review past runs, select the **Executions** tab, then click each run to see detailed logs. Workflow runs can be `Pending`, `In progress`, `Completed`, or `Failed`. 

## Filter historical executions by time range [workflows-execution-history-time-range]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

**Run again** and **Run step again** replay a past execution instead of triggering a new manual run. They reuse the input and context from an execution you select, which is useful for reproducing an issue or testing a step change against real prior data. The execution picker in these dialogs includes a time-range filter next to the selection list. The filter defaults to the last week through now, so you can narrow a long execution history down to the runs you care about.

When you open replay from a specific execution (for example, by selecting **Run again** or **Run step again** on that execution's details), Kibana anchors the range to it automatically: the end of the range becomes that run's start time, which covers the week leading up to it. If you then adjust the range so the selected execution no longer falls within it, Kibana clears the selection, and you need to choose a new execution before you can submit the replay.

## Troubleshoot errors [workflows-troubleshoot-errors]

When a workflow fails, open the failed execution from the **Executions** tab, then find the step with the error indicator. Expand the step to view the error message and to learn more about the root cause, such the input that caused the failure. After fixing an error, save the workflow before running it again.  

Common issues that can cause failures:

| Issue | Cause | Solution |
|-------|-------|----------|
| Syntax error | Invalid YAML | Check indentation and formatting. |
| Step failed | Action error | Review step configuration and inputs. |
| Missing variable | Undefined reference | Verify variable names and data flow. |
---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to monitor Elastic workflows executions and troubleshoot errors. 
---

# Monitor and troubleshoot workflows [workflows-monitor-troubleshoot]

After you run a workflow, you can track its progress in real time, review past executions, and diagnose any failures. This page explains how to use the execution panel and logs on the **Executions tab** to understand what happened during a workflow run.

::::{admonition} Requirements
To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. Refer to [](setup.md) for more information.

You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.
::::

## Monitor execution [workflows-monitor-execution]

When a workflow runs, the execution panel displays:

- **Real-time logs**: Each step appears as it executes.
- **Status indicators**: Green indicates success and red represents failure.
- **Timestamps**: The duration of each step.
- **Expandable details**: Click any step to examine details such as input parameters, output data, and execution timelines.

## View execution history [workflows-execution-history]

To review past runs, select the **Executions** tab, then click each run to see detailed logs. Workflow runs can be `Pending`, `In progress`, `Completed`, or `Failed`. 

## Troubleshoot errors [workflows-troubleshoot-errors]

When a workflow fails, open the failed execution from the **Executions** tab, then find the step with the error indicator. Expand the step to view the error message and to learn more about the root cause, such the input that caused the failure. After fixing an error, save the workflow before running it again.  

Common issues that can cause failures:

| Issue | Cause | Solution |
|-------|-------|----------|
| Syntax error | Invalid YAML | Check indentation and formatting. |
| Step failed | Action error | Review step configuration and inputs. |
| Missing variable | Undefined reference | Verify variable names and data flow. |
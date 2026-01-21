---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to monitor Elastic workflows executions and troubleshoot errors. 
---

# Monitor and troubleshoot workflows [workflows-monitor-troubleshoot]

After you run a workflow, you can track its progress in real time, review past executions, and diagnose any failures. This page explains how to use the execution panel and logs to understand what happened during a workflow run.

## Monitor execution [workflows-monitor-execution]

When a workflow runs, the execution panel displays:

- **Real-time logs**: Each step appears as it executes
- **Status indicators**: Green checkmarks for success, red for failure
- **Timestamps**: Duration for each step
- **Expandable details**: Click any step to view:
  - Input parameters
  - Output data
  - Execution timeline

## View execution history [workflows-execution-history]

To review past executions:

1. Click the **Executions** tab.
2. View all workflow runs with their status:
   - **Pending**: Waiting to start
   - **In progress**: Currently running
   - **Completed**: Finished successfully
   - **Failed**: Encountered an error
3. Click any execution to see detailed logs.

## Troubleshoot errors [workflows-troubleshoot-errors]

When a workflow fails:

1. Open the failed execution from the **Executions** tab.
2. Find the step with the error indicator.
3. Expand the step to view:
   - Error message
   - Input that caused the failure
   - Stack trace (if available)

Common issues:

| Issue | Cause | Solution |
|-------|-------|----------|
| Syntax error | Invalid YAML | Check indentation and formatting |
| Step failed | Action error | Review step configuration and inputs |
| Missing variable | Undefined reference | Verify variable names and data flow |
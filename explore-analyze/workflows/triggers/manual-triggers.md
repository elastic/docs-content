---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Understand manual triggers and how to create and configure them.
---

# Manual triggers

Manual triggers run workflows on-demand through the UI or API. They require explicit user action to start a workflow. Use manual triggers for testing, one-off tasks, administrative actions, or workflows that require a human decision to start.

To define a manual trigger, use the following syntax:

```yaml
triggers:
  - type: manual
```

This allows you to run a workflow manually by:

* Clicking **Run** in the Workflows UI
* Calling the workflow execution API, either directly or from an external system

## Input parameters

Manual triggers can accept input parameters, which you can reference in any step. When you define inputs at the workflow level, users are prompted to provide values when they run the workflow. Use inputs for values that may vary between runs. For fixed values like index names or API endpoints, use [constants](/explore-analyze/workflows/data.md#workflows-constants-vs-inputs) instead.

```yaml
name: Manual Processing Workflow
inputs:
  - name: environment
    type: string
    required: true
    default: "staging"
    description: "Target environment for processing"
  
  - name: batchSize
    type: number
    required: false
    default: 100
    description: "Number of records to process"
  
  - name: dryRun
    type: boolean
    required: false
    default: true
    description: "Run in test mode without making changes"

triggers:
  - type: manual

steps:
  - name: validateInputs
    type: console
    with:
      message: |
        Starting workflow with:
        - Environment: {{ inputs.environment }}
        - Batch Size: {{ inputs.batchSize }}
        - Dry Run: {{ inputs.dryRun }}
```


---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about Elastic workflows. 
---

# Workflows [workflows-overview]

A workflow is a defined sequence of steps designed to achieve a specific outcome through automation. It is a reusable, versionable "recipe" that transforms inputs into actions.

## Why use workflows [workflows-why]

Insight into your data isn't enough. The ultimate value lies in action and outcomes. Workflows complete the journey from data to insights to automated outcomes. Your critical operational data already lives in the Elastic cluster: security events, infrastructure metrics, application logs, and business context. Workflows let you automate end-to-end processes to achieve outcomes directly where that data lives, without needing external automation tools.

Workflows address common operational challenges, such as:

* **Alert fatigue**: Automate responses to reduce manual triage.
* **Understaffing**: Enable teams to do more with fewer resources.
* **Manual, repetitive work**: Automate routine tasks consistently.
* **Tool fragmentation**: Eliminate the need to add on external automation tools.

Workflows can handle a wide range of tasks, from simple, repeatable steps to complex processes.

## Who should use workflows [workflows-who]

Workflows are for you if you want to cut down on manual effort, speed up response times, and make sure recurring situations are handled consistently.

## Key concepts [workflows-concepts]

Some key concepts to understand while working with workflows: 

* **Triggers**: The events or conditions that initiate a workflow. Refer to [](/explore-analyze/workflows/triggers.md) to learn more.
* **Steps**: The individual units of logic or action that make up a workflow. Refer to [](/explore-analyze/workflows/steps.md) to learn more.
* **Data**: How data flows through your workflow, including inputs, constants, context variables, step outputs, and Liquid templating for dynamic values. Refer to [](/explore-analyze/workflows/data.md) to learn more.
* **Variables and constants**: Dynamic values you can reference throughout your workflow using template expressions. To understand when to use each, refer to [Choose between constants and inputs](/explore-analyze/workflows/data.md#workflows-constants-or-inputs). For a complete reference of available variables, refer to [Context variables reference](/explore-analyze/workflows/data/templating.md#workflows-context-variables).

## Workflow structure [workflow-structure]

Workflows are defined in YAML. In the YAML editor, describe _what_ the workflow should do, and the platform handles execution.

```yaml
# ═══════════════════════════════════════════════════════════════
# METADATA - Identifies and describes the workflow
# ═══════════════════════════════════════════════════════════════
name: My Workflow                    # Required: Unique identifier 
description: What this workflow does # Optional: Shown in UI
enabled: true                        # Optional: Enable or disable execution
tags: ["demo", "production"]         # Optional: For organizing workflows

# ═══════════════════════════════════════════════════════════════
# CONSTANTS - Reusable values defined once, used throughout
# ═══════════════════════════════════════════════════════════════
consts:
  indexName: "my-index"
  environment: "production"
  alertThreshold: 100
  endpoints:                          # Can be objects/arrays
    api: "https://api.example.com"
    backup: "https://backup.example.com"

# ═══════════════════════════════════════════════════════════════
# INPUTS - Parameters passed when the workflow is triggered
# ═══════════════════════════════════════════════════════════════
inputs:
  - name: environment
    type: string
    required: true
    default: "staging"
    description: "Target environment"
  - name: dryRun
    type: boolean
    default: true

# ═══════════════════════════════════════════════════════════════
# TRIGGERS - How/when the workflow starts
# ═══════════════════════════════════════════════════════════════
triggers:
  - type: manual                      # User clicks Run button
  # - type: scheduled                  # Runs on a schedule
  #   with:
        every: 1d
  # - type: alert                     # Triggered by an alert

# ═══════════════════════════════════════════════════════════════
# STEPS - The actual workflow logic (executed in order)
# ═══════════════════════════════════════════════════════════════
steps:
  - name: step_one
    type: elasticsearch.search
    with:
      index: "{{consts.indexName}}"   # Reference constants
      query:
        match_all: {}

  - name: step_two
    type: console
    with:
      message: |
        Environment: {{inputs.environment}}              # Reference inputs
        Found: {{steps.step_one.output.hits.total.value}} # Reference step output

```

## Learn more

- To create and run your first workflow, refer to [](/explore-analyze/workflows/get-started.md).
- Understand how to use the YAML editor in {{kib}} to define and run your workflows. Refer to [](/explore-analyze/workflows/author-workflows.md) to learn more.

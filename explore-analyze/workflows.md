---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about Elastic workflows. 
---

# Workflows [workflows-overview]

A workflow is a defined sequence of steps designed to achieve a specific outcome through automation. It is a reusable, versionable "recipe" that transforms inputs into actions.

Workflows are for anyone who wants to cut down on manual effort, speed up response times, and make sure recurring situations are handled the same way every time.

## Why use workflows? [workflows-why]

Insights on your data isn't enough. The ultimate value lies in action and outcomes. Workflows complete the journey from data to insight to automated outcomes. Your critical operational data already lives in Elastic: security events, infrastructure metrics, application logs, and business context. Workflows let you automate end-to-end outcomes directly where that data lives, without needing external automation tools.

Workflows address common operational challenges, such as:

* **Alert fatigue**: Automate responses to reduce manual triage.
* **Understaffing**: Enable teams to do more with fewer resources.
* **Manual, repetitive work**: Automate routine tasks consistently.
* **Tool fragmentation**: Eliminate the need to bolt on external automation tools.

Workflows can handle everything from simple, repeatable tasks to complex processes.

## Key components [workflows-components]

Every workflow is composed of three core elements:

* **Triggers**: The events or conditions that initiate a workflow. Triggers define _when_ a workflow runs.
* **Steps**: The individual units of logic or action that make up a workflow. Steps define _how_ data moves, decisions are made, and results are produced.
* **Connectors**: The integrations that allow workflows to interact with external systems and services. Connectors define _where_ actions are executed.


---
navigation_title: Classify and route alerts
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build a workflow that classifies incoming items with ai.classify, routes each item down a different branch, and summarizes the result with ai.summarize.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Classify and route mixed items with AI [workflows-classify-and-route-alerts]

This guide walks through building a workflow that takes a stream of mixed items (alerts, tickets, log entries) and routes each one down a different branch based on an AI classification. The workflow pairs the [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify) step with [`foreach`](/explore-analyze/workflows/steps/foreach.md) and [`if`](/explore-analyze/workflows/steps/if.md) or [`switch`](/explore-analyze/workflows/steps/switch.md), so each item gets exactly the handling it needs.

The workflow is adapted from [`ai-steps-demo.yaml`](https://github.com/elastic/workflows/blob/main/workflows/observability/ai-steps-demo.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first.

## Before you begin [workflows-classify-route-prereqs]

- **Permissions.** `All` on **Analytics > Workflows**. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **AI connector.** A configured LLM connector (Azure OpenAI, OpenAI, Anthropic, or Bedrock). Refer to [Connectors](/deploy-manage/manage-connectors.md). Note the connector ID.
- **A set of items to classify.** For this walkthrough, the workflow generates sample items with `ai.prompt`. In production, you'd read items from an alert trigger (`event.alerts`), an Elasticsearch search, or an upstream workflow.

## How it works [workflows-classify-route-how-it-works]

The workflow runs manually during development and can be switched to an alert trigger once you're happy with the routing:

1. **Gather items.** For the demo, two `ai.prompt` steps produce a mix of sample observability and security alerts. In production, replace this with your real data source.
2. **Iterate with `foreach`.** Each item is processed independently.
3. **Classify with `ai.classify`.** The step returns the category (for example, `observability alert` or `security alert`) and an optional rationale.
4. **Route with `if` (or `switch`).** Each branch runs the right follow-up: severity classification for observability, malicious-or-not classification for security.
5. **Summarize with `ai.summarize`.** The summary is attached to the routed item.

## Build the workflow [workflows-classify-route-build]

:::::{stepper}

::::{step} Declare the AI connector as a constant

Hold the connector ID in a constant so you can swap environments without touching step bodies:

```yaml
consts:
  llm_connector: "your-connector-id"

triggers:
  - type: manual
```
::::

::::{step} Gather items to classify

For development, generate a mix of sample items with two `ai.prompt` calls. Each call uses a JSON schema so the output is strongly typed and iterable:

```yaml
steps:
  - name: gather_observability_items
    type: ai.prompt
    connector-id: "{{ consts.llm_connector }}"
    with:
      prompt: "Generate two sample observability alerts."
      schema:
        items:
          type: object
          required: [id, severity, message]
          properties:
            id: { type: string }
            severity: { type: string, enum: [critical, high, medium, low] }
            message: { type: string }

  - name: gather_security_items
    type: ai.prompt
    connector-id: "{{ consts.llm_connector }}"
    with:
      prompt: "Generate three sample security alerts."
      schema:
        items:
          type: object
          required: [id, severity, category]
          properties:
            id: { type: string }
            severity: { type: string, enum: [critical, high, medium, low] }
            category: { type: string }
```

In a production workflow, replace these two steps with a real data source. For example, read `event.alerts` from an alert trigger or run an `elasticsearch.search` step.
::::

::::{step} Loop through the combined stream

Concatenate the two sample arrays and loop over the combined stream. Use `${{ ... }}` when passing arrays so they aren't stringified:

```yaml
  - name: route_each_item
    type: foreach
    foreach: "${{ steps.gather_observability_items.output.content | concat: steps.gather_security_items.output.content }}"
    steps:
      # Classification and branching steps go here. Use foreach.item.
```
::::

::::{step} Classify each item

Call `ai.classify` with the categories you want to route on. Set `includeRationale: true` during development so you can see why the model picked a category. Turn it off in production for lower token cost:

```yaml
      - name: identify_type
        type: ai.classify
        connector-id: "{{ consts.llm_connector }}"
        with:
          input: "${{ foreach.item }}"
          includeRationale: true
          categories:
            - "security alert"
            - "observability alert"
          fallbackCategory: "other"
```

The category ends up at `steps.identify_type.output.category`.
::::

::::{step} Branch on the classification

Use `if` steps for two branches, or `switch` for three or more. The following pattern uses `if` for clarity:

```yaml
      - name: handle_observability
        type: if
        condition: "steps.identify_type.output.category : 'observability alert'"
        steps:
          - name: classify_severity
            type: ai.classify
            connector-id: "{{ consts.llm_connector }}"
            with:
              input: "${{ foreach.item }}"
              categories: ["critical", "high", "medium", "low"]

          - name: store_observability_result
            type: data.set
            with:
              type: "observability"
              item: "${{ foreach.item }}"
              severity: "${{ steps.classify_severity.output.category }}"

      - name: handle_security
        type: if
        condition: "steps.identify_type.output.category : 'security alert'"
        steps:
          - name: classify_safety
            type: ai.classify
            connector-id: "{{ consts.llm_connector }}"
            with:
              input: "${{ foreach.item }}"
              categories: ["malicious", "not malicious"]
              fallbackCategory: "unknown"

          - name: store_security_result
            type: data.set
            with:
              type: "security"
              item: "${{ foreach.item }}"
              status: "${{ steps.classify_safety.output.category }}"
```

For more than two branches, use a [`switch` step](/explore-analyze/workflows/steps/switch.md) which reads cleaner than chained `if`/`else`.
::::

::::{step} Summarize the item

Add an `ai.summarize` call to produce a human-readable summary. Run it after classification so later steps can include both the category and the summary:

```yaml
      - name: summarize_item
        type: ai.summarize
        connector-id: "{{ consts.llm_connector }}"
        with:
          input: "${{ foreach.item }}"
```

`steps.summarize_item.output.content` is the summary string.
::::

:::::

## Complete workflow [workflows-classify-route-complete]

:::{dropdown} Full workflow YAML

```yaml
name: ai--classify-and-route
description: Classify a stream of mixed items and route each one down the right branch.
enabled: true
tags: ["ai", "classify", "route"]

consts:
  llm_connector: "your-connector-id"

triggers:
  - type: manual

steps:
  - name: gather_observability_items
    type: ai.prompt
    connector-id: "{{ consts.llm_connector }}"
    with:
      prompt: "Generate two sample observability alerts."
      schema:
        items:
          type: object
          required: [id, severity, message]
          properties:
            id: { type: string }
            severity: { type: string, enum: [critical, high, medium, low] }
            message: { type: string }

  - name: gather_security_items
    type: ai.prompt
    connector-id: "{{ consts.llm_connector }}"
    with:
      prompt: "Generate three sample security alerts."
      schema:
        items:
          type: object
          required: [id, severity, category]
          properties:
            id: { type: string }
            severity: { type: string, enum: [critical, high, medium, low] }
            category: { type: string }

  - name: route_each_item
    type: foreach
    foreach: "${{ steps.gather_observability_items.output.content | concat: steps.gather_security_items.output.content }}"
    steps:
      - name: identify_type
        type: ai.classify
        connector-id: "{{ consts.llm_connector }}"
        with:
          input: "${{ foreach.item }}"
          includeRationale: true
          categories:
            - "security alert"
            - "observability alert"
          fallbackCategory: "other"

      - name: summarize_item
        type: ai.summarize
        connector-id: "{{ consts.llm_connector }}"
        with:
          input: "${{ foreach.item }}"

      - name: handle_observability
        type: if
        condition: "steps.identify_type.output.category : 'observability alert'"
        steps:
          - name: classify_severity
            type: ai.classify
            connector-id: "{{ consts.llm_connector }}"
            with:
              input: "${{ foreach.item }}"
              categories: ["critical", "high", "medium", "low"]

          - name: store_observability_result
            type: data.set
            with:
              type: "observability"
              item: "${{ foreach.item }}"
              severity: "${{ steps.classify_severity.output.category }}"
              summary: "${{ steps.summarize_item.output.content }}"

      - name: handle_security
        type: if
        condition: "steps.identify_type.output.category : 'security alert'"
        steps:
          - name: classify_safety
            type: ai.classify
            connector-id: "{{ consts.llm_connector }}"
            with:
              input: "${{ foreach.item }}"
              categories: ["malicious", "not malicious"]
              fallbackCategory: "unknown"

          - name: store_security_result
            type: data.set
            with:
              type: "security"
              item: "${{ foreach.item }}"
              status: "${{ steps.classify_safety.output.category }}"
              summary: "${{ steps.summarize_item.output.content }}"
```

:::

## Extend this workflow [workflows-classify-route-extend]

- **Trigger from real alerts.** Replace the `manual` trigger and the two `gather_*` steps with an [alert trigger](/explore-analyze/workflows/triggers/alert-triggers.md) and a `foreach` over `event.alerts`.
- **Use `switch` for many categories.** When you have three or more branches, replace the `if` pair with a [`switch` step](/explore-analyze/workflows/steps/switch.md) for cleaner YAML.
- **Follow each branch with a real action.** Replace the `data.set` calls with `cases.createCase`, `http` (Slack, PagerDuty), or [composition](/explore-analyze/workflows/steps/composition.md) calls that invoke a dedicated child workflow for each category.
- **Persist the enriched stream.** Write the classified items back to {{es}} with [`elasticsearch.request`](/explore-analyze/workflows/steps/elasticsearch.md) for dashboarding.

## Related pages [workflows-classify-route-related]

- [AI-augmented workflows](/explore-analyze/workflows/use-cases/ai-augmented-workflows.md): The outcome this workflow supports.
- [AI steps reference](/explore-analyze/workflows/steps/ai-steps.md): Parameters for `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent`.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): `foreach`, `if`, `switch`, and others.
- [{{elastic-sec}} AI use cases](/solutions/security/ai/use-cases.md): Where this kind of automation fits among the other AI-powered tools available to SOC users.
- [`elastic/workflows` observability folder](https://github.com/elastic/workflows/tree/main/workflows/observability): More observability workflow examples.

---
applies_to:
  stack: ga 9.4+, preview 9.3
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
description: Internal test results comparing large language models across Elastic Security Agent Builder capabilities.
---

# Agent Builder LLM performance matrix for {{elastic-sec}} [agent-builder-llm-performance-matrix]

This page summarizes internal test results comparing large language models (LLMs) across [Agent Builder](/solutions/security/ai/agent-builder/agent-builder.md) capabilities and related {{elastic-sec}} AI-powered features. For the equivalent ratings covering [AI Assistant](/solutions/security/ai/ai-assistant.md) and AI chat use cases, refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md). To learn more about these use cases, refer to [AI-powered features](/explore-analyze/ai-features.md#security-features).

::::{important}
Higher scores indicate better performance. A score of 10 on a task means the model met or exceeded all task-specific benchmarks.

Models with a score of "Not recommended" failed testing. This could be due to various issues, including context window constraints.
::::

The **Agent Builder** columns (Alert Triage, Detection Engineering, Investigation, Workflow Execution, and Multi-step execution) measure the capabilities exercised through Agent Builder. **Agent Builder Score** is the average of those five capabilities. **Attack Discovery** and **Automatic Migration** are scored as standalone features, and **Overall Score** is the average of the Agent Builder Score, Attack Discovery, and Automatic Migration.

% The tables below are generated automatically from Elastic Security LLM evaluation
% results. Do not edit them by hand: update the CSVs via the `Sync LLM matrix`
% automation (see .github/workflows/sync-llm-matrix-keyless.yml), which pulls the
% latest artifacts produced by the `kibana-evals-security-matrix` Buildkite pipeline.

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

:::{csv-include} agent-builder-llm-performance-matrix/proprietary-models.csv
:caption: Scroll horizontally to view more information.
:::

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

:::{csv-include} agent-builder-llm-performance-matrix/open-source-models.csv
:caption: Scroll horizontally to view more information.
:::

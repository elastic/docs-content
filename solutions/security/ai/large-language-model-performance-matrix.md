---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/llm-performance-matrix.html
  - https://www.elastic.co/guide/en/serverless/current/security-llm-performance-matrix.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Large language model performance matrix for {{elastic-sec}} [llm-performance-matrix]

This page summarizes internal test results comparing large language models (LLMs) across {{elastic-sec}} [AI chat](/explore-analyze/ai-features/ai-chat-experiences.md) and AI-powered feature use cases. These ratings apply equally whether you're using [AI Assistant](/solutions/security/ai/ai-assistant.md) or [Agent Builder](/solutions/security/ai/agent-builder/agent-builder.md). To learn more about these use cases, refer to [AI-powered features](/explore-analyze/ai-features.md#security-features).

::::{important}
Higher scores indicate better performance. A score of 10 on a task means the model met or exceeded all task-specific benchmarks.

Models with a score of "Not recommended" failed testing. This could be due to various issues, including context window constraints.
::::

% The tables below are generated automatically from Elastic Security LLM evaluation
% results. Do not edit them by hand: update the CSVs via the `Sync LLM matrix`
% automation (see .github/workflows/sync-llm-matrix-keyless.yml), which pulls the
% latest artifacts produced by the `kibana-evals-security-matrix` Buildkite pipeline.

## Proprietary models [_proprietary_models]

Models from third-party LLM providers.

:::{csv-include} llm-performance-matrix/proprietary-models.csv
:caption: Scroll horizontally to view more information.
:::

## Open-source models [_open_source_models]

Models you can [deploy yourself](/explore-analyze/ai-features/llm-guides/local-llms-overview.md).

:::{csv-include} llm-performance-matrix/open-source-models.csv
:caption: Scroll horizontally to view more information.
:::

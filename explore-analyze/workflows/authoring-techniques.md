---
navigation_title: Workflow authoring techniques
applies_to:
  stack: preview 9.3
  serverless: preview
description: Techniques for authoring, running, monitoring, and organizing Elastic Workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflow authoring techniques [workflows-authoring-techniques]

Techniques that apply across workflow types, regardless of which outcome you're automating. Use this section when you're building or maintaining a workflow and need guidance on the mechanics.

- [Use the YAML editor](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md): Author and run workflows in the YAML editor in {{kib}}.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): Move data between steps, use dynamic templating, and make workflows resilient with `on-failure`.
- [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md): Track runs, review execution history, and troubleshoot failures.
- [Manage and organize workflows](/explore-analyze/workflows/authoring-techniques/manage-workflows.md): Find, edit, duplicate, enable, and disable workflows from the **Workflows** page.

% Ben Ironside Goldstein, 2026-04-16: Follow-up PRs per Vision doc Section 7 will split pass-data-handle-errors.md
% into separate how-tos (Pass data between steps, Handle errors and retries, Use constants and inputs)
% and add Use conditional logic, Iterate over results with Foreach, Test and debug a workflow.

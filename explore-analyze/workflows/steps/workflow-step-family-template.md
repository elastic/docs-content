---
navigation_title: Workflow step family template
applies_to:
  stack: preview 9.3
  serverless: preview
description: Authoring template for documenting a workflow step family (for example, cases.* or a future product namespace).
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Template — Workflow step family reference

::::{note}
This page is an **authoring template**. Duplicate its structure when you add documentation for a new workflow step family under [](/explore-analyze/workflows/steps/). Replace placeholder text and remove this note in the published page.

The live reference for Cases steps is [](/explore-analyze/workflows/steps/cases.md).
::::

## How to use this template

1. Copy this file to `explore-analyze/workflows/steps/<family>.md` (for example `cases.md`, `observability.md`).
2. Register the file in `explore-analyze/toc.yml` under **Workflows → Steps → Action steps**, next to [](/explore-analyze/workflows/steps/elasticsearch.md) and [](/explore-analyze/workflows/steps/kibana.md).
3. Add a short entry for the step family in [](/explore-analyze/workflows/steps/action-steps.md).
4. Cross-link from related pages (for example [](/explore-analyze/workflows/steps/kibana.md) when the family complements generic `kibana.*` actions).

## Page metadata (YAML frontmatter)

Use the same pattern as other workflow step pages:

* `navigation_title`: Short title for the navigation sidebar (often the product or capability name).
* `applies_to`: Stack and serverless lifecycle (for example `preview` with a minimum version).
* `description`: One sentence for search and SEO.
* `products`: Include `kibana` and the relevant deployment products.

## Suggested page structure

### Title and introduction

* **H1**: Name the step family (for example “Cases workflow steps”).
* **Opening paragraph**: What users can automate with this family, which product area it maps to, and how it relates to [workflow steps](/explore-analyze/workflows/steps.md) overall.

### Execution and permissions

* Explain that steps run **as the workflow executor** (user or API key), consistent with [](/explore-analyze/workflows/steps/kibana.md).
* Point to solution docs for **case access, roles, and feature controls** where relevant.

### When to use this family vs generic steps

* Compare to **`kibana.request`** ([generic request](/explore-analyze/workflows/steps/kibana.md#generic-request-actions)): prefer named family steps for readability, validation, and stable fields.
* Compare to other **`kibana.*` named actions** if overlap exists (for example a default-space shortcut vs full case APIs).

### Conventions

Document cross-cutting rules for the family:

* **Identifiers**: How users pass resource IDs (`case_id`, space, owner, and so on).
* **Optimistic concurrency**: If updates require a `version` (or etag) field, describe chaining outputs (`steps.<name>.output.case.version`).
* **Outputs**: Typical shape (for example `output.case` for case-shaped responses).
* **Limits**: Batch sizes, pagination, and caps enforced by validation (align with Kibana constants when documenting numbers).

### Step catalog

Provide a **table** with at least:

| Column | Purpose |
|--------|---------|
| Step `type` | Exact string in `steps[].type` (for example `cases.createCase`). |
| Summary | One line describing behavior. |
| Notes | Optional: preview-only, disabled, or requires specific owner. |

Add **grouped subsections** (Create and read, Updates, Attachments, and so on) if the table is large.

### Detailed parameters

* Prefer **one example YAML** per common pattern rather than duplicating full schemas.
* For exhaustive field lists, link to **OpenAPI / Kibana API docs** or the workflow UI when those sources are the source of truth.
* Call out steps that are **not yet available** or **disabled** in the UI.

### Example workflow

Include a short **`steps:`** excerpt that chains two or three steps and shows templating (`${{ steps... }}`, `{{ inputs... }}`).

### Related documentation

* Link to solution docs (for example [Cases](/explore-analyze/cases.md) or [Elastic Security cases](/solutions/security/investigate/security-cases.md)).
* Link to the implementing Kibana PR or issue for **release tracking** when useful.

## Checklist before publishing

* [ ] Step `type` strings match the workflow engine and UI.
* [ ] `applies_to` matches the release that ships the steps.
* [ ] Cross-links to [](/explore-analyze/workflows/steps/action-steps.md) and [](/explore-analyze/workflows/steps/kibana.md) are in place.
* [ ] Limitations (disabled steps, solution-only owners) are explicit.

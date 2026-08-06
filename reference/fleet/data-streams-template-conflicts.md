---
navigation_title: Resolve overlapping index templates
description: Resolve overlapping index templates when you enable namespace index templates for a Fleet integration.
applies_to:
  stack: ga 9.5+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Resolve overlapping index templates for namespace customization [data-streams-template-conflicts]

Learn how to interpret and resolve warnings about overlapping index templates when you enable [namespace index templates](/reference/fleet/data-streams-namespace-custom.md) for a {{fleet}} integration. This page helps you decide whether to keep your existing customizations, switch to {{fleet}}-managed namespace index templates, or combine both approaches.

## When overlapping templates appear [data-streams-template-conflicts-when]

If you previously duplicated an integration's base data stream index template (priority `200`), narrowed the index pattern to one namespace, and raised the copy's priority (often to `250` or higher), that copy can overlap with a {{fleet}}-managed namespace index template. For example, you might have copied `logs-nginx.error` into `logs-nginx.error-production-custom` with pattern `logs-nginx.error-production*` and priority `280`.

When you enable namespace index templates for that same namespace, {{fleet}} tries to create a managed template such as `logs-nginx.error@namespace.production` at priority `250` for the same index pattern. {{es}} applies only one winning index template per index creation, so those templates overlap. The result depends on the existing template's priority, as described in [How {{fleet}} detects and reports overlaps](#data-streams-template-conflicts-detect).

The same can happen with any pre-existing index template whose index patterns match the namespace's data streams, not only copies with a custom suffix in the name.

## How {{fleet}} detects and reports overlaps [data-streams-template-conflicts-detect]

When you enable namespace index templates for a namespace on an integration, {{fleet}} runs a preflight check for each `(data stream, namespace)` pair. The check uses the {{es}} simulate index API (`POST _index_template/_simulate_index/<index>`) to see which existing template would win for that data stream, then compares priorities with the planned namespace index template.

::::{note}
{{fleet}} sets the namespace index template priority to the base template priority plus 50: `250` for most integrations (base `200`), or `200` for integrations with `dataset_is_prefix: true` data streams (base `150`). The examples on this page use `250`; if your integration uses `dataset_is_prefix` data streams, read `200` instead. A user with the `manage_index_templates` privilege can change this priority with the {{es}} index template API, but {{fleet}} restores the default whenever the integration's templates are reinstalled or resynchronized.
::::

{{fleet}} reports overlaps in the UI before changes are applied, and in API responses as warnings. Each overlap falls into one of these cases:

| Situation | What happens |
| --- | --- |
| Existing template priority is higher than `250` | {{fleet}} creates the namespace index template, but {{es}} applies the existing template for new data streams. The namespace index template's `composed_of` chain (including `<namespace>@custom`) is not used. |
| Existing template priority is exactly `250` | {{fleet}} cannot create the namespace index template. The existing template continues to govern new data streams for that pair until you change priorities and enable namespace index templates again. |
| Existing template priority is lower than `250` | {{fleet}} creates the namespace index template, and {{es}} applies it for new data streams. The existing template no longer affects newly created indices in that namespace. |

::::{note}
Index templates are applied when backing indices are created. Existing indices are not rewritten when you enable or turn off namespace index templates.
::::

{{es}} does not merge overlapping index templates. The highest-priority matching template wins as a whole. Component templates are merged only within that winning template's `composed_of` list.

## Choose a resolution path [data-streams-template-conflicts-resolve]

Pick the path that matches your goal.

### Use {{fleet}}-managed namespace index templates [data-streams-template-conflicts-use-fleet]

Use this path when you want `<namespace>@custom` and related {{fleet}} namespace features to apply.

1. Identify overlapping templates in **Index Management** → **Index Templates**. Look for templates whose index patterns match the same data streams as the planned `@namespace.<namespace>` templates.
2. If any overlapping template has priority `250`, lower that priority (for example to `200` or less) or remove the template before enabling. Same-priority templates block creation of the {{fleet}}-managed namespace index template.

   ::::{include} _snippets/change-index-template-priority.md
   ::::
3. Enable namespace index templates for the namespace. For UI and API steps, refer to [Customize data streams with namespace index templates](/reference/fleet/data-streams-namespace-custom.md).
4. Confirm the managed templates exist (for example, search index templates for `@namespace.<namespace>`).
5. Create or update the `<namespace>@custom` component template with the settings you still need. Copy useful settings from your older custom index templates into `<namespace>@custom` or into the data stream `@custom` templates when they should stay data-stream-specific.
6. Optionally delete or further lower the priority of unused custom index templates that no longer win, if you don't need them as a fallback.
7. Roll over each affected data stream so new backing indices use the managed templates.

::::{tip}
If you enabled namespace index templates while a priority-`250` overlap blocked some templates, turn them off for that namespace, adjust those priorities, then enable them again so {{fleet}} can create the missing namespace index templates.
::::

### Keep your existing custom index templates [data-streams-template-conflicts-keep-custom]

Use this path when your custom index templates already do what you need.

1. Cancel enabling if the warning appears in the UI, or leave the namespace out of **Namespaces with dedicated index templates**.
2. If you already enabled namespace index templates for the namespace, remove it from **Namespaces with dedicated index templates** on the integration's **Settings** tab, or turn off **Use dedicated index templates for this namespace** in the integration policy editor. {{fleet}} deletes the managed namespace index templates; your existing templates remain.
3. Continue managing customization through your existing index templates and component templates.

### Combine both approaches [data-streams-template-conflicts-mixed]

Use this path only when you understand which template should win for each data stream.

1. Review every overlapping template's priority against the namespace index template priority (`250` for most integrations; refer to the preceding note).
2. For data streams where your custom template must win, set its priority higher than the namespace index template priority. For data streams where the {{fleet}}-managed namespace index template must win, set your custom template's priority lower (but not equal, which blocks creation), or remove the template.

   ::::{include} _snippets/change-index-template-priority.md
   ::::
3. Enable namespace index templates and read the warning list to confirm the expected winners.
4. Verify a sample of new backing indices (settings, mappings, and lifecycle) after rollover.

Leaving overlapping templates at priority `250` or higher means some or all namespace index template customization might be unused or incomplete, even after you enable the feature.

## Related pages [data-streams-template-conflicts-related]

* [Customize data streams with namespace index templates](/reference/fleet/data-streams-namespace-custom.md)
* [Edit the {{es}} index template](/reference/fleet/data-streams.md#data-streams-index-templates-edit)
* [Best practices for copying an integration index template](/reference/fleet/integrations-assets-best-practices.md#assets-restrictions-cloning-index-template)
* [Tutorials: Customize data retention policies](/reference/fleet/data-streams-ilm-tutorial.md)

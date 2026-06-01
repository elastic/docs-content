---
navigation_title: Documentation strategies
description: "Editorial strategies for documenting Elastic features and procedures that vary by deployment type. Includes a strategy decision table, IA placement guidance, examples, and review symptoms."
---

# Documentation strategies for deployment-type variation

Use this page to choose an editorial approach when content varies by deployment type, and to spot common issues during review. For background on the deployment types and how they differ, refer to [](about.md).

## Strategies

When an action or activity differs depending on deployment type, there are three broad strategies:

- Create one doc per deployment type for the same activity.
- Make the doc valid for all deployment types (for example, with [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs).
- If the activity is part of a bigger guide, rely on a separate doc that explains the activity for all deployment types, and link to it.

The right choice depends on the activity, the scope of the surrounding doc, and how widely the steps differ across deployment types.

### Pick a strategy

| Use case | Approach | Example |
|---|---|---|
| Activity is atomic and required or performed in many other docs | Create a dedicated doc that covers the activity for all deployment types. Refer to that doc from other docs that need the activity. | Configure `elasticsearch.yml`; add a keystore or secure setting; put a file into the config directory |
| Longer process that differs more by deployment type | Evaluate the trade-off between fitting everything into a single document and creating multiple per-deployment-type documents. | Configure remote clusters (multiple docs); manage snapshot repositories (multiple docs); file-based user management (one doc for self-managed and ECK) |
| Guide exists but only for some deployment types | Evaluate whether the scope is intentional (meets a business need) or a gap. If a gap, expand the doc to cover other deployment types. If it must stay scoped, tell the user why and offer alternatives or escape hatches. | [](/manage-data/migrate.md), currently scoped to ECH and ECE |
| Pathway or process only exists for one or some deployment types | Break the content out into a labelable chunk: a bullet, a callout, or a section. Indicate applicability with [`applies_to`](/contribute-docs/how-to/cumulative-docs/index.md) tags. | An {{es}} command-line utility for cron expression validation, only available on self-managed |

### Where new content lives in the IA

Some parts of the docs IA are organized by deployment type (for example, [](/deploy-manage/deploy.md) has separate sections for self-managed, ECK, ECE, ECH, and {{serverless-short}}). Other sections are organized by concept and apply across deployment types.

| Section type | Belongs here |
|---|---|
| Deployment-specific | First-mile setup, architecture and value proposition for that deployment type, concepts unique to that deployment's structure (for example, config file location), and wayfinding to shared concepts |
| Shared (concept-based) | Cross-deployment primitives extended by deployment-specific modes, config or admin tasks users return to repeatedly or that happen after hello-world, and feature usage regardless of deployment type |

## Examples

### Access {{kib}}

If we include all deployment-type instructions in every doc that asks the reader to open {{kib}}, the docs feel repetitive and become longer than they need to be without any benefit to the reader.

Instead, create a single generic doc that explains how to open {{kib}} across all deployment types, and link to it. Users who already know how to access {{kib}} can skip the link.

### Stack monitoring

[](/deploy-manage/monitor/stack-monitoring.md) is a core {{es}} concept, but Elastic provides helpful shortcuts and utilities to set it up in ECH, ECK, and ECE.

The stack monitoring docs stay together as one narrative, but:

- Setup topics are separated by deployment type, because the processes vary widely in steps and complexity. ECH and ECE share a topic, because they use the same setup wizard.
- Metrics and data access topics are shared across deployment types. The processes differ slightly but fit neatly into a tabbed experience.
- Visualization and alerting configuration are shared topics that apply regardless of deployment type.

This keeps the full stack monitoring narrative in one place while providing a clear pathway for each deployment type.

## Things to watch for

Use this list when reviewing PRs or auditing existing pages.

- **Specific deployment types as a prerequisite.** A deployment-agnostic task that opens with "Create an {{ech}} deployment" scopes itself unnecessarily.
- **`applies_to` doesn't match the deployment types mentioned in prose.** Either the prose or the tag is wrong.
- **Shared procedures use a deployment-specific surface.** For example, a procedure that should work for ECK or self-managed opens with "use the {{ecloud}} Console."
- **Manually editing config files or dropping files in filesystem folders** without acknowledging that orchestrated deployment types don't expose those files the same way.
- **API calls for setup or config tasks** when some deployment types have better UI pathways for the same task.
- **Prerequisites don't match the page scope.** A page tagged for one set of deployment types or versions has prerequisites tagged for a different set. Either the prerequisite or the page-level `applies_to` is wrong.
- **Readers from other deployment types are stranded.** A page scoped to some deployment types offers no cross-reference or explanation for readers on the others. Link to the equivalent procedure or note why one doesn't exist.
- **Duplicated procedure where a cross-reference would do.** An atomic procedure (configure a setting, access {{kib}}, install an integration) is restated in multiple guides instead of being maintained in one place and linked to.
- **A missing feature on some deployment types is silently omitted.** A page covers a feature available on several deployment types but doesn't acknowledge that it's removed or replaced on others (most often {{serverless-short}}: {{ilm-init}}, {{watcher}}, custom plugins, audit logging). Note the absence and link to the closest alternative.
- **"Self-managed" used as a grouping label.** A page uses "self-managed" to mean ECK, ECE, and self-managed together. Use the specific deployment type instead.

## Resources

- [](/contribute-docs/how-to/cumulative-docs/guidelines.md): how `applies_to` tagging works
- [](/contribute-docs/how-to/cumulative-docs/example-scenarios.md): example tagging patterns for various deployment-type variations

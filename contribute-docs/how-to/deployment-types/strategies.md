---
navigation_title: Documentation strategies
description: "Editorial strategies for documenting Elastic features and procedures that vary by deployment type. Includes a strategy decision table, IA placement guidance, examples, and review symptoms."
---

# Strategies for documenting across deployment types

Use this page to choose an editorial approach when content varies by deployment type, and to spot common issues when reviewing your own or others' work. For background on the deployment types and how they differ, refer to [](about.md).

## Strategies

When an action or activity differs depending on deployment type, the right approach depends on the activity, the scope of the surrounding doc, and how widely the steps differ across deployment types.

| Use case | Approach | Example |
|---|---|---|
| Activity is atomic and required or performed in many other docs | Create a dedicated doc that covers the activity for all deployment types. Refer to that doc from other docs that need the activity. | • [](/deploy-manage/stack-settings.md)<br>• [](/deploy-manage/security/secure-settings.md) |
| Longer process that differs more by deployment type | Evaluate the trade-off between fitting everything into a single document and creating one document for each deployment type. Tools like [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs can help keep variation in one doc. See [Patterns by how a capability differs across deployment types](#patterns-by-how-a-capability-differs-across-deployment-types) for guidance. | • [](/deploy-manage/remote-clusters.md)<br>• [](/deploy-manage/tools/snapshot-and-restore.md) |
| Guide exists but only for some deployment types | Evaluate whether the scope is intentional (meets a business need) or a gap. If a gap, expand the doc to cover other deployment types. If it must stay scoped, tell the user why and offer alternatives or escape hatches. | [](/manage-data/migrate.md), currently scoped to ECH and ECE |
| Pathway or process only exists for one or some deployment types | Break the content into elements you can label: bullets, callouts, or sections. Indicate applicability with [`applies_to`](/contribute-docs/how-to/cumulative-docs/index.md) tags. | [`elasticsearch-croneval`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-croneval.md), an {{es}} CLI utility for cron expression validation, only available on self-managed |

### Patterns by how a capability differs across deployment types

You have a lot of flexibility when deciding how to shape content that varies by deployment type. However, if you're not sure what to do, here are some patterns to help you decide.

| Relationship | Content shape | `applies_to` pattern |
|---|---|---|
| **Identical primitive and config.** Same behavior, same config surface. | One page, no deployment-specific content. | Page-level `applies_to: stack`. |
| **Same primitive, different config surface.** For example, set the same setting in `elasticsearch.yml` vs. a {{k8s}} CRD vs. the {{ecloud}} UI. | One central page: shared concept, then forked steps. | Page-level `applies_to` listing the deployment types that apply. [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs for the forked steps. |
| **Augmented (minor).** Platform adds a convenience on top of the base primitive. | One page: base capability, then a scoped section for what the platform adds. | Page-level `applies_to` covers all types. Section-level or admonition `applies_to` on the scoped section. |
| **Augmented (significant).** Platform adds a layer that changes the user's mental model or workflow (for example, Cloud SSO wrapping {{es}} auth). | Shared overview that covers the concept and orients users, then forked content. The base capability and the platform-added behavior each need room. | Page-level `applies_to` on the overview. [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs if the workflows are parallel; sibling pages if the platform-specific workflow would overwhelm the base. |
| **Constrained by platform.** Same primitive, restricted on some types. | One page: full capability, with restrictions called out where relevant. | Page-level `applies_to` covers all types where the feature exists. Inline `applies_to` or admonitions to flag constraints. Use `unavailable` sparingly and [per guidelines](/contribute-docs/how-to/cumulative-docs/guidelines.md#when-to-indicate-something-is-not-applicable) for blocked sub-features. |
| **Replaced by a different mechanism.** Same user goal, different mechanism (most often {{serverless-short}}). | Shared overview of the user goal, then forked content for each mechanism. | Page-level `applies_to` on the overview. [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs if mechanisms are parallel; sibling pages if they're too different to coexist. |
| **Removed or not available.** Capability missing on some deployment types. | Don't just omit. Signal the absence where users are likely to look. | Don't add the missing type to page-level `applies_to`. Use section-level or inline `serverless: unavailable` where confusion is likely. Use the `removed` lifecycle value for version-specific removals. |

## Examples

The following are real-world examples of how we address varying processes across deployment types.

:::{dropdown} Access {{kib}}
If we include all deployment-type instructions in every doc that asks the reader to open {{kib}}, the docs feel repetitive and become longer than they need to be without any benefit to the reader.

Instead, create a single generic doc that explains how to open {{kib}} across all deployment types, and link to it. Users who already know how to access {{kib}} can skip the link.
:::

:::{dropdown} Stack monitoring
[](/deploy-manage/monitor/stack-monitoring.md) is a core {{es}} concept, but Elastic provides helpful shortcuts and utilities to set it up in ECH, ECK, and ECE.

The stack monitoring docs stay together as one narrative, but:

- Setup topics are separated by deployment type, because the processes vary widely in steps and complexity. ECH and ECE share a topic, because they use the same setup wizard.
- Metrics and data access topics are shared across deployment types. The processes differ slightly but fit neatly into a tabbed experience.
- Visualization and alerting configuration are shared topics that apply regardless of deployment type.

This keeps the full stack monitoring narrative in one place while providing a clear pathway for each deployment type.
:::

## Things to watch for

Use this checklist when reviewing PRs or auditing existing pages. These are common issues that we encounter when trying to document across deployment types.

- [ ] **Specific deployment types as a prerequisite.** A deployment-agnostic task includes "Create an {{ech}} deployment" as a prerequisite.
- [ ] **`applies_to` doesn't match the deployment types mentioned in prose.** For example, the page label is `stack` but the opening sentence says "In ECE and ECH, ..."
- [ ] **Shared procedures use a deployment-specific surface.** A procedure that should work for ECK or self-managed opens with "use the {{ecloud}} Console."
- [ ] **Manually editing config files or dropping files in filesystem folders** without acknowledging that orchestrated deployment types don't expose those files the same way. Link to a central doc that covers the task across deployment types, fork the procedure, or add a note.
- [ ] **API calls for setup or config tasks** when some deployment types have better UI pathways for the same task. Unless it is much more contextually appropriate to use the API, link to a central doc that covers the task in additional surfaces, fork the procedure, or add a note.
- [ ] **Prerequisites don't match the page scope.** A page tagged for one set of deployment types or versions has prerequisites tagged for a different set (not the same as [dimensions](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions)).
- [ ] **Readers from other deployment types are stranded.** A page scoped to one or more deployment types (but not all) offers no cross-reference or explanation for readers using other deployment types. Link to the equivalent procedure or note why one doesn't exist.
- [ ] **A duplicated procedure where a cross-reference would do.** An atomic procedure (configure a setting, access {{kib}}, install an integration) is restated in multiple guides instead of being maintained in one place and linked to, or a procedure documented elsewhere is restated on a page without a snippet.
- [ ] **A missing feature on some deployment types is silently omitted.** A page covers a feature available on several deployment types but doesn't acknowledge that it's removed or replaced on others (most often {{serverless-short}}: for example, {{ilm-init}}, {{watcher}}, custom plugins, audit logging). Note the absence and link to the closest alternative.
- [ ] **"Self-managed" used as a grouping label.** The term "self-managed" is sometimes used as a catch-all for anything not hosted on {{ecloud}}, including ECK and ECE. ECK, ECE, and self-managed are distinct deployment types with meaningful differences, and tying them together obscures those distinctions. Always refer to each deployment type by name.

:::{admonition} Use an incremental, iterative approach
Sometimes, there's not enough time to rework a tutorial to make it deployment-agnostic. Acknowledging the limitation and providing a way forward is a good first step. Open an issue to track a longer-term fix.
:::

## Resources

- [](/contribute-docs/how-to/cumulative-docs/guidelines.md): how `applies_to` tagging works
- [](/contribute-docs/how-to/cumulative-docs/example-scenarios.md): example tagging patterns for various deployment-type variations

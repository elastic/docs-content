---
navigation_title: Strategies
description: "Editorial strategies for documenting Elastic features and procedures that vary by deployment type. Includes a decision table for choosing an approach, IA placement rules, and named patterns from existing docs."
---

# Strategies for deployment-type variation

Once you've [classified content by deployment-sensitivity](index.md#classify-content-by-deployment-sensitivity), use this page to pick an editorial strategy.

The goal is to avoid two opposite mistakes:

- **Over-scoping** — taking a deployment-agnostic concept and writing it as if it only applies to one type
- **Hiding variation** — squeezing genuinely different steps into one procedure that doesn't quite work for anyone

## Pick a strategy

| Use case | Approach | Examples |
|---|---|---|
| **Activity is atomic and reused in many other docs** | Create a single dedicated doc that covers all deployment types, and link to it from anywhere that needs it. Don't repeat the steps in every guide. | [Stack settings](/deploy-manage/stack-settings.md), [Secure your settings](/deploy-manage/security/secure-settings.md), authentication realms (SAML), remote cluster setup for CCS or CCR |
| **Longer process, differs more by deployment type** | Evaluate the trade-off between one combined document (using [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) or tabs) versus multiple per-deployment documents. Combined is better when the workflow stays parallel; multiple is better when paths diverge significantly. | Remote clusters, snapshot repository management, file-based user management, OTel quickstarts, stack monitoring setup |
| **Guide exists but only for some deployment types** | Decide if that scope is intentional (meets a real business need) or a gap from incomplete migration. If a gap, expand the doc to cover other deployment types. If it must stay scoped, tell the user why and link to alternatives or escape hatches. | [Migrate your Elasticsearch data](/manage-data/migrate.md) — currently scoped to ECH and ECE |
| **Pathway or process only exists for one or some deployment types** | Break the deployment-specific content out into a labelable chunk: a bullet, a callout, or a section. Then indicate applicability with [`applies_to`](/contribute-docs/how-to/cumulative-docs/index.md) tags. | An Elasticsearch CLI utility that only exists on self-managed deployments |

For tagging syntax and patterns, refer to [Cumulative docs example scenarios](/contribute-docs/how-to/cumulative-docs/example-scenarios.md).

## Common difference patterns

A feature can differ across deployment types in more than one way. This table summarizes the patterns we see most often, with examples from existing docs. None of these are rules — they're starting points to recognize what's going on before you choose a strategy.

| Difference | Examples | Common approach |
|---|---|---|
| **Identical across deployment types** | Query DSL, mappings, ingest pipelines, [custom roles](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md), [{{ilm-init}}](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md) where available | Single page tagged at the `stack` level. No per-deployment forking, no section tags. |
| **Same capability, different config surface** | `elasticsearch.yml`, a Kubernetes CRD, a Cloud UI editor, or a project setting all configuring the same thing | Single page with [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs per surface. See [Stack settings](/deploy-manage/stack-settings.md), [Secure your settings](/deploy-manage/security/secure-settings.md). |
| **Augmented by the platform (minor)** | ECH and ECE add Cloud SSO on top of native {{es}} authentication realms | Single page, with a scoped section or admonition for the addition. The base content stays shared. |
| **Augmented by the platform (significant)** | ECH and ECE's managed snapshot lifecycle on top of native {{es}} snapshots; orchestrator-driven autoscaling | Shared overview + sibling pages per type. See [snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md), with dedicated pages for [ECH](/deploy-manage/tools/snapshot-and-restore/elastic-cloud-hosted.md), [ECE](/deploy-manage/tools/snapshot-and-restore/cloud-enterprise.md), [ECK](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md), and [self-managed](/deploy-manage/tools/snapshot-and-restore/self-managed.md). |
| **Constrained on some deployment types** | ECH and ECE block file and PKI auth realms; ECK reserves operator-managed settings; {{serverless-short}} blocks JVM access | Single page. Flag constraints inline or in admonitions at the point they're relevant, rather than rewriting the page. |
| **Replaced by a different mechanism** | {{serverless-short}} replaces {{es}} security realms with Cloud org-level authentication; replaces {{es}} custom roles with project-scoped role assignments | Shared overview that orients the user, plus sibling pages for each mechanism. Tabs tend to bury one side or the other. |
| **Removed or unavailable** | No {{ilm-init}}, {{watcher}}, custom plugins, or audit logging on {{serverless-short}}; no JVM customization | Leave the removed type off the page-level `applies_to`. Use section-level or inline `applies_to` (for example, `serverless: unavailable`) at the point users would look. For version-specific removals, use the `removed` lifecycle. |

## Two principles that cut across all strategies

**Extract atomic actions once.** Setup steps like configuring a setting, adding a keystore entry, or accessing Kibana appear in dozens of guides. Write the procedure once with all deployment types covered, and link to it from each higher-level guide. Don't restate the procedure in every doc.

**Scope honestly.** If a guide truly only works for some deployment types, say so explicitly. Don't pretend a procedure is universal when it isn't, and don't leave readers from other deployment types without an alternative or a pointer to one.

---

## Where deployment-specific content belongs in the IA

Some sections of the docs are organized by deployment type — for example, the [Deploy](/deploy-manage/deploy.md) section has separate areas for self-managed, ECK, ECE, ECH, and Serverless. Other sections are organized by concept and apply across deployment types.

**As a rule: first-mile content is deployment-specific. Everything reusable is shared.**

### What belongs in a deployment-specific section

- **Lay of the land** — architecture and value proposition for that deployment type
- **Structural concepts unique to the deployment type** — config file location, CRD layout, project settings UI
- **First mile** — how to stand up the orchestrator and the deployment
- **Wayfinding** — pointers from first-mile content into shared docs for next steps

### What belongs in a shared section

- A feature exists everywhere but is **configured differently** per deployment type (for example, authentication realms, snapshots)
- Config and admin tasks that users **return to repeatedly** or that happen **after hello-world**
- **Feature usage**, regardless of deployment type

When a feature has both shared usage and deployment-specific configuration, the page typically lives in a shared section, with deployment-specific configuration broken out using [`applies_to`](/contribute-docs/how-to/cumulative-docs/index.md) tags or [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) tabs.

---

## Named patterns

These patterns recur often enough that it's useful to recognize them by name.

| Pattern | When to use it |
|---|---|
| Access Kibana | A doc needs the user to "open Kibana" but isn't specifically about Kibana access |
| Stack monitoring (split setup / shared body / shared visualization) | A topic has both shared concepts and deployment-specific setup |
| Migrate-style scoped guide | A guide genuinely only applies to a subset of deployment types |
| Signal absence | A feature isn't available on some deployment types and users from those types might still look for it |

### Access Kibana

If a doc needs the user to "open Kibana," there are two acceptable approaches:

- Link to a single generic doc that covers Kibana access across all deployment types, so users who know how to access Kibana can skip the click
- Assume the user knows how to access Kibana (appropriate for advanced tasks)

Never reproduce deployment-type-specific Kibana access instructions in a doc that's about something else. It bloats the doc and scopes it to whichever deployment type happens to be illustrated.

### Stack monitoring (split setup / shared body / shared visualization)

The stack monitoring documentation is a useful reference pattern when a topic has both shared concepts and deployment-specific setup:

- **Separate setup topics by deployment type** — these processes vary widely in steps and complexity. ECH and ECE share a topic because they use the same setup wizard.
- **Shared metrics and data access topics** — these differ between deployment types but fit neatly into a tabbed experience.
- **Shared visualization and alerting topics** — these apply regardless of deployment type.

This keeps the whole stack monitoring narrative in one place while providing a clear pathway for each deployment type.

### Migrate-style scoped guide

When a guide genuinely only applies to a subset of deployment types (often because it's still work-in-progress), use a note at the top of the page to explain the scope and offer escape hatches for readers outside the scope. The [Migrate your Elasticsearch data](/manage-data/migrate.md) page is an example: the page is scoped to ECH and ECE, with a note explaining that the same approach can be adapted for other deployment types.

### Signal absence

When a feature isn't available on some deployment types — especially when users coming from another deployment type might look for it — don't silently omit it. Briefly note that it isn't available and link to the closest alternative if there is one. This applies most often to Serverless, which removes or replaces features like {{ilm-init}}, Watcher, custom plugins, audit logging, and JVM customization.

---

## See also

- [Documenting deployment types](index.md) — primer and classification
- [Review checklist](review-checklist.md) — what to look for in PRs
- [Cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/guidelines.md) — how `applies_to` works
- [Cumulative docs example scenarios](/contribute-docs/how-to/cumulative-docs/example-scenarios.md) — tagging patterns

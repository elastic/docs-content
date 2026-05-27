---
navigation_title: Review checklist
description: "Checklist for reviewing Elastic documentation that touches multiple deployment types. Covers common symptoms of over-scoping, mismatched applies_to tags, and surface-specific content that should be generalized or split."
---

# Review checklist

Use this checklist when reviewing PRs, auditing existing docs, or assessing content from other teams. Each item describes a symptom, why it matters, and what to do about it.

These symptoms often co-occur. Fixing one often surfaces another.

## 1. Specific deployment type as a prerequisite

**Symptom:** A page or procedure for a deployment-agnostic task opens with "Create an {{ech}} deployment" (or similar) as a prerequisite.

**Why it matters:** It scopes the entire page to one deployment type even though the task itself works on all deployment types. Readers using ECK, ECE, self-managed, or Serverless think the page isn't for them.

**What to do:**

- Remove the deployment-specific prerequisite if the task truly applies to all deployment types
- Replace with a generic prerequisite (for example, "A running {{es}} cluster")
- If the task really only works on one deployment type, keep the prerequisite and ensure the page-level `applies_to` reflects that

## 2. `applies_to` doesn't match deployment types mentioned in prose

**Symptom:** The page-level `applies_to` says `stack` (all four versioned deployment types), but the prose only ever references ECH workflows. Or the frontmatter says `deployment: ess` but the page also describes ECE behavior in a section.

**Why it matters:** Badges and tags are how readers filter for content that applies to them. A mismatch undermines that signal and leaves readers either over-confident or wrongly excluded.

**What to do:**

- If the prose is correct, update the `applies_to`
- If the `applies_to` is correct, update the prose
- Use section or inline tags to mark exceptions when most of the page applies broadly but a section applies narrowly

For dimension choice, refer to [Cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/guidelines.md#dimensions).

## 3. Orchestrator surfaces mentioned in generic content

**Symptom:** A page about a Kibana feature, Elasticsearch API, or general concept opens by referencing the {{ecloud}} Console, the ECE Cloud UI, or project settings.

**Why it matters:** Naming an orchestrator surface in a deployment-agnostic page implicitly scopes the page to whichever deployment type owns that surface. The same task is reachable from every deployment type's surface; mentioning only one makes the others invisible.

**What to do:**

- Remove the surface mention if the content is genuinely cross-deployment
- Replace with a deployment-agnostic phrasing (for example, "Open Kibana" — and link to a single doc that explains how to open Kibana across deployment types)
- If the page really is deployment-specific, fix the `applies_to` rather than the prose

Refer to [Signals](signals.md) for the full list of telltale surface mentions.

## 4. Manual file edits or filesystem paths

**Symptom:** Steps tell the user to edit `elasticsearch.yml`, drop a file into a config directory, or change a value on disk — without acknowledging that orchestrated deployment types don't expose these files the same way.

**Why it matters:** Self-managed users edit files directly. ECK users patch CRDs and mount volumes. ECH and ECE users apply user settings through the UI or API. Serverless users often can't change the setting at all. A procedure that assumes one mechanism leaves four other audiences stuck.

**What to do:**

- If the content applies to all deployment types, use [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) to show each mechanism, or link to a shared atomic doc like [stack settings](/deploy-manage/stack-settings.md)
- If the content is genuinely self-managed only (for example, a CLI utility that isn't available elsewhere), make that scope explicit with `applies_to`

## 5. API calls for setup tasks that have better UI pathways

**Symptom:** A setup or configuration procedure uses raw Elasticsearch API calls when orchestrated deployment types provide safer UI-based pathways for the same task.

**Why it matters:** {{ech}} and {{ece}} don't block unsafe setting changes made through the cluster settings API, even when the orchestrator UI would prevent the same change. Documenting only the API path encourages risky behavior on orchestrated deployments and ignores the supported pathway.

**What to do:**

- For procedures that have a UI pathway on orchestrated deployments, document both — with the UI pathway as the default for those deployment types
- Use [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) to separate API-based and UI-based procedures
- Add a warning when the API path is unsafe outside of self-managed and ECK

## 6. Prerequisites don't match the page scope

**Symptom:** A page tagged for one deployment type or version has prerequisites that specify a different scope — for example, a page tagged `deployment: eck` opens with a prerequisite that says "{{stack}} 9.4 or later."

**Why it matters:** Prerequisites have their own applicability. When the prerequisite scope is narrower than the page scope, readers within the page's audience might not actually be able to follow the procedure. When it's broader, the page is probably mis-scoped.

**What to do:**

- Verify the prerequisite is accurate for every deployment type and version the page claims to cover
- If the prerequisite is genuinely narrower, narrow the page-level `applies_to` to match — or scope the prerequisite with inline `applies_to`
- If the prerequisite is broader, broaden the page-level `applies_to` to match

## 7. Readers from other deployment types are stranded

**Symptom:** A page is scoped to some deployment types (for example, ECH and ECE) but offers no pathway for readers on the others. No cross-reference to the equivalent procedure, and no note explaining why an equivalent doesn't exist.

**Why it matters:** Readers arriving from search or external links don't always know the page is scoped. Without a wayfinding link or a note, they can't tell whether the procedure doesn't apply to them, hasn't been documented yet, or they're missing something.

**What to do:**

- Link to the equivalent procedure for other deployment types if one exists
- Add a note explaining why an equivalent doesn't exist, and link to the closest alternative or escape hatch
- For an example, refer to the scope note at the top of [Migrate your Elasticsearch data](/manage-data/migrate.md)

## 8. Duplicated procedure where a cross-reference would do

**Symptom:** The same procedure — configure a setting, add a keystore entry, access Kibana, install an integration — is restated in multiple guides instead of being maintained in one place and linked to.

**Why it matters:** Duplicated procedures drift. One copy gets updated with new deployment-type coverage; the others stay stale. Readers following an older copy hit steps that no longer work for their deployment type.

**What to do:**

- Find or create a single source of truth that covers all applicable deployment types (for example, [stack settings](/deploy-manage/stack-settings.md) for setting changes)
- Replace the duplicate with a cross-reference
- Refer to [Strategies for deployment-type variation](strategies.md#pick-a-strategy) for when this pattern applies

## 9. A missing feature on some deployment types is silently omitted

**Symptom:** A page covers a feature that exists for several deployment types but doesn't acknowledge that the feature is removed or replaced on others — most often {{serverless-short}} ({{ilm-init}}, {{watcher}}, custom plugins, audit logging).

**Why it matters:** Readers arriving from another deployment type expect to find the feature where they normally look for it. Silence reads as either "this applies to me too" or "you missed something."

**What to do:**

- Leave the removed type off the page-level `applies_to`
- Use a section-level or inline `applies_to` (for example, `serverless: unavailable`) at the point where users would look for the feature
- Link to the closest alternative if one exists
- For version-specific removals, use the `removed` lifecycle

---

## See also

- [Documenting deployment types](index.md) — primer and classification
- [Signals: how to recognize deployment context](signals.md) — symptom diagnosis
- [Strategies for deployment-type variation](strategies.md) — what to do once you've spotted an issue
- [Cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/guidelines.md) — `applies_to` tagging rules

---
navigation_title: Signals
description: "Telltale signs that documentation, screenshots, or support content is about a specific Elastic deployment type. Use during reviews to spot deployment-specific content that should be tagged or restructured."
---

# Signals: how to recognize deployment context

When you're reviewing a doc, looking at a screenshot, reading a ticket, or auditing search results, you often need to know *which deployment type the content is about* without anyone telling you explicitly.

This page collects the cues that signal a piece of content is rooted in a specific deployment type. Use them to:

- Spot when an `applies_to` tag is missing or wrong
- Catch content that's quietly scoped to one deployment type without saying so
- Quickly orient yourself in unfamiliar areas of the docs

## Quick-reference table

| Signal | Self-managed | ECK | ECE | ECH | Serverless |
|---|---|---|---|---|---|
| **URL pattern in screenshots or links** | Direct host URL (for example, `https://localhost:5601`) | (none — Kubernetes service URL) | Customer-defined admin URL (for example, `admin.<host>`) | `cloud.elastic.co` | `cloud.elastic.co/projects` |
| **Terminology for the unit of work** | Cluster | Cluster (Kubernetes-native: Custom Resource) | Deployment | Deployment | Project |
| **UI or surface named** | None (config on disk) | Kubernetes CRDs and manifests | ECE Cloud UI | {{ecloud}} Console | Project settings |
| **Files or mechanisms mentioned** | `elasticsearch.yml`, `kibana.yml`, keystore | Kubernetes volumes, secrets, init containers | Bundles, user settings, plugins | User settings, bundles, plugins | (no user-accessible config files) |
| **Features mentioned** | All Elasticsearch APIs, ILM, plugins | All + operator-managed features | Same as ECH | All except some ECE-only restrictions; supports plugins, bundles, private links, agentless | Limited subset: no ILM, no plugins, no user-controlled snapshots, no BYOK |
| **Telltale phrase** | "edit the file," "SSH into the node" | "apply the manifest," "patch the CR" | "in the ECE Cloud UI," "as a platform admin" | "in {{ecloud}} Console" | "in your project," "in project settings" |

## How to use this in a review

When you encounter a doc or PR:

1. **Scan for signals** from the table above.
2. **Check whether the page-level `applies_to`** matches the signals you see.
3. **If there's a mismatch:**
   - If the page is about a deployment-agnostic concept that mentions one deployment's surface — flag the surface mention, not the page scope
   - If the page is genuinely scoped to a specific deployment but isn't tagged that way — fix the `applies_to`

For the full review checklist, refer to [Review checklist](review-checklist.md).

## Examples

| What you see | What it signals | What to do if the page should be cross-deployment |
|---|---|---|
| "Log in to {{ecloud}} Console and open Kibana" on a generic Kibana feature page | {{ech}} (orchestrator surface) | Replace with deployment-agnostic phrasing (for example, "Open {{kib}}") and link to a single generic "access {{kib}}" doc |
| "Edit `elasticsearch.yml` to set this value" on a setting-configuration page | Self-managed direct file access. Other deployment types use user settings (ECH, ECE), CRDs (ECK), or don't expose the setting (Serverless) | Use an `applies-switch` per surface, or link to [Stack settings](/deploy-manage/stack-settings.md) |
| A code block starting with `apiVersion: elasticsearch.k8s.elastic.co/v1` | ECK manifest | Either scope the surrounding content to ECK or clearly mark the code block as one of several deployment-specific approaches |

---

## See also

- [Documenting deployment types](index.md) — primer and content classification
- [Review checklist](review-checklist.md) — symptoms to look for during PR review
- [Strategies for deployment-type variation](strategies.md) — what to do when content varies

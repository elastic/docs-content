---
navigation_title: "Troubleshooting"
description: "Guidance for writing troubleshooting content that help users diagnose and resolve specific problems quickly and effectively."
applies_to:
  stack: 
  serverless: 
---

# Troubleshooting

This page provides guidelines for writing effective troubleshooting pages in the Elastic docs.

## Types of troubleshooting content

There are several subtypes of troubleshooting content:

* **A dedicated troubleshooting page** (preferred): Use for specific, well-defined problems. The problem appears in the page title. Includes required **Symptoms** and **Resolution** sections. Optimized for search and direct linking.

* **Generic "Troubleshooting" or "Common problems" index page**: Use to organize multiple related troubleshooting topics. The title is generic (for example, "Common problems with {{product.apm}}"). Contains anchor links to sections on the same page or links to dedicated troubleshooting pages. Consider breaking out individual problems into dedicated pages as content grows.

* **Troubleshooting section within a general documentation page**: Use sparingly for brief, contextual troubleshooting tied to a specific feature or quickstart. If content grows beyond a few bullet points, extract it into a dedicated troubleshooting page and link to it.

The rest of this guide focuses on dedicated troubleshooting pages. Generic index pages and troubleshooting sections within general docs have different structure requirements and may not include all elements described here.

## What is a troubleshooting page

Troubleshooting pages help users fix specific problems they encounter while using Elastic products. They are intentionally narrow in scope (one primary issue per page), problem-driven, and focused on unblocking users as quickly as possible. 

Use the troubleshooting content type when:

- Users encounter a specific, repeatable problem.
- The problem can be identified through common symptoms.
- There is a known resolution or recommended workaround.

A page that doesn't describe a specific problem isn't troubleshooting content.

Readers of troubleshooting content are typically blocked or frustrated and want a fast, reliable fix. They expect clear guidance and strong recommendations without requiring background information or deep explanations. Keep troubleshooting pages short and to the point. Optimize for quick resolution, not exhaustive coverage.

## Structure of a troubleshooting page

To help users quickly identify and resolve problems, troubleshooting pages use a consistent structure. A predictable format helps users confirm they're in the right place and move directly to the solution they need.

### Required elements

The following elements are required in troubleshooting pages:

1. A consistent **filename:** Succinctly describe the problem. 
   - For example: `no-data-in-kibana.md`, `traces-dropped.md`.
2. Appropriate **[frontmatter](https://elastic.github.io/docs-builder/syntax/frontmatter/):**
   - `applies_to:` [Tags](https://elastic.github.io/docs-builder/syntax/applies) for versioning/availability info per the [cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/index.md).
   - `description`: A brief summary of the page fit for search results and tooltips.
   - `product`: The relevant Elastic product(s) the page relates to.
3. A clear **title:** A brief description of the problem, written from the user's perspective.
   - For example: "EDOT Collector doesn't propagate client metadata", "No application-level telemetry visible in {{kib}}", or "Logs are missing after upgrading {{agent}}".
4. A **Symptoms** section: Describe what users can observe when the problem occurs.
   - Focus only on user-visible behavior.
   - Do not explain causes.
   - Use bullet points.
   - Include error messages, log output, or UI behavior when helpful:
     - If the problem manifests as a specific error message, include the exact error text (or common variations) in the symptoms. Error messages are often how users identify and search for troubleshooting content.
     - If the problem manifests as undesirable behavior without a specific error, clearly describe the observable symptoms (for example, "No data appears in {{kib}}" or "Service status shows as unhealthy").
5. A **Resolution** section: Provide clear, actionable steps to resolve the issue. Each step should move the reader closer to a working system or help rule out possible causes or assumptions.
   - Use numbered steps.
   - Be prescriptive and opinionated.
   - Include minimal configuration examples when relevant.
   - Assume the reader's situation matches the **Symptoms** section.
   - Avoid speculative or diagnostic language.

### Optional elements

Consider including the following when they add value:

- A **Best practices** section: Use this section to explain how users can avoid encountering this specific problem again. Focus on preventive measures, configuration choices, or deployment patterns that directly relate to preventing this issue. This is the appropriate place to recommend supported or preferred patterns related to the problem, clarify Elastic-specific guidance, call out known limitations or constraints, and set expectations about scale, load, or deployment environments.
- A **Resources** section: Provide links to supplementary documentation for readers who want deeper context. Resources must not be required to fix the issue. Prefer Elastic-owned documentation, but link to upstream or external docs when necessary.

## Best practices

When you create troubleshooting pages, follow these best practices:

- Describe one primary issue per page.
- Be explicit about supported and unsupported setups.
- Optimize for fast resolution, not exhaustive coverage.

Do not use troubleshooting for teaching users how to use a feature for the first time (use a tutorial), explaining how a system works (use an overview), listing configuration options or APIs (use reference documentation), or describing general best practices that aren't tied to resolving a specific problem or preventing it from happening again.

## Template

To get started writing your troubleshooting page, use [the template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/troubleshooting-template.md).

## Examples

Here are some examples of well-structured troubleshooting pages in the Elastic documentation:

- [No logs, metrics, or traces visible in {{kib}}](/troubleshoot/ingest/opentelemetry/no-data-in-kibana.md): Addresses a specific data visibility issue with clear symptoms and resolution steps.
- [EDOT Collector doesn't propagate client metadata](/troubleshoot/ingest/opentelemetry/edot-collector/metadata.md): Focuses on a specific configuration problem with symptoms and actionable resolution steps.
- [Troubleshoot common errors in {{es}}](/troubleshoot/elasticsearch/errors.md): An example of an error reference index page that organizes multiple error-based troubleshooting topics.
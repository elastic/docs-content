---
navigation_title: "Troubleshooting"
description: "Guidance for writing troubleshooting pages that help users diagnose and resolve specific problems quickly and effectively."
applies_to:
  stack: 
  serverless: 
---

# Troubleshooting

This page provides guidelines for writing effective troubleshooting pages in the Elastic docs.

## What is a troubleshooting page

Troubleshooting pages help users fix specific problems they encounter while using Elastic products. They are intentionally narrow in scope (one primary issue per page), problem-driven, and focused on unblocking users as quickly as possible. 

Use the troubleshooting content type when:

- Users encounter a specific, repeatable problem
- The problem can be identified through common symptoms
- There is a known resolution or recommended workaround

A page that doesn't describe a specific problem isn't troubleshooting content.

Readers of troubleshooting content are typically blocked or frustrated and want a fast, reliable fix. They expect clear guidance and strong recommendations without requiring background information or deep explanations.

## Best practices

When you create troubleshooting pages, follow these best practices:

- Describe one primary issue per page
- Be explicit about supported and unsupported setups
- Optimize for fast resolution, not exhaustive coverage

Do not use troubleshooting for teaching users how to use a feature for the first time (use a tutorial), explaining how a system works (use an overview), listing configuration options or APIs (use reference documentation), or describing general best practices.

## Structure of a troubleshooting page

To help users quickly identify and resolve problems, troubleshooting pages use a consistent structure. A predictable format helps users confirm they're in the right place and move directly to the solution they need.

### Required elements

The following elements are required in overview pages:

- A consistent **filename:** Succinctly describe the problem. 
  - For example: `no-data-in-kibana.md`, `traces-dropped.md`.
- Appropriate **[frontmatter](https://elastic.github.io/docs-builder/syntax/frontmatter/):**
  - `applies_to:` [Tags](https://elastic.github.io/docs-builder/syntax/applies) for versioning/availability info per the [cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/index.md)
  - `description`: A brief summary of the page fit for search results and tooltips
  - `product`: The relevant Elastic product(s) the page relates to
- A clear **title:** A brief description of the problem, written from the user’s perspective.
  - For example: "EDOT Collector doesn't propagate client metadata", "No application-level telemetry visible in {{kib}}", or "Logs are missing after upgrading {{agent}}"
- A **Symptoms** section: Describe what users can observe when the problem occurs.
  - Focus only on user-visible behavior
  - Do not explain causes
  - Use bullet points
  - Include error messages, log output, or UI behavior when helpful
-A **Resolution** section: Provide clear, actionable steps to resolve the issue. Each step should move the reader closer to a working system or help rule out possible causes or assumptions.
  - Use numbered steps
  - Be prescriptive and opinionated
  - Include minimal configuration examples when relevant
  - Assume the reader's situation matches the **Symptoms** section
  - Avoid speculative or diagnostic language

### Optional elements

Consider including the following when they add value:

- A **Best practices** section: Use this section to explain how users can avoid the issue in the future. This is the appropriate place to recommend supported or preferred patterns, clarify Elastic-specific guidance, call out known limitations or constraints, and set expectations about scale, load, or deployment environments.
- A **Resources** section: Provide links to supplementary documentation for readers who want deeper context. Resources must not be required to fix the issue. Prefer Elastic-owned documentation, but link to upstream or external docs when necessary.

## Template

To get started writing your troubleshooting page, use [the template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/troubleshooting-template.md).
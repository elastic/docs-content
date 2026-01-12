---
description: "Guidelines for writing useful and comprehensive overview pages in the Elastic documentation."
applies_to:
  stack:
  serverless:
---

# Overviews

This page provides guidelines for writing effective overview pages in the Elastic docs. This page and its associated template can be used by humans and LLMs to draft new overviews, or to evaluate existing pages.

Use this page to:

- Help you draft a new overview by copying and pasting the [template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/overview-template.md).
- Understand the structure and best practices for overviews before you write one.
- Evaluate existing overviews or drafts against the standards outlined here.

Whether you're a regular contributor or reviewing someone else's work, these guidelines help ensure consistency, completeness, and quality across the Elastic documentation.

## What is an overview

An overview provides conceptual information that helps users understand a feature, product, or concept. It answers two fundamental questions:

- **What is it?**
- **How does it work?**
- **How does it bring value?**

Readers of overview pages are typically in a learning state rather than a goal-oriented or problem-solving state. They are often first-time users who want to get up and running quickly. Having effective overview content builds trust and confidence in our products.

Overviews serve several purposes:

- Explain what something is and why it matters.
- Inform users how features and capabilities improve their workflows.
- Help users navigate to the right content for their needs.
- Clarify how components, features, or concepts relate to each other.
- Help users choose between options or understand trade-offs.

## Structure of an overview

To help users quickly understand a feature or concept, overviews use a consistent structure. A predictable format improves comprehension and makes the content easier to navigate.

### Required elements

Every overview must include the following elements:

1. A consistent **filename:** Use descriptive noun-based patterns. Common patterns include:
   - `[feature-name].md` (for example, `text-embedding.md`)
   - `[concept].md` (for example, `data-streams.md`)
   - `index.md` for section landing pages

2. Appropriate **[frontmatter](https://elastic.github.io/docs-builder/syntax/frontmatter/):**
   - `applies_to:` [Tags](https://elastic.github.io/docs-builder/syntax/applies) for versioning/availability info per the [cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/index.md)
   - `description`: A brief summary of the page fit for search results and tooltips
   - `product`: The relevant Elastic product(s) covered in the overview
% TODO once we have structured types     - The `type` field set to `overview`

3. A clear **title:** A concise, descriptive name for the feature or concept
   - For example, "Text embedding" or "Data streams"

4. An **introduction:** Explain what the feature or concept is and why it matters to users. This should:
   - Answer "What is it?" at a high level.
   - Establish the scope: what the overview covers and, optionally, what it doesn't.
   - Help readers quickly determine if they're in the right place.

5. **Core content sections:** The body of the overview explaining how it works, key concepts, components, or use cases. Structure these sections based on what users need to understand.

### Recommended sections

Include the following sections in most overview pages:

1. **Use cases or examples:** Concrete scenarios showing how the feature or concept applies in practice.
2. **How it works:** A section explaining the underlying mechanism, workflow, or architecture. Consider including a diagram.
3. **Next steps:** Suggestions for what users can do next, such as getting started guides or tutorials.
4. **Related pages:** Links to related documentation such as how-to guides, reference material, or other overviews.

### Optional elements

Consider including the following when they add value:

- **Background or context:** Historical context, industry context, or an explanation of why something was designed a certain way. This is especially useful for complex concepts with non-obvious design decisions.
- **[Diagrams](https://elastic.github.io/docs-builder/syntax/diagrams/):** Architecture diagrams, flowcharts, or other visual aids to illustrate concepts and relationships.
- **Comparison tables:** When helping users choose between options, use tables to compare features, trade-offs, or use cases.
- **[Tabs](https://elastic.github.io/docs-builder/syntax/tabs/):** When explaining variations (such as different deployment types or product tiers), use tabs to show the differences.
- **Key terminology:** Define important terms if they're central to understanding the concept.

## Best practices

When you create overview pages, follow these best practices:

- **Focus on a single concept:** Each overview should be dedicated to one concept, feature, or topic. If you find yourself explaining a second concept in depth, create a separate overview and link to it.
- **Lead with user value:** Start by explaining why the feature or concept matters to the user, not just what it does.
- **Use the inverted pyramid:** Begin with the most important information at a high level, then progressively add detail. This lets readers grasp the essentials quickly and dive deeper as needed.
- **Keep it conceptual:** Focus on explaining ideas, not on step-by-step instructions. Avoid instructional or reference content. Link to how-to guides and reference pages instead.
- **Answer the key questions:** Ensure your overview addresses the fundamental questions: What is it? Why does it matter? How does it work? When would I use it?
- **Use concrete examples:** Abstract concepts become clearer when illustrated with real-world scenarios or use cases.
- **Provide visual aids:** Diagrams, flowcharts, and architecture illustrations help users grasp complex relationships.
- **Avoid duplication:** Don't repeat detailed information that belongs in reference or how-to pages. Link to those pages instead.

## Template

To get started writing your overview page, use the [template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/overview-template.md).

## Examples

Here are some examples of well-structured overview pages in the Elastic documentation:

- [Data streams](/manage-data/data-store/data-streams.md)
- [{{ilm-cap}}](/manage-data/lifecycle/index-lifecycle-management.md)


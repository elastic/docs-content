---
navigation_title: "How-to guides"
---

# How to write how-to guides

This page provides guidelines for writing effective how-to guides in Elastic documentation. To learn about other content types, refer to [](index.md).

## What is a how-to guide?

A how-to guide contains a short set of instructions to be carried out, in sequence, to accomplish a specific task. You can think of it like a cooking recipe.

It has two essential components:

- A set of **requirements**
- A sequence of **steps** to follow

This focus on a self-contained task is what defines a how-to guide and sets it apart from longer procedural guides, such as quickstarts or tutorials.

% TODO: Add eventual snippet that disambiguates how-tos, tutorials, and quickstarts -->

## Key principles

There are a few key principles to keep in mind when drafting how-to guides:

- **Focus on the user's goal:** Structure content around what users want to accomplish, not what the tool can do.
- **Write recipes, not lessons:** Don't define concepts or explain why things work, unless required for the task at hand. Add useful context to a "Related pages" or "Learn more" section instead.
- **Keep it focused:** A how-to guide should be scoped to a single, well-defined task. As a rule of thumb, if you need more than 10 overall steps, consider breaking it into multiple how-to guides or use the tutorial format.
- **Show alternative approaches:** When multiple valid solutions exist, show the options users might choose. For example:
  - If the same step can be carried out in the UI or with an API, use [tabs](https://elastic.github.io/docs-builder/syntax/tabs/#tab-groups) to show both options.
  - If instructions differ per deployment type or version, use an [applies-switch](https://elastic.github.io/docs-builder/syntax/applies-switch/) to show the variations.
- **Skip edge cases:** Focus on the typical, primary use case, and avoid documenting rare or non-standard variations.
- **Test your steps:** Authors and reviewers should follow the instructions end to end, to catch errors, missing steps, and language issues.

## Structure of a how-to guide

How-to guides follow a consistent structure. The following sections outline the required, recommended, and optional elements.

### Required elements

The following elements are required in every how-to guide:

- A consistent **filename:** Use action verb patterns like `create-*.md`, `configure-*.md`, or `troubleshoot-*.md`.
  - For example: `run-elasticsearch-docker.md`
- Appropriate **[frontmatter](https://elastic.github.io/docs-builder/syntax/frontmatter/):**
  - `applies_to:` [Tags](https://elastic.github.io/docs-builder/syntax/applies) for versioning/availability info per the [cumulative docs guidelines](/contribute-docs/how-to/cumulative-docs/index.md)
  - `description`: A brief summary of the page fit for search results and tooltips
  - `product`: The relevant Elastic product(s) used in the how-to
% TODO once we have structured types  - The `type` field set to `how-to`
- A clear **title:** A precise description of the task using an action verb
  - For example, "How to run {{es}} in Docker"
- An **introduction:** A brief summary of what the guide accomplishes and what the user will achieve.
- A **Before you begin** section: List any special permissions or data/configuration needed. Assume basic feature access. You can also link to background knowledge or highlight known pitfalls.
- A set of **steps:** Numbered instructions that begin with imperative verb phrases. Keep each step focused on a single action.
  :::{tip}
  Use the [stepper component](https://elastic.github.io/docs-builder/syntax/stepper/) for longer how-tos or those with complex steps.
  :::

### Recommended sections

Include the following sections in most how-to guides:

- **Next steps:** Suggestions for what users can do next after completing the task.
- **Related pages:** Links to related documentation such as conceptual topics, reference material, or other how-to guides.

### Optional elements

Consider including the following when they add value:

- **[Code annotations](https://elastic.github.io/docs-builder/syntax/code/#code-callouts):** Annotate important lines within code blocks.
- **[Screenshots](https://elastic.github.io/docs-builder/syntax/images/#screenshots):** Add visual aids for UI tasks when context is hard to describe in words. Use screenshots sparingly as they're hard to maintain.
- **Success checkpoints:** Include confirmation steps that show users whether critical actions succeeded before moving on.
- **Error handling:** Mention common errors and how to resolve them.

## Template

You can use the [how-to template](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/how-to-template.md) to get started writing your how-to guide.

## Examples

Here are some examples of well-structured how-to guides in the Elastic documentation:

% TODO: Add links to 2-3 exemplary how-to guides in the docs


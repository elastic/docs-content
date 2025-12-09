---
navigation_title: "Content types"
description: "Overview of guidelines for choosing the appropriate content types in the Elastic documentation."
---

# Elastic Docs content types

This page provides an overview of the different content types used in the Elastic documentation and guidelines for choosing the appropriate type when creating new docs pages.

Content types ensure the Elastic Docs are structured, consistent, and easy for users to follow. When we use the right content type, we make it easier for users to find the information they need and efficiently complete tasks. 

To help you quickly get started, each content type includes its own guidelines, best practices, and templates.

Before you start drafting a new docs page, identify the appropriate content type for your page.
Use these guidelines as a framework, not a rulebook. You should adapt structure and syntax where necessary to best serve users, but you should rarely need to deviate from the best practices.

:::{tip}
Need help choosing a content type or structuring a new page? Reach out to the docs team using the `@elastic/docs` handle in GitHub or post in the [#docs](https://elastic.slack.com/archives/C0JF80CJZ) Slack channel.
:::

## Mixing different content types

Some documentation pages combine multiple content types.

Mixing different types is fine as long as each section is clearly delineated and serves a distinct purpose. For example, a page about configuring authentication might include:

1. A brief overview of authentication concepts (explanation)
2. Step-by-step instructions to set up authentication (how-to)
3. A reference table of authentication settings (reference)

This works because each section is clearly separated and serves a distinct purpose. You shouldn't embed the settings table in the middle of the instructions, or interrupt the steps with conceptual explanations. This would break the flow and make it hard to scan the page for specific information.

When mixing content types, ensure that the overall structure and flow remain clear and logical for users. Use headings and sections to delineate different content types as needed.

:::{note}
The exception to this rule is the tutorial content type, which weaves explanatory and background information throughout the step-by-step instructions. This is because tutorials are focused on teaching a broader concept or workflow, rather than completing a specific task as fast as possible.

A tutorial should always be a standalone page, meaning it should have only one content type: `tutorial`.

% TODO add this once we have structured types:

% the frontmatter should only specify `type: tutorial`.
:::

## Guidelines per content type

- [How-to](how-tos.md)
% - [Tutorial](tutorials.md)

## Templates per content type

Refer to [our templates](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/how-to-template.md) for each content type to get started quickly.

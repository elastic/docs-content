---
navigation_title: "Content types"
description: "Overview of guidelines for choosing the appropriate content types in the Elastic documentation."
applies_to:
  stack: 
  serverless: 
---

# Elastic Docs content types

Content types ensure the Elastic Docs are well-structured, consistent, and complete. When we use the right content type, we make it easier for users to find the information they need and efficiently complete tasks. 

To help you quickly get started, each content type includes its own guidelines, best practices, and templates.

Before you start drafting a new docs page, identify the appropriate content type for your page.
Use these guidelines as a framework, not a rulebook. You should adapt structure and syntax where necessary to best serve users, but you should rarely need to deviate from the best practices.

:::{tip}
Need help choosing a content type or structuring a new page? Reach out to the docs team using the `@elastic/docs` handle in GitHub or post in the [community docs channel](https://elasticstack.slack.com/archives/C09EUND5612). (Elasticians can also use the internal [#docs](https://elastic.slack.com/archives/C0JF80CJZ) Slack channel.)
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

- [How-to guides](how-tos.md)
- [Overviews](overviews.md)
- [Troubleshooting](troubleshooting.md)
% - [Tutorial](tutorials.md)

## Templates per content type

Refer to [our templates](https://github.com/elastic/docs-content/blob/main/contribute-docs/content-types/_snippets/templates/) for each content type to get started quickly.

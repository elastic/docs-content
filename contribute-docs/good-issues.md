---
navigation_title: How to create good docs issues
---

# How to create good docs issues

We’re eager to help you. The best way to get our help is by creating a documentation issue. The following guidelines explain how to create documentation issues that we can act upon with minimal effort from you.

## Before creating an issue

### Check for existing documentation 

We are constantly improving our docs search and navigation. Before opening an issue about a missing piece of content, try the docs search or the navigation.

### Make sure the issue is still relevant

If you are creating an issue based on an old support case or a long-standing problem, validate that it is still relevant. Has the product or documentation changed since the original report?

### Validate technical details

If your request requires technical review or input, try to validate the details before opening the issue. For external contributors, provide as much context as possible in the issue description. For internal contributors, consider discussing with developers first to prevent the issue from being blocked indefinitely.

## When creating an issue

### Write a clear and specific title

Titles help us identify and triage issues. The more specific they are, the better. If you’re creating an issue using the Report an issue link, edit the placeholder text.

| ✅ Do this | ❌ Don't do this |
| ----- | ----- |
| *Add a new section on air-gapped configuration* | *Update docs* |
| *Website Link in EDOT logs tutorial is broken* | *Website some-doc-url* |
| *Python code snippet is not valid in tutorial X* | *This docs is wrong1!1* |

### Formulate a clear request in the description

Descriptions help us understand what needs to be changed in the docs. If there’s a template, strive to follow it. A good description contains a **definition of done** that describes the change you’d like to see.

| ✅ Do this | ❌ Don't do this |
| ----- | ----- |
| *Update the installation methods table on the Elastic Agent page to include details on the new endpoint. Here is a sample config.* | *This doc must be improved.* |
| *Include a new table that outlines installation methods and upgradability for Elastic Agent.* | *There is no definition of done.* |
| *A customer had trouble with a recent Kafka change. Adding a note in the documentation would have helped them resolve their issue more quickly and prevented a support ticket.* | *There is no context nor a “why”.* |

### Provide relevant links and resources

When submitting requests or issues, include links to the impacted documentation pages and related tickets or discussions.

#### Link to impacted documentation pages

Include links to the relevant documentation pages that relate to your request or issue.

#### Link to related tickets and discussions

If your request relates to existing tickets or discussions, provide relevant links and context.

For external contributors, include links to any public discussions, GitHub issues, forum posts, or blog posts that provide relevant background.

For internal contributors, if your request stems from internal tickets or discussions, summarize the key points and mark any internal-only links clearly. If you need to provide sensitive context (such as UI copy for early-stage designs or billing changes), you can create an issue in the private repo, [elastic/docs-content-internal](https://github.com/elastic/docs-content-internal/issues/new/choose). Most issues should be opened in the public repo, [elastic/docs-content](https://github.com/elastic/docs-content/issues/new/choose).

:::{tip}
**For internal contributors:** You can link to public docs issues from internal support cases and private issues. This adds a link to the docs issue's GitHub timeline for users within the Elastic org.
:::

### Follow the issue templates

The issue templates are there to help you provide the right information. You can always add more context if you want or modify the structure to suit your needs.

### One Issue = One Single, Testable Problem

Ideally, each ticket must represent a single, isolated problem or feature, or a bundle of closely related items. **Do not combine multiple bugs or requests into one ticket.**

If your request is for a large project with many parts, reach out to the docs team to determine the scope and see how it’s best to chunk work.

## Closing issues

In general, we will ask for clarification if the issue has problems. **If our feedback is not addressed in a reasonable time, we might close the issue**. You can always reopen it after editing it.

## Examples of great docs issues

Here are some examples of excellent docs issues:

- [Document Elastic Agent Upgrade Fails on Windows with status 0xc0000142](https://github.com/elastic/ingest-docs/issues/1775)
- [Prebuilt rule customization, upgrade, and export/import workflows](https://github.com/elastic/security-docs/issues/5061)

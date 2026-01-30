---
description: "Guidelines for writing effective release notes content in changelog YAML files for Elastic products."
---

# Release notes

This page provides guidelines for writing useful and consistent release notes for Elastic products.
Use this content type and the associated schema to draft new release notes or to evaluate existing content.

Use this page to:

- Understand the purpose and structure of release notes.
  - Learn about the different types.
  - Determine when to include optional information such as impact and actions.
- Write clear, user-focused content.
- Evaluate existing release notes against the standards outlined here.

Whether you're summarizing your pull request in a changelog or reviewing someone else's work, these guidelines help ensure consistency, completeness, and quality across Elastic release notes.

## What are release notes

Release notes communicate the changes in a product release, including new features, enhancements, bug fixes, breaking changes, deprecations, and more.
They help users understand what changed, why it matters, and what they need to do about it.

Readers of release notes include:

- **Developers**: Need to understand version updates that can impact their code or integrations, including breaking changes, new endpoints, deprecations, and bug fixes.
- **Technical users** (System administrators, DevOps engineers, IT specialists):  Need to ensure updates are correctly applied and systems are properly maintained, considering configuration changes, security updates, and compatibility.
- **End users**: Want to know how updates affect them, especially in production environments, focusing on new features, enhancements, and bug fixes.
- **Support teams**: Need accurate information about issues and changes to effectively assist customers.

## Structure of release notes

Elastic release notes should be generated from changelog YAML files that follow a [common schema](https://github.com/elastic/docs-builder/blob/main/docs/contribute/_snippets/changelog-fields.md).
Each changelog file describes a single change and includes metadata such as the type of change, affected products, and user-facing descriptions.

:::{important}
The layout and formatting of release notes in the published documentation is handled automatically by Elastic Docs.
For technical details, refer to [Create and bundle changelogs](https://elastic.github.io/docs-builder/contribute/changelog/).

Focus on creating clear, accurate content in the changelogs rather than worrying about how it will appear in the final documentation.
:::

### Required elements

Every changelog must include the following elements:

1. **Products**: The Elastic products affected by the change. Where possible, include a target release version or date and the lifecycle (for example, preview, beta, or GA).
1. **Type**: The type of change. For guidance, go to [Choosing the right type](#changelog-types).
1. **Title**: A short, user-facing summary. In general, limit it to 80 characters. For examples, go to [Writing effective titles](#changelog-titles).

### Optional elements

Consider including the following elements when they add value:

- **Description**: Additional information about the change (maximum 600 characters). See [Writing effective descriptions](#changelog-descriptions) for guidance.
- **Areas**: The components, features, or product areas affected by the change (for example, "{{esql}}" or "{{ml-app}}").
- **PR** and **issues**: The numbers or URLs for the related pull request and issues.
- **Feature-id**: If you want to be able to track changelogs associated with a specific feature flag or filter them out of the documentation, add a unique identifier.

The following elements apply to specific types of changes:

- **Impact**: For breaking changes, deprecations, or known issues, describe how the user's environment is affected.
- **Action**: For breaking changes, deprecations, or known issues, describe what users must do to mitigate the change.
- **Subtype**: For breaking changes, further refine the category of change. For example, you can have API, configuration, or plugin breaking changes.

## Best practices

When creating changelog entries, follow these best practices:

- **Consider the audience**: Remember that release notes are read by developers, system administrators, end users, and support teams. Focus on what problems are solved or how users are affected, not implementation details.
- **Keep it concise**: Release notes should be scannable. Users often read many entries quickly.
- **Be specific**: Avoid vague descriptions. Explain exactly what changed and why it matters.
- **Use consistent language**: Follow the same terminology used in the product documentation.
- **Link to related content**: Include links to documentation and related issues when helpful.
- **Test your descriptions**: Have someone unfamiliar with the change read your entry to ensure it's clear.

### Choose the changelog type [changelog-types]

The changlog type categorizes your change and determines which section it appears in within the release notes. Choose the type that best describes your change:

Breaking change
:   Use `breaking-change` for changes that potentially make other systems that rely on the product break or misbehave.
:   Always include `impact` and `action` fields.
:   Consider including a `subtype` (for example, `api`, `behavioral`, or `configuration`.)
:   Examples include API changes, configuration format changes, removed features, and behavioral changes that break compatibility.

Bug fix
:   Use `bug-fix` for the resolution of a bug that existed in previous releases.
:   Focus on what was wrong and what is now correct.
:   Examples include fixes for crashes, incorrect behavior, data loss, and security vulnerabilities.

Deprecation
:   Use `deprecation` for functionality that will be removed in a later release.
:   Focus on what users need to do to migrate away from the deprecated functionality.
:   Optionally include `impact` and `action` fields.
:   Examples include APIs, configuration options, or features scheduled for removal.

Enhancement
:   Use `enhancement` for minor improvements that don't break or fix existing behavior.
:   Focus on how existing functionality is improved.
:   Examples include performance improvements, UI refinements, and expanded options for existing features.

Feature
:   Use `feature` for new user-facing functionality or significant new capabilities.
:   Focus on what users can now do that they couldn't before.
:   Examples include new APIs, major UI features, new integrations, and significant new capabilities.

Known issue
:   Use `known-issue` for problems that are not fixed in the release but are actively being worked on.
:   Include information about all affected versions and contexts.
:   Optionally include `impact` and `action` fields (with workaround steps).
:   Examples include significant defects or limitations that might impact implementation.

Other
:   Use `other` for any information that doesn't fit into the above categories.
:   Use sparingly.

Security
:   Use `security` for security advisories about vulnerabilities.
:   Follow security team guidelines for disclosure of sensitive information.
:   Examples include security patches and vulnerability disclosures.

### Writing effective titles [changelog-titles]

The changelog title should be a clear, concise, and user-focused summary.

Follow these best practices:

- **Use present tense**: "Adds support for..." not "Added support for...".
- **Focus on user impact**: What can users do now, or what problem is solved?
- **Be specific**: Avoid vague titles like "Bug fixes and performance improvements".
- **Keep it short**: Use a maximum of 80 characters.
- **Avoid jargon and acronyms**: Use plain language that all users can understand.
- **Start with action verbs**: "Fixes...", "Adds...", "Improves...", "Removes...".

#### Good title examples

- "Adds support for custom authentication providers"
- "Fixes memory leak in long-running queries"
- "Improves query performance for date range filters"
- "Removes deprecated `_all` field from search API"

#### Poor title examples

- "Bug fixes" (too vague)
- "Refactored internal query processing" (focuses on implementation, not user impact)
- "Fixed bug #12345" (uses internal reference, doesn't explain impact)
- "Performance improvements" (too vague)

### Writing effective descriptions [changelog-descriptions]

The changelog description provides additional context about the change.
Not all changes need a description. If the title is self-explanatory, you can omit it.

Include a description when:

- The change needs additional context to be understood.
- There are important details users should know.
- The change affects multiple components or has broader implications.
- You need to explain limitations or caveats.

Follow these best practices:

- **Keep it concise**: Use a maximum of 600 characters.
- **Focus on user value**: Explain what users can do or what problems are solved.
- **Provide context**: Help users understand when or why they would use this.
- **Include relevant details**: Describe configuration changes, API changes, or behavioral differences.
- **Use code blocks**: Consider the layout of your configuration examples and code snippets.

#### Good description examples

- This enhancement allows you to configure custom authentication providers through the security settings. Previously, only built-in providers were supported.
- Fixes an issue where queries with date range filters could cause excessive memory usage in clusters with many shards. The fix optimizes memory allocation for date range queries.

#### Poor description examples

- "Internal refactoring": Doesn't explain user impact.
- "See PR #12345 for details": Doesn't provide information, only a reference.
- Repeating the title verbatim, which adds no value.

### Writing about impact and actions

The changelog impact and action fields are required for breaking changes and recommended for deprecations and known issues.
They help users understand what changed and what they need to do.

The impact field explains how the user's environment is affected by the change.
Follow these best practices:

- Be specific about what breaks or changes.
- Explain the scope of the impact (such as whether it affects all users or specific configurations).
- Use clear, direct language.

The action field provides steps users must take to mitigate the change.
Follow these best practices:

- Provide clear, actionable steps.
- Order steps logically (most important first).
- Include code examples or configuration snippets when helpful.
- Be prescriptive—tell users exactly what to do.

#### Good impact examples

- For a breaking change: "The `_all` field is no longer available in search queries. Any queries that reference `_all` will fail with an error".
- For a deprecation: "The `old_api` endpoint continues to work but will be removed in version 10.0. No new features will be added to this endpoint".

#### Good action examples

- For a breaking change: "Update all queries that use `_all` to use specific field names instead. For example, replace `_all:search_term` with `message:search_term OR title:search_term`".
- For a deprecation: "Migrate to the new `new_api` endpoint before version 10.0. Update your code to use `POST /api/v2/endpoint` instead of `POST /api/v1/old_endpoint`. View the migration guide for detailed examples."
- For a known issue: "As a workaround, restart the service after applying the configuration change. This issue will be fixed in the next release".

## Common anti-patterns

Avoid these common mistakes:

- **Focusing on implementation**: Don't describe how you fixed something; describe the user impact.
- **Using internal references**: Avoid "Fixed bug #12345" or "See PR #67890"--summarize the change so that users can decide whether to follow the links.
- **Being too vague**: "Bug fixes and performance improvements" doesn't help users understand what changed.
- **Including unnecessary technical details**: Skip internal architecture changes unless they affect users.

## Examples

Here are some examples of well-structured release notes in the Elastic documentation:

- [{{es}} release notes](elasticsearch://release-notes/index.md)
- [{{agent}} release notes](elastic-agent://release-notes/index.md)
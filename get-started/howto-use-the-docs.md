---
applies_to:
  serverless:
  stack:
---
# How to use the documentation

Our documentation is organized to guide you through your journey with Elastic, from learning the basics to deploying and managing complex solutions.

Here is a detailed breakdown of the documentation structure:

* [**Elastic fundamentals**](/get-started/index.md): Understand the basics about the deployment options, platform, solutions, and features of the documentation.  
* [**Solutions and use cases**](/solutions/index.md): Learn use cases, evaluate, and implement Elastic's solutions: Observability, Search, and Security.  
* [**Manage data**](/manage-data/index.md): Learn about data store primitives, ingestion and enrichment, managing the data lifecycle, and migrating data.  
* [**Explore and analyze**](/explore-analyze/index.md): Get value from data through querying, visualization, machine learning, and alerting.  
* [**Deploy and manage**](/deploy-manage/index.md): Deploy and manage production-ready clusters. Covers deployment options and maintenance tasks.  
* [**Manage your Cloud account**](/cloud-account/index.md): A dedicated section for user-facing cloud account tasks like resetting passwords.  
* [**Troubleshoot**](/troubleshoot/index.md): Identify and resolve problems.  
* [**Extend and contribute**](/extend/index.md): How to contribute to or integrate with Elastic, from open source to plugins to integrations.  
* [**Release notes**](/release-notes/index.md): Contains release notes and changelogs for each new release.  
* [**Reference**](/reference/index.md): Reference material for core tasks and manuals for other Elastic products.

## Applicability badges

Because you can deploy Elastic products in different ways (like on {{ecloud}} or in your own data center) and have different versions, not all documentation applies to every user. To help you quickly see if a topic is relevant to your situation, we use **applicability badges**.

These badges appear at the top of a page or section and tell you which products, deployment models, and versions the content applies to. They also indicate the maturity level of a feature, such as **beta**, **technical preview**, or **generally available (GA)**. This system ensures that you can identify content specific to your environment and version.

:::{tip}
A **Stack** badge indicates that a page applies to [{{stack}}](/get-started/the-stack.md) components across all deployment options except {{serverless-full}}. If a page applies to all deployment options, it will have **{{serverless-short}}** and Stack badges.
:::

## Page options

On each documentation page, you'll find several links that allow you to interact with the content:

* **View as Markdown**: This link shows you the raw Markdown source code for the page you're viewing. This can be helpful if you want to reuse the source or feed the document to AI.  
* **Edit this page**: Selecting this link will take you directly to the page's source file in its GitHub repository. From there, you can propose edits, which our team will review.  
* **Report an issue**: If you've found a problem, like a typo, a technical error, or confusing content, but don't want to edit the page yourself, use this link. It will open a new issue in our GitHub repository, pre-filled with information about the page you were on, so you can describe the problem in detail.

## Versioned documentation

Starting with Elastic Stack 9.0, Elastic no longer publishes separate documentation sets for each minor release. Instead, all changes in the 9.x series are included in a single, continuously updated documentation set.

This approach helps:

* Reduce duplicate pages.  
* Show the full history and context of a feature.  
* Simplify search and navigation.

We clearly mark content added or changed in a specific version using availability badges. The availability badges appear in page headers, section headers, and inline.

### Elastic Stack example

{applies_to}`stack: ga 9.1.0`

This means the feature is:

* Generally Available (GA) in the [{{stack}}](/get-started/the-stack.md) across all deployment options except {{serverless-full}}
* Introduced in version 9.1.0

:::{tip}
If a page applies to all deployment options including {{serverless-full}}, it will have both {{serverless-short}} and Stack badges.
:::

### Serverless example

{applies_to}`serverless: ga` {applies_to}`security: beta`

This means the feature is:

* Generally Available for {{es-serverless}} projects  
* Beta for {{sec-serverless}} projects

### Elastic Cloud Enterprise example

{applies_to}`ece: deprecated 4.1.0`

This means the feature is:

* Available on Elastic Cloud Enterprise  
* Deprecated starting in version 4.1.0

:::{tip}
Want to learn more about how availability badges are used? Check the [Elastic Docs syntax guide](https://elastic.github.io/docs-builder/syntax/applies/).
:::

## Accessing previous versions

You can browse documentation for different versions of our products in two ways:

* **Version menu:** On most documentation pages, you'll find a version menu. Clicking this menu allows you to switch to a different version of the documentation for the content you are currently viewing.  
* **All documentation versions page:** For a complete list of all available documentation versions for all Elastic products, you can visit the [All documentation versions](/versions.md) page.

## Glossary

To help you understand the terminology used throughout our documentation, we provide a [glossary of common Elastic terms](/reference/glossary/index.md). This is a great resource for new users or anyone looking to clarify the meaning of a specific term.

## How to contribute

We value contributions from our community. For detailed instructions on how to contribute to both the main documentation and the API references, refer to our [contribution guide](https://www.elastic.co/docs/extend/contribute/).
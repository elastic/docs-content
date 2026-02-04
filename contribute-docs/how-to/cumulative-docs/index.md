---
description: "Cumulative documentation is a single-source-of-truth approach where pages evolve over time to accommodate version and deployment differences, rather than maintaining separate documentation sets."
applies_to:
  stack:
  serverless:
type: overview
---

# Cumulative documentation

Cumulative documentation is a single-source-of-truth approach used in the Elastic documentation ([elastic.co/docs](https://elastic.co/docs)). Instead of publishing separate documentation sets for each minor release, cumulative docs use a tagging system to indicate which content applies to specific versions, products, and deployment types. The same page evolves over time to accommodate these differences.

:::{important}
Cumulative documentation applies to the following versions and products: Elastic Stack 9.0+, ECE 4.0+, ECK 3.0+, EDOT, and unversioned products like Serverless and Elastic Cloud.

Our AsciiDoc-based documentation system continues to be published and maintained for earlier versions: Elastic Stack 8.x and earlier, ECE 3.x and earlier, ECK 2.x and earlier.
:::

## Use cases

Cumulative documentation is valuable when:

* **Features evolve across versions**: When functionality is added, changed, or deprecated across product versions, cumulative docs allow you to document all supported versions in a single location.
* **Deployment differences exist**: When features or configurations differ between Elastic Cloud Serverless, Elastic Cloud Hosted, or self-managed deployments, cumulative docs let users compare options on one page.
* **Product availability varies**: When features are available in some products but not others (for example, available in {{es}} but not in Kibana), cumulative docs clearly indicate these boundaries.
* **Lifecycle changes occur**: When features move between states (Tech Preview → Beta → GA), cumulative docs track these transitions without creating separate documentation sets.

## Benefits

### For readers

When users arrive at an Elastic documentation page, they find a single source of truth that:

* Contains content relevant to their specific version and deployment type
* Allows comparison of features and functionality across different offerings
* Eliminates the need to switch between multiple versions of the same page
* Reduces confusion about which documentation applies to their situation

:::{image} ./images/reader-experience.png
:screenshot:
:alt: Screenshot showing documentation with version-specific badges indicating which stack versions and deployment types features apply to, allowing users to quickly identify relevant content
:::

### For contributors

Cumulative documentation provides several advantages for documentation maintainers:

* **Single source of truth**: One canonical page per feature reduces inconsistencies and maintenance overhead
* **No drift**: Eliminates divergence between similar documentation sets that can occur with version-specific copies
* **Efficient updates**: Changes apply to all applicable versions from a single edit
* **Clear history**: Version control shows the complete evolution of a feature's documentation
* **Better coverage**: Makes it easier to document deprecations and removals without losing historical context for users on older versions

## How it works

Cumulative documentation uses the `applies_to` tagging system in Markdown source files to indicate version and deployment applicability. These tags control how content is displayed to users based on their context.

### The tagging system

There are three levels where you can apply tags:

1. **Page-level tags** (mandatory): Added to the frontmatter to define overall applicability of the page
2. **Section-level tags**: Applied to individual sections when only parts of a page vary
3. **Element-level tags**: Applied to specific elements like tabs, dropdowns, and admonitions for fine-grained control

### When to tag content

**You should tag content when:**

* Functionality is added in a specific version
* Functionality changes state (for example, Tech Preview → Beta → GA)
* Availability varies by deployment type (for example, available in {{ech}} but not in {{ece}})
* Features are deprecated or removed in specific versions

**You generally don't need to tag:**

* Content-only changes like fixing typos or improving clarity
* Every paragraph when applicability has been established earlier on the page
* General availability features in unversioned products (Serverless) where all users are on the latest version

### Version configuration and dynamic rendering

The cumulative docs system uses a central version configuration file ([`versions.yml`](https://github.com/elastic/docs-builder/blob/main/config/versions.yml)) that tracks:

* Latest released versions of all products
* Earliest versions documented in the Docs V3 system
* Version ranges for all supported products

This configuration drives the dynamic rendering logic, which:

* Labels unreleased versions as `planned`
* Enables continuous documentation releases
* Allows {{stack}} and Serverless offerings to be documented together

:::{tip}
Read more about how site configuration works in the [docs-builder configuration guide](https://elastic.github.io/docs-builder/configure/site/).
:::

:::{include} /contribute-docs/_snippets/tag-processing.md
:::

## Key concepts

Understanding these terms will help you work with cumulative documentation:

* **`applies_to` tags**: Metadata tags that indicate which versions, products, or deployment types content applies to
* **Page-level tags**: Frontmatter tags that define overall applicability of an entire page (mandatory)
* **Section-level tags**: Tags applied to specific sections when only parts of a page vary
* **Element-level tags**: Fine-grained tags applied to specific content elements like tabs or admonitions
* **Dynamic rendering**: The system that displays or hides content based on user context and version configuration

:::{tip}
**Key principles for contributors:**

* **Never remove content for supported versions**: Information should remain available for all supported product versions unless it was never accurate.
* **Use page-level tags**: Always include `applies_to` tags in the page frontmatter.
* **Tag at the appropriate level**: Apply tags at the highest level that makes sense (page > section > element) to avoid over-tagging.
* **Maintain single source of truth**: Each feature should have one canonical documentation page that evolves over time.
:::

## Next steps

To start contributing to cumulative documentation:

* Review the [cumulative docs guidelines](guidelines.md) for detailed decision-making guidance on when and how to tag content
* Learn about [badge usage and placement](badge-placement.md) to understand how to integrate `applies_to` badges into different content structures
* Explore [example scenarios](example-scenarios.md) to see real-world examples organized by documentation maturity level
* Reference the [`applies_to` syntax guide](https://elastic.github.io/docs-builder/syntax/applies) for all valid values and syntax patterns

## Related pages

* [Content types overview](/contribute-docs/content-types/index.md) - Understand how to structure different types of documentation pages
* [Cumulative docs reference](reference.md) - Quick reference for `applies_to` syntax
* [Docs builder syntax guide](https://elastic.github.io/docs-builder/syntax/) - Complete documentation for Markdown syntax in Elastic docs

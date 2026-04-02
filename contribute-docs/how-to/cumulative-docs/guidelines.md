---
navigation_title: Guidelines
---

# Cumulative docs guidelines

:::{note}
This content is still in development.
If you have questions about how to write cumulative documentation while contributing,
reach out to **@elastic/docs** in the related GitHub issue or PR.
:::

To get started with cumulative docs, ask yourself:

* Does this content vary between products, versions, or deployment types?
* Is this a feature lifecycle change or just content improvement?
* Will users benefit from knowing this information?

If the answer to at least one of these questions is _yes_, follow these guidelines to write cumulative documentation.

## What `applies_to` tags can communicate

### Type

In cumulative documentation, you can use `applies_to` to communicate:

* **Product- or deployment-specific availability**: When content applies to or functions differently between products or deployment types (for example, Elastic Cloud Serverless or Elastic Cloud Hosted). Read more in [Product and deployment model applicability](#products-and-deployment-models).
* **Feature lifecycle and version-related functionality**: When features are introduced, modified, or removed in specific versions, including lifecycle changes (for example, going from Beta to GA). Read more in [Version and product lifecycle applicability](#versions).

Both types of applicability are added as part of the same `applies_to` tagging logic.
The product or deployment type is the [key](reference.md#key)
and the [feature lifecycle](reference.md#lifecycle)
and [version](reference.md#version) make up the value.

```
<key>: <lifecycle> <version>
```

### Level

For each type of applicability information, you can add `applies_to` metadata at different levels:

* **Page-level** metadata is **mandatory** and must be included in the frontmatter.
  This defines the overall applicability of the page across products and deployment models.
* **Section-level** annotations allow you to specify different applicability for individual sections
  when only part of a page varies between products or versions.
* **Element-level** annotations allow tagging block-level elements like tabs, dropdowns, and admonitions.
  Choosing the right element can help communicate how to interpret applicability information. For example
  tabs might indicate alternatives (only one tab is relevant to each user) and admonitions might indicate
  that there is a notable exception to applicability in some context.
* **Inline** annotations allow fine-grained annotations within paragraphs or lists.
  This is useful for highlighting the applicability of specific phrases, sentences,
  or properties without disrupting the surrounding content.

For a full syntax reference for page, section, and inline level `applies_to` annotations,
refer to [the applies_to syntax guide](https://elastic.github.io/docs-builder/syntax/applies).

## Dimensions

The `applies_to` keys fall into three dimensions based on the products and user contexts being documented on the page:

| Dimension | Description | Values |
| --- | --- | --- |
| Stack/Serverless | Represents the version or "flavor" of the core Elastic platform. Use when your content is primarily about features, functionality, or workflows that vary based on which version of the Elastic platform users are running.<br><br>Also use for deployment, configuration, or management tasks that are available or consistent across deployment types (these are often built into Elasticsearch - see tips). | `stack`, `serverless` |
| Deployment | Represents how the Elastic platform is deployed and orchestrated. Use when your content is primarily about deployment, configuration, or management tasks that differ based on how users have deployed Elasticsearch and Kibana, or a deployment-specific tutorial for a stack task. | `deployment` (with subkeys: `ece`, `eck`, `ess`, `self`), `serverless` |
| Product | Represents software outside the core Elastic platform that has its own versioning scheme. Use when your content is primarily about features or functionality specific to these standalone products. | `product` (with subkeys, including those for APM agents, EDOT SDKs, and client libraries) |

Most pages focus on one primary context, so you should only use keys from one dimension at the page level. For example, a page about a Kibana feature would use the Stack/Serverless dimension, while a page about configuring cluster settings would use the Deployment dimension.

### Dimension usage tips

* `serverless` can appear in both the Stack/Serverless dimension and the Deployment dimension. This is because Serverless acts as both a "version" or "flavor" of the stack (like `stack`), and a unique deployment type with specialized management processes (like `ece` or `eck`).
* The versioned Elastic Stack (`stack`) can be deployed across ECE, ECK, ECH, and self-managed clusters. When deployment, configuration, or management tasks are available or consistent across these deployment types (often because they're built into Elasticsearch), use `stack` in the Stack/Serverless dimension rather than specifying each deployment type individually.
* If your content has nuances specific to another dimension, determine the "primary" dimension for the page level `applies_to` frontmatter, and then add the secondary dimension information as requirements, or as tagged sections later on the page. 
* To determine the primary dimension of a page, consider what the main focus of the page is, what most of the content relates to, and what context users will primarily identify with when they arrive at the page. For example, if a page is primarily about a Kibana feature but mentions deployment-specific configuration, use the Stack/Serverless dimension as primary. Refer to [Cumulative docs example scenarios](/contribute-docs/how-to/cumulative-docs/example-scenarios.md#primary-dimension) for an example.

## General guidelines

### When to tag content

Every page should include page-level `applies_to` tags to indicate which product or deployment type
the content applies to. This is mandatory for every page.

You should also generally tag content when:

* **Functionality is added**:
  Tag content if the functionality described is added in a specific release.

* **Functionality changes state**:
  Tag content if existing functionality changes state (`preview`, `beta`, `ga`, `deprecated`, `removed`).

* **Availability varies**:
  Tag content if the availability of the functionality described differs across products or deployment types.

### When _not_ to tag content

You generally do not need to tag:

* **Content-only changes**:
  Do _not_ tag content-only changes like typo fixes, formatting updates, information architecture updates,
  or other documentation updates that don't reflect feature lifecycle changes.

* **Every paragraph/section**:
  You do _not_ need to tag every section or paragraph.
  Only tag when the context or applicability changes from what has been established earlier on the page.

* **Unversioned products**:
  For products where all users are always on the latest version (like serverless),
  you do _not_ need to tag workflow changes if the product lifecycle is unchanged.

### Tips

* **Consider how badges take up space on the page**:
  Avoid badge placement patterns that take up unnecessary Markdown real estate.
  For example, adding a dedicated column for applicability in a table when only
  a few rows require an `applies_to` badge.
* **Use `unavailable` sparingly**:
  For example, if a page is only about Elastic Cloud Hosted, don't add a `serverless: unavailable` tag.
  Refer to [When to indicate something is NOT applicable](#when-to-indicate-something-is-not-applicable) for specific guidance.
* **Don’t assume features are available everywhere**:
  For example, if a Kibana UI panel is missing from Serverless,
  notate it in the documentation even if it is intuitive.
* **Clarify version availability per context**:
  Sometimes features GA for one deployment but remain preview for another.
* **Think across time**:
  Product lifecycle changes with each release.
  Even if a feature might be deprecated or legacy in one deployment it might still be supported elsewhere.
* **For updates, remember they might be older than you think**:
  Some updates that might be required to the documentation could precede v9.0.
  For these changes need to be made to the old AsciiDoc versions of the content.

## Order of items [order-of-items]

### Versions [order-versions]

When listing multiple versions, author the newest version first whenever possible. This keeps files consistent and easier to maintain.
Regardless of the source file, the build system automatically renders badge lifecycles in reverse chronological order.
This means that badges always appear to users from newest to oldest, which is the reverse of the product development timeline.

For example this syntax:

```
{applies_to}`stack: preview =9.0, beta =9.1, ga 9.2+`
```

Results in this badge:

{applies_to}`stack: preview =9.0, beta =9.1, ga 9.2+`

### Keys [order-keys]

The build system automatically orders multiple [keys](reference.md#key) in a consistent pattern. This reduces authoring overhead and makes content easier for users to scan.

:::{important}
Key ordering only occurs if all keys are declared in the same directive. Keys declared seperately, for example: ``` {applies_to}`stack: ga` {applies_to}`serverless: preview` ```, will not be reordered by docs-builder.
:::

Keys are ordered as follows:

1. **Stack/Serverless**: Stack, Serverless
2. **Deployment types**: ECH (Elastic Cloud Hosted), ECK (Elastic Cloud on Kubernetes), ECE (Elastic Cloud Enterprise), Self-Managed
3. **ProductApplicability**: ECCTL, Curator, EDOT items (alphabetically), APM Agent items (alphabetically)

For example this syntax:

````
```{applies_to}
deployment:
  ece: ga
  self: ga
serverless: ga
```
````

Results in the badges in this order:

{applies_to}`{ deployment: { ece: ga, self: ga }, serverless: ga }`

## Product and deployment model applicability [products-and-deployment-models]

For the full list of supported product and deployment model tags,
refer to [](reference.md#key).

### Guidelines [products-and-deployment-models-guidelines]

* **Always include page-level product and deployment model applicability information**.
  This is _mandatory_ for all pages.
* **Use only one dimension at the page level.**
  Choose either the Stack/Serverless dimension, the Deployment dimension, or the Product dimension.
  See [Dimensions](#dimensions) for more information.
* **Determine if section or inline applicability information is necessary.**
  This _depends on the situation_.
  * For example, if a portion of a page is applicable to a different context than what was specified at the page level,
  clarify in what context it applies using section or inline `applies_to` badges.
  * Section-level and inline annotations can reference items from a different dimension than the page-level dimension when needed to clarify specific requirements.
% Source: https://elastic.github.io/docs-builder/versions/#defaults-and-hierarchy
* **Do not assume a default product or deployment type.**
  Treat all products and deployment types equally. Don't treat one as the "base" and the other as the "exception".

### Common scenarios [products-and-deployment-models-examples]

Here are some common scenarios you might come across:

* Content is about both Elastic Stack components and the Serverless UI.
  ([example](example-scenarios.md#stateful-serverless))
* Content is primarily about orchestrating, deploying, or configuring an installation.
  ([example](example-scenarios.md#workflow-tabs))
* Content is primarily about a product following its own versioning schema.
  % TO DO: Add example
  % ([example](example-scenarios.md#))
* A whole page is generally applicable to Elastic Stack 9.0 and to Serverless,
  but one specific section isn’t applicable to Serverless.
  ([example](example-scenarios.md#page-section-varies-product))
* The whole page is generally applicable to all deployment types,
  but one specific paragraph only applies to Elastic Cloud Hosted and Serverless,
  and another paragraph only applies to Elastic Cloud Enterprise.
  ([example](example-scenarios.md#page-section-varies-deployment))
* Likewise, when the difference is specific to just one paragraph or list item, the same rules apply.
  Just the syntax slightly differs so that it stays inline.
  % TO DO: Add example
  % ([example](example-scenarios.md#))

## Version and product lifecycle applicability [versions]

### Guidelines [versions-guidelines]

* **Ensure your change is related to a specific version.**
  Even though a change is made when a specific version is the latest version,
  it does not mean the added or updated content only applies to that version.
  * For example, you should not use version tagging when fixing typos,
    improving styling, or adding a long-forgotten setting.
% Source: https://github.com/elastic/kibana/pull/229485/files#r2231876006
* **Do _not_ use version numbers in prose**.
  Avoid using version numbers in prose adjacent to `applies_to` badge to prevent
  confusion when the badge is rendered with `Planned` ahead of a release.
* **Cumulative documentation is not meant to replace release notes.**
  * For example, if a feature becomes available in {{serverless-short}} and
    doesn’t have a particular lifecycle state to call out (preview, beta, deprecated…),
    it does not need specific tagging. However, it does need a release note entry to document the change.
* **Consider carefully when the change is going to be published.**
  Read more about how publishing can vary between repos in the [branching strategy guide](https://elastic.github.io/docs-builder/contribute/branching-strategy/).
* **Do not use date-based tagging for unversioned products.**
  `applies_to` does not accept date-based versioning.
* **Be aware of exceptions.**
  If the content also applies to another context (for example a feature is removed in both Kibana 9.x and Serverless),
  then it must be kept for any user reading the page that may be using a version of Kibana prior to the removal.

### Common scenarios [versions-examples]

#### Unversioned products

For unversioned products like {{serverless-short}} or {{ecloud}}:

* When a new feature is introduced in an unversioned product:
  * If it is added in GA, label only at the page level.
    There is no need to label newly added GA content in unversioned products at the section or line level
    if it is already labeled as available at the page level.
    ([example](example-scenarios.md#unversioned-added))
  * If it is added in technical preview or beta, and the related content is added to an existing page
    that is already labeled as generally available in the unversioned product at the page level,
    label the new technical preview or beta content at the section or line level.
    ([example](example-scenarios.md#unversioned-added))
* When a feature in an unversioned product changes lifecycle state to `preview`, `beta`, `ga` or `deprecated`,
  replace the previous lifecycle state with the new lifecycle state.
  ([example](example-scenarios.md#lifecycle-changed))
* When a feature in an unversioned product is removed, remove the content altogether
  unless the content also applies to another context that is versioned
  (refer to [Mixed versioned and unversioned products](#mixed)).

#### Versioned products

For versioned products like the Elastic Stack:

* When a new feature is introduced in a versioned product, label the content with the lifecycle state
  and the version in which it was introduced.
  % TO DO: Add example
  % ([example](example-scenarios.md#))
* When a feature in a versioned product changes lifecycle state,
  append the new lifecycle state and the version in which the state changed to the relevant key in `applies_to`.
  This applies to all lifecycle states including `preview`, `beta`, `ga`, `deprecated`, and `removed`
  ([example](example-scenarios.md#lifecycle-changed)).


#### Mixed versioned and unversioned products [mixed]

* When documenting features shared between serverless and Elastic Stack
  ([example](example-scenarios.md#stateful-serverless)).
* When a feature in an unversioned product is removed, but the content also applies to
  another context (for example a feature is removed in both Kibana 9.x and Serverless),
  then it must be kept for any user reading the page that may be using a version of
  the product prior to the removal.
  ([example](example-scenarios.md#removed))

## When to indicate something is NOT applicable

By default, we communicate that content does not apply to a certain context by simply **not specifying it**.
For example, a page describing how to create an {{ech}} deployment just requires identifying "{{ech}}" as context. No need to overload the context with additional `serverless: unavailable` indicators.

This is true for most situations. However, it can still be useful to call it out in a few specific scenarios:

* **When there is a high risk of confusion for users**. For example, if a feature is available in two out of three serverless project types, it might make sense to clarify and be explicit about the feature being “unavailable” for the third type.

  ```yml
  ---
  applies_to:
    stack: ga
    serverless:
      elasticsearch: ga
      security: ga
      observability: unavailable
  ---
  ```


* **When only one section, paragraph, or element describes functionality that is unavailable in the context set at a higher level**.
  For example, if a page is largely applicable to both `serverless` and `stack`, but one section describes functionality that is not possible in serverless (and there is no alternative).

  ````md
  ---
  applies_to:
    stack: ga
    serverless: ga
  —--

  # Spaces

  [...]

  ## Configure a space-level landing page [space-landing-page]
  ```{applies_to}
  serverless: unavailable
  ```
  ````


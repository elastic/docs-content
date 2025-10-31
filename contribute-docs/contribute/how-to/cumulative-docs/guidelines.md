---
navigation_title: Guidelines
---

% Audience: Anyone who contributes to docs
% Goals:
%   * Provide guidance that is appropriate for new contributors

# Cumulative docs guidelines

Start by asking yourself:

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
% TO DO: Add when https://github.com/elastic/docs-builder/issues/1436 is complete
% * **Element-level** annotations allow tagging block-level elements like tabs, dropdowns, and admonitions.
%  This is useful for ...
* **Inline** annotations allow fine-grained annotations within paragraphs or lists.
  This is useful for highlighting the applicability of specific phrases, sentences,
  or properties without disrupting the surrounding content.

For a full syntax reference for page, section, and inline level `applies_to` annotations,
refer to [](/contribute-docs/syntax/applies.md).

## General guidelines

### When to tag content

Every page should include page-level `applies_to` tags  to indicate which product or deployment type
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

% Source: Slack conversation
* **Consider how badges take up space on the page**:
  Avoid badge placement patterns that take up unnecessary Markdown real estate.
  For example, adding a dedicated column for applicability in a table when only
  a few rows require an `applies_to` badge.
% Source: George's checklist
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
  Even if a feature might be deprecated or legacy in one deployment it may still be supported elsewhere.
* **For updates, remember they may be older than you think**:
  Some updates that may be required to the documentation could precede v9.0.
  For these changes need to be made to the old AsciiDoc versions of the content.

% TO DO: Update when the PRs that auto-sort order are merged
% Maybe move to the "how dynamic tagging works"?
## Order of items

### Versions

When listing multiple versions, author the newest version first whenever possible. This keeps files consistent and easier to maintain.
Regardless of the source file, the build system automatically builds badge lifecycles in reverse chronological order.
This means that badges will always appear to users from newest to oldest, which is the reverse of the product development timeline.

For example:

{applies_to}`stack: preview 9.0.5, beta 9.1, ga 9.2`

### Keys

The build system automatically orders multiple [keys](reference.md#key) in a consistent pattern. This reduces authoring overhead and makes content easier for users to scan.

:::{important}
Key ordering only occurs if all keys are declared in the same directive. Keys declared seperately, for example: ``` {applies_to}`stack: ga` {applies_to}`serverless: preview` ```, will not be reordered by docs-builder.
:::

Keys are ordered as follows:

1. **Stack/Serverless**: Stack, Serverless
2. **Deployment types**: ECH (Elastic Cloud Hosted), ECK (Elastic Cloud on Kubernetes), ECE (Elastic Cloud Enterprise), Self-Managed
3. **ProductApplicability**: ECCTL, Curator, EDOT items (alphabetically), APM Agent items (alphabetically)

For example:

```{applies_to}
deployment:
  ece: ga
  self: ga
stack: ga
serverless: ga
```

## Product and deployment model applicability [products-and-deployment-models]

For the full list of supported product and deployment model tags,
refer to [](reference.md#key).

### Guidelines [products-and-deployment-models-guidelines]

* **Always include page-level product and deployment model applicability information**.
  This is _mandatory_ for all pages.
* **Determine if section or inline applicability information is necessary.**
  This _depends on the situation_.
  * For example, if a portion of a page is applicable to a different context than what was specified at the page level,
  clarify in what context it applies using section or inline `applies_to` badges.
% Source: https://elastic.github.io/docs-builder/versions/#defaults-and-hierarchy
* **Do not assume a default product or deployment type.**
  Treat all products and deployment types equally. Don't treat one as the "base" and the other as the "exception".

### Common scenarios [products-and-deployment-models-examples]

Here are some common scenarios you might come across:

* Content is about both Elastic Stack components and the Serverless UI.
  ([example](example-scenarios.md#stateful-serverless))
* Content is primarily about orchestrating, deploying or configuring an installation.
  % TO DO: Add example
  % ([example](example-scenarios.md#))
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

* When documenting features shared between serverless and Elastic Stack,
  ...
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

* When there is a high risk of confusion for users. This may be subjective, but let’s imagine a scenario where a feature is available in 2 out of 3 serverless project types. It may make sense to clarify and be explicit about the feature being “unavailable” for the 3rd type. For example:

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


* When a specific section, paragraph or list item has specific applicability that differs from the context set at the page or section level, and the action is not possible at all for that context (meaning that there is no alternative). For example:

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


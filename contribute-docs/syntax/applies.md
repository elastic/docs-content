# Applies to

Starting with Elastic Stack 9.0, ECE 4.0, and ECK 3.0, documentation follows a [cumulative approach](/contribute/cumulative-docs/index.md): instead of creating separate pages for each product and release, we update a single page with product- and version-specific details over time.

To support this, source files use a tagging system to indicate:

* Which Elastic products and deployment models the content applies to.
* When a feature changes state relative to the base version.

This is what the `applies_to` metadata is for. It can be used at the [page](#page-level),
[section](#section-level), or [inline](#inline-level) level to specify applicability with precision.

:::{note}
For detailed guidance, refer to [](/contribute/cumulative-docs/index.md).
:::

## Syntax

The `applies_to` metadata supports an [exhaustive list of keys](#key-value-reference).

When you write or edit documentation, only specify the keys that apply to that content. Each key accepts values with the following syntax:

```
<key>: <lifecycle> [version], <lifecycle> [version], ...
```

Where:

- The lifecycle is mandatory.
- The version is optional.

### Page level

Page level annotations are added in the YAML frontmatter, starting with the `applies_to` key and following the [key-value reference](#key-value-reference). For example:

```yaml
---
applies_to:
  stack: ga
  deployment:
    ece: ga
---
```

For more examples, refer to [Page annotation examples](#page-annotation-examples).

:::{important}
All documentation pages must include an `applies_to` tag in the YAML frontmatter.
:::

### Section level

A header can be followed by an `{applies_to}` directive which contextualizes the applicability of the section further.

Section-level `{applies_to}` directives require triple backticks because their content is literal. Refer to [](directives.md#exception-literal-blocks) for more information.

````markdown
```{applies_to}
stack: ga 9.1
```
````

To play even better with Markdown editors the following is also supported:

````markdown
```yaml {applies_to}
stack: ga 9.1
```
````

This allows the YAML inside the `{applies_to}` directive to be fully highlighted.

For more examples, refer to [Section annotation examples](#section-annotation-examples).

:::{note}
Section-level `{applies_to}` directives must be preceded by a heading directly.
:::

### Inline level

You can add inline applies annotations to any line using the following syntax:

```markdown
This can live inline {applies_to}`section: <life-cycle> [version]`
```

A specialized `{preview}` role exists to quickly mark something as a technical preview. It takes a required version number
as an argument.

```markdown
Property {preview}`<version>`
:   definition body
```

For more examples, refer to [Inline annotation examples](#inline-annotation-examples).

## Key-value reference

Use the following key-value reference to find the appropriate key and value for your applicability statements.

:::::{tab-set}

::::{tab-item} Keys

:::{include} /_snippets/applies_to-key.md
:::

::::

::::{tab-item} Lifecycles

:::{include} /_snippets/applies_to-lifecycle.md
:::

::::

::::{tab-item} Versions

:::{include} /_snippets/applies_to-version.md
:::

::::
:::::

## Examples

### Versioning examples

Versioned products require a `version` tag to be used with the `lifecycle` tag:

```
applies_to:
  stack: preview 9.1, ga 9.4
  deployment:
    ece: deprecated 9.2, removed 9.8
```

Unversioned products use `lifecycle` tags without a version:

```
applies_to:
  serverless:
    elasticsearch: beta
    observability: removed
```

### Lifecycle and versioning examples

:::::{dropdown} Unversioned products

:::{include} _snippets/unversioned-lifecycle.md
:::

:::::

:::::{dropdown} Versioned products

:::{include} _snippets/versioned-lifecycle.md
:::

:::::

:::::{dropdown} Identify multiple states for the same content

:::{include} /syntax/_snippets/multiple-lifecycle-states.md
:::

:::::

### Page annotation examples

:::{include} _snippets/page-level-applies-examples.md
:::

### Section annotation examples

:::{include} _snippets/section-level-applies-examples.md
:::

### Inline annotation examples

:::{include} _snippets/inline-level-applies-examples.md
:::

## Structured model

![Applies To Model](images/applies.png)

The previous model is projected to the following structured YAML.

:::::{dropdown} Applies to model

```yaml
---
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
  serverless:
    security:
    elasticsearch:
    observability:
  product:
    ecctl:
    curator:
    apm_agent_dotnet:
    apm_agent_go:
    apm_agent_java:
    apm_agent_node:
    apm_agent_php:
    apm_agent_python:
    apm_agent_ruby:
    apm_agent_rum:
    edot_collector:
    edot_ios:
    edot_android:
    edot_dotnet:
    edot_java:
    edot_node:
    edot_php:
    edot_python:
    edot_cf_aws:
    edot_cf_azure:
---
```
:::::

## Look and feel

### Block

:::::{dropdown} Block examples

```{applies_to}
stack: preview 9.1
serverless: ga

apm_agent_dotnet: ga 1.0.0
apm_agent_java: beta 1.0.0
edot_dotnet: preview 1.0.0
edot_python:
edot_node: ga 1.0.0
elasticsearch: preview 9.0.0
security: removed 9.0.0
observability: deprecated 9.0.0
```
:::::

### Inline

:::::{dropdown} In text

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut libero diam. Mauris sed eleifend erat,
sit amet auctor odio. Donec ac placerat nunc. {applies_to}`stack: preview` Aenean scelerisque viverra lectus
nec dignissim. Vestibulum ut felis nec massa auctor placerat. Maecenas vel dictum.

- {applies_to}`elasticsearch: preview` Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut libero diam. Mauris sed eleifend erat, sit amet auctor odio. Donec ac placerat nunc.
- {applies_to}`observability: preview` Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut libero diam.
- {applies_to}`security: preview` Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ut libero diam. Mauris sed eleifend erat, sit amet auctor odio. Donec ac placerat nunc. Aenean scelerisque viverra lectus nec dignissim.

:::::

:::::{dropdown} Stack

| `applies_to`                               | result                               |
|--------------------------------------------|--------------------------------------|
| `` {applies_to}`stack: ` ``                | {applies_to}`stack: `                |
| `` {applies_to}`stack: preview` ``         | {applies_to}`stack: preview`         |
| `` {applies_to}`stack: preview 8.18` ``    | {applies_to}`stack: preview 8.18`    |
| `` {applies_to}`stack: preview 9.0` ``     | {applies_to}`stack: preview 9.0`     |
| `` {applies_to}`stack: preview 9.1` ``     | {applies_to}`stack: preview 9.1`     |
| `` {applies_to}`stack: preview 99.0` ``    | {applies_to}`stack: preview 99.0`    |
| `` {applies_to}`stack: ga` ``              | {applies_to}`stack: ga`              |
| `` {applies_to}`stack: ga 8.18` ``         | {applies_to}`stack: ga 8.18`         |
| `` {applies_to}`stack: ga 9.0` ``          | {applies_to}`stack: ga 9.0`          |
| `` {applies_to}`stack: ga 9.1` ``          | {applies_to}`stack: ga 9.1`          |
| `` {applies_to}`stack: ga 99.0` ``         | {applies_to}`stack: ga 99.0`         |
| `` {applies_to}`stack: beta` ``            | {applies_to}`stack: beta`            |
| `` {applies_to}`stack: beta 8.18` ``       | {applies_to}`stack: beta 8.18`       |
| `` {applies_to}`stack: beta 9.0` ``        | {applies_to}`stack: beta 9.0`        |
| `` {applies_to}`stack: beta 9.1` ``        | {applies_to}`stack: beta 9.1`        |
| `` {applies_to}`stack: beta 99.0` ``       | {applies_to}`stack: beta 99.0`       |
| `` {applies_to}`stack: deprecated` ``      | {applies_to}`stack: deprecated`      |
| `` {applies_to}`stack: deprecated 8.18` `` | {applies_to}`stack: deprecated 8.18` |
| `` {applies_to}`stack: deprecated 9.0` ``  | {applies_to}`stack: deprecated 9.0`  |
| `` {applies_to}`stack: deprecated 9.1` ``  | {applies_to}`stack: deprecated 9.1`  |
| `` {applies_to}`stack: deprecated 99.0` `` | {applies_to}`stack: deprecated 99.0` |
| `` {applies_to}`stack: removed` ``         | {applies_to}`stack: removed`         |
| `` {applies_to}`stack: removed 8.18` ``    | {applies_to}`stack: removed 8.18`    |
| `` {applies_to}`stack: removed 9.0` ``     | {applies_to}`stack: removed 9.0`     |
| `` {applies_to}`stack: removed 9.1` ``     | {applies_to}`stack: removed 9.1`     |
| `` {applies_to}`stack: removed 99.0` ``    | {applies_to}`stack: removed 99.0`    |
:::::

:::::{dropdown} Serverless

| `applies_to`                                    | result                                    |
|-------------------------------------------------|-------------------------------------------|
| `` {applies_to}`serverless: ` ``                | {applies_to}`serverless: `                |
| `` {applies_to}`serverless: preview` ``         | {applies_to}`serverless: preview`         |
| `` {applies_to}`serverless: ga` ``              | {applies_to}`serverless: ga`              |
| `` {applies_to}`serverless: beta` ``            | {applies_to}`serverless: beta`            |
| `` {applies_to}`serverless: deprecated` ``      | {applies_to}`serverless: deprecated`      |
| `` {applies_to}`serverless: removed` ``         | {applies_to}`serverless: removed`         |
:::::

### Badge rendering order

`applies_to` badges are displayed in a consistent order regardless of how they appear in your source files. This ensures users always see badges in a predictable hierarchy:

1. **Stack** - Elastic Stack
2. **Serverless** - Elastic Cloud Serverless offerings
3. **Deployment** - Deployment options (ECH, ECK, ECE, Self-Managed)
4. **ProductApplicability** - Specialized tools and agents (ECCTL, Curator, EDOT, APM Agents)
5. **Product (generic)** - Generic product applicability

Within the ProductApplicability category, EDOT and APM Agent items are sorted alphabetically for better scanning.

:::{note}
Inline applies annotations are rendered in the order they appear in the source file.
:::
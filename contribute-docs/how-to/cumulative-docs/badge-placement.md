# Badge usage and placement

:::{note}
This content is still in development.
If you have questions about how to write cumulative documentation while contributing,
reach out to **@elastic/docs** in the related GitHub issue or PR.
:::

As you continue contributing to documentation and more versions are released,
you might have questions about how to integrate `applies_to` badges in
cumulative documentation.

## Use cases

Depending on what you're trying to communicate, you can use the following patterns to represent
version and deployment type differences in your docs:

* **Pages**: Provide signals that a page applies to the reader.
* **Headings**: Provide signals about a section’s scope so a user can choose to read or skip it as needed.
* **Lists**: Identify features in a list of features that are exclusive to a specific context, or that were introduced in a specific version or comparing differing requirements, limits, and other simple, mirrored facts.
* **Definition lists**: Identify settings or options that are exclusive to a specific context, or that were introduced in a specific version.
* **Tabs**: Provide two sets of procedures when one or more steps in a process differs between contexts or versions. In most cases you should use [`applies-switch`](https://elastic.github.io/docs-builder/syntax/applies-switch/) instead of a generic [`tab-set`](https://elastic.github.io/docs-builder/syntax/tabs/).
* **Admonitions**: Draw attention to happy differences and basic clarifications.
* **Sibling pages**: When the information is too complex to be addressed with only the other content patterns.

## General placement principles

At a high level, you should follow these badge placement principles:

* Place badges where they're most visible but least disruptive to reading flow.
* Consider scanning patterns - readers often scan for relevant information.
* Ensure badges don't break the natural flow of content.
* Use consistent placement patterns within similar content types.
* Consider visual grouping - readers must naturally associate the badge with its corresponding content, no more, no less.

## Placement in specific elements

There are more specific guidelines on badge placement to follow when using specific elements.

### Page frontmatter

Use [`applies_to` in a page's frontmatter](https://elastic.github.io/docs-builder/syntax/applies#syntax) to provide signals that a page applies to the reader.

::::{warning}
Do **not** use [section-level](https://elastic.github.io/docs-builder/syntax/applies#section-level) or [inline annotations](https://elastic.github.io/docs-builder/syntax/applies#inline-level) with the page title.
::::

### Headings [headings]

Use [section annotations](https://elastic.github.io/docs-builder/syntax/applies#section-level) on the next line after a heading when the entire content between that heading and the next [heading](https://elastic.github.io/docs-builder/syntax/headings) of the same or higher level is version or product-specific.

For example, on the [Observability AI Assistant](https://www.elastic.co/docs/solutions/observability/observability-ai-assistant#choose-the-knowledge-base-language-model) page, all the content in this section is only applicable to Elastic Stack versions 9.1.0 and later.

::::{image} ./images/heading-correct.png
:screenshot:
:alt: Correct use of applies_to with headings
::::

% FOR THE REVIEWER: IS THIS TRUE?
% What do you think of allowing inline applies_to in headings as long as there is only one badge?
:::{warning}
Do **not** use [inline annotations](https://elastic.github.io/docs-builder/syntax/applies#inline-level) with headings.

::::{image} ./images/heading-incorrect.png
:screenshot:
:alt: Rendering error when using inline applies_to with headings
::::
:::

### Ordered and unordered lists [ordered-and-unordered-lists]

Reorganize content as needed so the `applies_to` badge is relevant to the entire contents of the list item.
This could mean distinguishing between deployment types, products, lifecycles, or versions.
Placing the badge at the beginning of the list item, allows the reader to scan the list for the item that is relevant to them.

For example, the [Alerting and action settings in Kibana](https://www.elastic.co/docs/reference/kibana/configuration-reference/alerting-settings) page lists how the default value for the `xpack.actions.preconfigured.<connector-id>.config.defaultModel` setting varies in Serverless/Stack and across versions.

::::{image} ./images/list-correct.png
:screenshot:
:alt:
::::

### Definition lists [definition-lists]

The recommended placement of `applies_to` badges in definition lists varies based on what part(s) of the list item relate to the badge.

#### If the badge is relevant to the entire contents of a list item, put it at the end of the term [definition-list-item-full]

This means using an inline annotation at the end of the same line as the term. For example, on the Kibana [Advanced settings](https://www.elastic.co/docs/reference/kibana/advanced-settings#kibana-banners-settings) page, the entire `banners:linkColor` option is only available in Elastic Stack 9.1.0 and later.

:::{image} ./images/definition-list-entire-item.png
:screenshot:
:alt: Correct use of applies_to with definition list item
:::

:::{warning}
Do **not** put the `applies_to` badge at the beginning or end of the definition if it relates to the entire contents of the item.

::::{image} ./images/definition-list-item-incorrect.png
:screenshot:
:alt: Incorrectly using inline applies_to with a definition list item
::::
:::

#### If the badge is only relevant to a portion of the definition, follow the appropriate placement guidelines for the elements used in the definition [definition-list-item-part]

This might include labeling just one of multiple paragraphs, or one item in an ordered or unordered list. For example, on the [Google Gemini Connector page](https://www.elastic.co/docs/reference/kibana/connectors-kibana/gemini-action-type#gemini-connector-configuration), the default model is different depending on the deployment type and version of the Elastic Stack. These differences should be called out with their own `applies_to` badges.

In this example, the `applies_to` badges should be at the beginning of each list item as described in [the guidelines for lists](#ordered-and-unordered-lists).

::::{image} ./images/definition-list-portion-correct.png
:screenshot:
:alt: Correctly using inline applies_to in a portion of a definition list item
::::

### Tables

The recommended placement in tables varies based on what part(s) of the table related to the `applies_to` label.

#### If the badge is relevant to the entire row, add the badge to the end of the first column [table-row]

Add the badge to the end of the first column to indicate that it applies to all cells in a row.

For example, the [Streaming Input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-streaming#_metrics_14) page includes a table that contains one setting per row and a new setting is added in 9.0.4.

::::{image} ./images/table-entire-row-correct.png
:screenshot:
:alt:
::::

In some cases it might be appropriate to add column dedicated to applicability,
but you should avoid adding specific Markdown real estate to the page layout and
causing existing tables with content from long before the base version,
for example Elastic Stack 9.0.0, look incomplete.

In the same example as above, creating a column dedicated to applicability would
likely take up unnecessary space and could cause confusion since the majority of
rows include content that has been available long before 9.0.0.

::::{image} ./images/table-entire-row-incorrect.png
:screenshot:
:alt:
::::

#### If the badge is relevant to one cell, add the badge to the cell it applies to [table-cell]

Add the badge to the end of the content in a cell to indicate that it applies to that one cell only.

For example, the [Collect application data](https://www.elastic.co/docs/solutions/observability/apm/collect-application-data#_capabilities) page includes a table that compares functionality across two methods for collecting APM data, and only one of the methods is in technical preview.

::::{image} ./images/table-one-cell-correct.png
:screenshot:
:alt:
::::
:::

:::{tip}
If the one cell that the badge applies to is in the first column, consider formatting the content
using something other than a table (for example, a definition list) to avoid confusion with the
[previous scenario](#table-row) in which adding the badge to the first column indicates that the
badge applies to the whole row.
:::

#### If the badge is relevant to part of a cell, follow the appropriate placement guidelines for the elements used in the cell [table-cell-part]

For example, the [Parse AWS VPC Flow Log](https://www.elastic.co/docs/reference/beats/filebeat/processor-parse-aws-vpc-flow-log) page includes new information relevant to 9.2.0 and later about a setting that already existed before 9.2.0. In this example, the `applies_to` badges should be at the beginning of each list item as described in [the guidelines for lists](#ordered-and-unordered-lists).

::::{image} ./images/table-part-of-cell-correct.png
:screenshot:
:alt:
::::
:::

% Reference: https://github.com/elastic/kibana/pull/229485/files#r2231856744
:::{tip}
If needed, break the contents of the cell into multiple lines using `<br>` to isolate the content you're labeling or consider not using a table to format the related content.
:::

### Tabs

When you need to show versions as tab titles, consider using [applies-switch](https://elastic.github.io/docs-builder/syntax/applies-switch) instead. The applies-switch component has built-in support for using applies-to metadata as tab titles and render these as badges.

### Admonitions

Admonitions support the `applies_to` property to indicate which products or versions the information applies to. Refer to the [admonitions documentation](https://elastic.github.io/docs-builder/syntax/admonitions#applies-to-information) for syntax details.

### Dropdowns

Dropdowns support the `applies_to` property to add a badge to the dropdown title. Refer to the [dropdowns documentation](https://elastic.github.io/docs-builder/syntax/dropdowns#with-applies_to-badge) for syntax details.

### Code blocks

To specify `applies_to` information for a code block, refer to [](example-scenarios.md#code-block).

### Images

To specify `applies_to` information for an image, refer to [](example-scenarios.md#screenshot).

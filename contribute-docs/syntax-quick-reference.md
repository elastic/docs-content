---
navigation_title: "Syntax quick reference"
---

# Syntax quick reference

Elastic documentation uses a custom implementation of [MyST Markdown](https://mystmd.org/) with extended syntax for directives, metadata, and tagging.

This page offers quick guidance on commonly used syntax elements. Elements are in alphabetical order.

For the full syntax reference, go to [elastic.github.io/docs-builder/syntax/](https://elastic.github.io/docs-builder/syntax/).


:::{tip}
Contributing to [elastic.co/guide](https://www.elastic.co/guide/index.html)? Refer to [Contribute to `elastic.co/guide` (Asciidoc)](asciidoc-guide.md).
:::

## Admonitions

Use admonitions to caution users, or to provide helpful tips or extra information.

::::::{dropdown} Types
These examples show the available admonition types, with rendered output followed by the Markdown syntax.

**Warning**

:::::{tab-set}

::::{tab-item} Output

:::{warning}
Users could permanently lose data or leak sensitive information.
:::

::::

::::{tab-item} Markdown

```markdown
:::{warning}
Users could permanently lose data or leak sensitive information.
:::
```

::::

:::::

**Important**

:::::{tab-set}

::::{tab-item} Output

:::{important}
Less dire than a warning. Users might encounter issues with performance or stability.
:::

::::

::::{tab-item} Markdown

```markdown
:::{important}
Less dire than a warning. Users might encounter issues with performance or stability.
:::
```

::::

:::::

**Note**

:::::{tab-set}

::::{tab-item} Output

:::{note}
Supplemental information that provides context or clarification.
:::

::::

::::{tab-item} Markdown

```markdown
:::{note}
Supplemental information that provides context or clarification.
:::
```

::::

:::::

**Tip**

:::::{tab-set}

::::{tab-item} Output

:::{tip}
Advice that helps users work more efficiently or make better choices.
:::

::::

::::{tab-item} Markdown

```markdown
:::{tip}
Advice that helps users work more efficiently or make better choices.
:::
```

::::

:::::

**Custom**

:::::{tab-set}

::::{tab-item} Output

:::{admonition} Special note
Custom admonition with custom label.
:::

::::

::::{tab-item} Markdown

```markdown
:::{admonition} Special note
Custom admonition with custom label.
:::
```

::::

:::::

::::::

**Best practices**
- ✅ Use custom admonitions as needed

**Avoid**
- ❌ Stacking admonitions
- ❌ Overloading a page with too many admonitions

For more details, refer to [Admonitions](https://elastic.github.io/docs-builder/syntax/admonitions).

---

## Anchors

A default anchor is automatically created for each [heading](#headings), in the form `#heading-text` (lowercase, with spaces converted to hyphens and special characters removed). To create a custom anchor, add it in square brackets at the end of a heading: `[my-better-anchor]`

:::{dropdown} Default anchor
```markdown
#### Hello world!
<!-- Auto-generated default anchor: #hello-world -->
```
:::


:::{dropdown} Custom anchor
```markdown
#### Hello world! [get-started]
```
:::

**Best practices**
- ✅ Create custom anchors for repeated structural headings like "Example request"

**Avoid**
- ❌ Including punctuation marks in custom anchors
- ❌ Defining custom anchors in text that is not a heading

For more details, refer to [Links](https://elastic.github.io/docs-builder/syntax/links#same-page-links-anchors).

---

## Applies to

Use `applies_to` metadata to tag content for specific contexts, for example whether a feature is available on certain products, versions, or deployment types.

This metadata enables you to write [cumulative documentation](how-to/cumulative-docs/index.md), because Elastic no longer publishes separate docs sets for every minor release.

**Example: Section tag**

::::{tab-set}

:::{tab-item} Output

#### Stack-only content
```{applies_to}
stack:
```

:::

:::{tab-item} Markdown

````markdown
# Stack-only content
```{applies_to}
stack:
```
````

:::

::::

For full syntax and more examples, refer to [the `applies_to` documentation](https://elastic.github.io/docs-builder/syntax/applies).

:::{tip}
The syntax for `applies_to` metadata differs depending on whether it's added at the [page level](https://elastic.github.io/docs-builder/syntax/applies/#page-level) (in frontmatter), [section level](https://elastic.github.io/docs-builder/syntax/applies/#section-level) (after a heading), or [inline](https://elastic.github.io/docs-builder/syntax/applies/#inline-level).
:::


:::{tip}
The `applies_to` tags are scope signals for readers, not comprehensive metadata. If a page contains general information that applies to all contexts, it doesn't need tags.
:::

**Best practices**
- ✅ Define a set of [page-level tags](https://elastic.github.io/docs-builder/syntax/applies#page-level) in a front matter block
- ✅ Add section-level tags in an `{applies_to}` [directive](https://elastic.github.io/docs-builder/syntax/applies#section-level) after a heading
- ✅ Indicate versions (`major.minor`) and release phases like `beta`
- ✅ Describe critical patch-level differences in prose rather than using version tags

**Avoid**

- ❌ Adding `applies_to` tags to general, broadly applicable content
- ❌ Overloading pages with repetitive tags

---

## Code blocks

Multi-line blocks for code, commands, configuration, and similar content. Use three backticks ` ``` ` on separate lines to start and end the block. For syntax highlighting, add a language identifier after the opening backticks.

::::{tab-set}

:::{tab-item} Output

```yaml
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
```

:::

:::{tab-item} Markdown

```markdown
    ```yaml
    server.host: "0.0.0.0"
    elasticsearch.hosts: ["http://localhost:9200"]
    ```
```

:::

::::


**Best practices**
- ✅ Include code blocks within lists or other block elements as needed
- ✅ Add language identifiers like `yaml`, `json`, `bash`

**Avoid**
- ❌ Placing code blocks in admonitions
- ❌ Using inline code formatting (single backticks) for multi-line content

For more details, refer to [Code](https://elastic.github.io/docs-builder/syntax/code).

---

## Code callouts

Inline annotations that highlight or explain specific lines in a code block.

### Explicit callout
To explicitly create a code callout, add a number marker in angle brackets (`<1>`, `<2>`, and so on) at the end of a line. Add the corresponding callout text below the code block, in a numbered list that matches the markers.

::::{tab-set}

:::{tab-item} Output

```json
{
  "match": {
    "message": "search text" <1>
  }
}
```
1. Searches the `message` field for the phrase "search text"

:::

:::{tab-item} Markdown

````markdown callouts=false
    ```json
    {
      "match": {
        "message": "search text" <1>
      }
    }
    ```
    1. Searches the `message` field for the phrase "search text"
````

:::

::::

### Automatic (comment-based) callout [magic-callout]
Add comments with `//` or `#` to automatically create callouts.

::::{tab-set}

:::{tab-item} Output

```json
{
  "match": {
    "message": "search text" // Searches the message field
  }
}
```

:::

:::{tab-item} Markdown

````markdown callouts=false
```json
{
  "match": {
    "message": "search text" // Searches the message field
  }
}
```
````

:::

::::

**Best practices**
- ✅ Keep callout text short and specific
- ✅ Use only one type of callout per code block (don't mix [explicit](#explicit-callout) and [automatic](#magic-callout))
- ✅ Make sure there's a corresponding list item for each explicit callout marker in a code block

**Avoid**
- ❌ Overusing callouts—they can impede readability

For more details, refer to [Code callouts](https://elastic.github.io/docs-builder/syntax/code#code-callouts).

---

## Comments

Use `%` to add single-line comments. Use HTML-style `<!--` and `-->` for multi-line comments.

::::{tab-set}

:::{tab-item} Output

% This is a comment
This is regular text

<!--
so much depends
upon
a multi-line
comment
-->
Regular text after multi-line comment

:::

:::{tab-item} Markdown

```markdown
    % This is a comment
    This is regular text

    <!--
    so much depends
    upon
    a multi-line
    comment
    -->
    Regular text after multi-line comment
```

:::

::::

**Best practices**
- ✅ Add a space after the `%` in single-line comments

**Avoid**
- ❌ Using `#` or `//` for comments (reserved for [magic callouts](#magic-callout))

---

## Dropdowns

Collapsible blocks for hiding and showing content.

::::::{tab-set}

:::::{tab-item} Output

::::{dropdown} Title or label
Collapsible content
::::

:::::

:::::{tab-item} Markdown

```markdown
:::{dropdown} Title or label
Collapsible content
:::
```

:::::

::::::

**Best practices**
- ✅ Use dropdowns for text, lists, images, code blocks, and tables
- ✅ Add `:open:` to auto-expand a dropdown by default

**Avoid**
- ❌ Using dropdowns for very long paragraphs or entire sections

For more details, refer to [Dropdowns](https://elastic.github.io/docs-builder/syntax/dropdowns).

---

## Headings
Headings mark the title of a page or section. To create a heading, add number signs `#` at the beginning of the line (one `#` for each heading level).

::::{tab-set}

:::{tab-item} Output

![Heading levels](images/headings.png)

:::

:::{tab-item} Markdown

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

:::

::::

**Best practices**
- ✅ Start every page with a Heading 1
- ✅ Use only one Heading 1 per page
- ✅ Define custom anchors for repeated headings

**Avoid**
- ❌ Using headings in tabs or dropdowns
- ❌ Going deeper than Heading 4

For more details, refer to [Headings](https://elastic.github.io/docs-builder/syntax/headings).

---

## Images
Standard Markdown image syntax: `![alt text]` followed by the image path in parentheses.

::::{tab-set}

:::{tab-item} Output

![Bear emerging from hibernation](images/bear.png)

:::

:::{tab-item} Markdown

```markdown
![Bear emerging from hibernation](images/bear.png)
```

:::

::::

**Best practices**
- ✅ Store images in a centralized directory
- ✅ Follow v3 [best practices for screenshots](how-to/cumulative-docs/badge-placement.md#images)
- ✅ Specify `:screenshot:` in an [image directive](https://elastic.github.io/docs-builder/syntax/images#screenshots) to add a border

**Avoid**
- ❌ Using lots of UI screenshots that create a maintenance burden
- ❌ Including confidential info or PII in an image
- ❌ Adding a drop shadow or torn edge effect

For more details, refer to [Images](https://elastic.github.io/docs-builder/syntax/images).

---


## Inline formatting
Elastic Docs v3 supports standard Markdown inline formatting.

| Output | Markdown |
| ------ | -------- |
| **bold** | \*\*bold\*\* |
| _italics_ | \_italics\_ |
| `monospace` | \`monospace\` |
| ~~strikethrough~~ | \~\~strikethrough\~\~ |
| \*escaped symbols\* | `\*escaped symbols\*` |

**Best practices**
- ✅ Use `_emphasis_` to introduce a term
- ✅ Use inline `code` in headings and other elements as needed

**Avoid**
- ❌ Overusing `**strong**` or `_emphasis_`—aim for readability

---

## Links

Standard Markdown links to doc pages, sections (anchors), or external content. Prefer absolute paths for links within the doc set.

:::{dropdown} Syntax
```markdown
    [link text](/absolute/file.md#anchor)
    [link text](https://external-site.com)
    [link text](other-repo://path/file.md)
    (#same-page-anchor)
```
:::

**Best practices**
- ✅ Use inline formatting in link text: `[**bold link**](https://elastic.github.io/docs-builder/syntax/bold-page)`
- ✅ Autogenerate link text from the page or section title: `[](https://elastic.github.io/docs-builder/syntax/use-title#section)`
- ✅ Define a custom [anchor](#anchors) by adding `[anchor-text]` at the end of a heading line

**Avoid**
- ❌ Using unclear, inaccessible link text like "click here" or "this"
- ❌ Including terminal punctuation in link text

For more details, refer to [Links](https://elastic.github.io/docs-builder/syntax/links).

---

## Lists

Standard Markdown ordered (numbered) and unordered (bulleted) lists. Indent with four spaces to nest paragraphs and other elements under a list item. Unordered lists can start with hyphens `-`, asterisks `*`, or plus signs `+`.

:::{dropdown} Syntax

  ```
      - Unordered item 1
      ····Paragraph within item 1
      - Unordered item 2
  ```

  ```
  1. Ordered item 1
  2. Ordered item 2
  ```
:::

**Best practices**
- ✅ Add code blocks, images, admonitions, and other content within a list item
- ✅ Nest lists, mixing ordered and unordered as needed
- ✅ Use parallel structure and phrasing in list items
- ✅ Capitalize only the first word of list items (sentence case)
- ✅ Use terminal punctuation consistently and only for complete sentences

**Avoid**
- ❌ Using lists solely for layout purposes
- ❌ Using lists for structured data or comparisons—use tables instead

For more details, refer to [Lists](https://elastic.github.io/docs-builder/syntax/lists).

---

## Navigation title

Optional [front matter](https://elastic.github.io/docs-builder/syntax/frontmatter) element that sets a custom title for navigation items. Appears in the left navigation (table of contents), breadcrumbs, and previous/next links. For information about page titles, refer to [Headings](#headings).

::::{tab-set}

:::{tab-item} Output

![Rendered nav title](images/nav-title.png)

:::

:::{tab-item} Markdown

Page front matter (YAML):

```yaml
---
navigation_title: "Minimalist identifier"
---
```

Page title (Markdown H1):

```markdown
# Full descriptive page title with product context
```

:::

::::


**Best practices**
- ✅ Use active phrasing and shorter forms
- ✅ Make sure the navigation title clearly identifies the page topic
- ✅ Omit product names that appear in the full H1 page title

**Avoid**
- ❌ Duplicating the H1 page title
- ❌ Using a long navigation title or lots of punctuation
- ❌ Abbreviating with periods or ellipses

For more details, refer to [Title](https://elastic.github.io/docs-builder/syntax/titles).

---

## Substitutions
Key-value pairs that define reusable variables. They help ensure consistency and enable short forms. To use a substitution (or "sub"), surround the key with double curly brackets: `{{variable}}`


### Define a sub

:::{dropdown} Syntax

In `docset.yml`:

```
subs:
  ccs: "cross-cluster search"
  ech: "Elastic Cloud Hosted"
  kib: "Kibana"
```
:::


### Use a sub

This example uses the sub defined in `docset.yml` above.

::::{tab-set}

:::{tab-item} Output

{{ech}} supports most standard {{kib}} settings.

:::

:::{tab-item} Markdown

In `myfile.md`:

```
{{ech}} supports most standard {{kib}} settings.
```

:::

::::

**Best practices**
- ✅ Check the global `docset.yml` file for existing product and feature name subs
- ✅ Use substitutions in code blocks by setting `subs=true`
- ✅ Define new page-specific substitutions as needed

**Avoid**
- ❌ Overriding a `docset.yml` sub by defining a page-level sub with the same key (causes build errors)
- ❌ Using substitutions for common words that don't need to be standardized

For more details, refer to [Substitutions](https://elastic.github.io/docs-builder/syntax/substitutions).

---

## Tabs

Block element that displays content in switchable tabs to help users find the right context (such as deployment type or programming language). [Synced tab groups](https://elastic.github.io/docs-builder/syntax/tabs#tab-groups) are supported.

:::::::{tab-set}

::::::{tab-item} Output

:::::{tab-set}

::::{tab-item} Tab 1 title
Tab 1 content
::::

::::{tab-item} Tab 2 title
Tab 2 content
::::

:::::

::::::

::::::{tab-item} Markdown

```markdown
::::{tab-set}

:::{tab-item} Tab 1 title
Tab 1 content
:::

:::{tab-item} Tab 2 title
Tab 2 content
:::

::::
```

::::::

:::::::

**Best practices**
- ✅ Use clear, descriptive tab labels
- ✅ Make sure all tabs have the same type of content and similar goals
- ✅ Keep tab content scannable and self-contained (don't make users switch tabs to follow steps or compare content)
- ✅ Include other block elements in tabs, like [admonitions](#admonitions)

**Avoid**
- ❌ Nesting tabs
- ❌ Splitting step-by-step procedures across tabs
- ❌ Using more than 6 tabs (use as few as possible)
- ❌ Using tabs in [dropdowns](#dropdowns)


For more details, refer to [Tabs](https://elastic.github.io/docs-builder/syntax/tabs).

---

## Tables

Standard table layout for structured data. Automatically scrolls horizontally if needed. The **header** row is optional.

::::{tab-set}

:::{tab-item} Output

| Header | Header |
| ------ | ------ |
| Data   | Info   |
| Info	 | Data   |

:::

:::{tab-item} Markdown

```markdown
| Header | Header |
| ------ | ------ |
| Data   | Info   |
| Info	 | Data   |
```

:::

::::

**Best practices**
- ✅ Use leading and trailing pipes for clarity
- ✅ Add spaces for readability (they're trimmed)
- ✅ Keep cell content scannable and parallel
- ✅ Use standard Markdown text alignment when necessary (`:-- --: :--:`)

**Avoid**
- ❌ Inserting block elements or multiple paragraphs in a table cell
- ❌ Using a table solely for position or spacing purposes

For more details, refer to [Tables](https://elastic.github.io/docs-builder/syntax/tables).

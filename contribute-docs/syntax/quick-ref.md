---
navigation_title: "Quick reference"
---

# Syntax quick reference

This page offers quick guidance on Elastic Docs v3 syntax, including usage tips. Elements are in alphabetical order. The [full syntax guide](https://elastic.github.io/docs-builder/syntax/index.md) provides implementation details.

## Admonitions

Use admonitions to caution users, or to provide helpful tips or extra information.

::::{dropdown} Types

These examples show the syntax first, followed by the rendered admonition.

 **Warning**

  ```markdown
      :::{warning}
      Users could permanently lose data or leak sensitive information.
      :::
  ```
  :::{warning}
  Users could permanently lose data or leak sensitive information.
  :::

  **Important**

  ```markdown
      :::{important}
      Less dire than a warning. Users might encounter issues with performance or stability.
      :::
  ```
  :::{important}
  Less dire than a warning. Users might encounter issues with performance or stability.
  :::

  **Note**
  ```markdown
      :::{note}
      Supplemental information that provides context or clarification.
      :::
  ```
  :::{note}
  Supplemental information that provides context or clarification.
  :::

  **Tip**
  ```markdown
      :::{tip}
      Advice that helps users work more efficiently or make better choices.
      :::
  ```
  :::{tip}
  Advice that helps users work more efficiently or make better choices.
  :::

  **Custom**
  ```markdown
      :::{admonition} Special note
      Custom admonition with custom label.
      :::
  ```
  :::{admonition} Special note
  Custom admonition with custom label.
  :::

::::

**DOs**<br>
✅ **Do:** Use custom admonitions as needed

**DON'Ts**<br>
❌ **Don't:** Stack admonitions<br>
❌ **Don't:** Overload a page with too many admonitions

[More details: Admonitions →](https://elastic.github.io/docs-builder/syntax/admonitions.md)
<br>
<br>

---

## Anchors

A default anchor is automatically created for each [heading](#headings), in the form `#heading-text` (hyphenated, lowercase, special characters and spaces trimmed). To create a custom anchor, add it in square brackets at the end of a heading: `[my-better-anchor]`

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

**DOs**<br>
✅ **Do:** Create custom anchors for repeated structural headings like "Example request"<br>

**DON'Ts**<br>
❌ **Don't:** Include punctuation marks in custom anchors<br>
❌ **Don't:** Define custom anchors in text that is not a heading

[More details: Links →](https://elastic.github.io/docs-builder/syntax/links.md#same-page-links-anchors)
<br>
<br>

---

## Applies to

Tags that identify technical contexts: the feature base (stack/serverless), deployments, and project types that a piece of content "applies to." Use `applies_to` tags to help users determine whether content is right for their deployments and configuration. These tags are a [version content pattern](../how-to/cumulative-docs/example-scenarios.md) in Elastic Docs v3.

**Example: Section tag**

:::{dropdown} Syntax
````markdown
# Stack-only content
```{applies_to}
stack:
```
````
:::

:::{dropdown} Output
#### Stack-only content
```{applies_to}
stack:
```
:::

For full syntax and more examples, see [](https://elastic.github.io/docs-builder/syntax/applies.md).

<!--
:::{tip}
The `applies_to` tags are scope signals for readers, not comprehensive metadata. If a page contains general information that applies to all contexts, it doesn't need tags.
:::
-->

% TODO restore details when guidance has settled

**DOs**<br>
✅ **Do:** Define a set of [page-level tags](https://elastic.github.io/docs-builder/syntax/applies.md#page-level) in a front matter block<br>
✅ **Do:** Add section-level tags in an `{applies_to}` [directive](https://elastic.github.io/docs-builder/syntax/applies.md#section-level) after a heading<br>
✅ **Do:** Indicate versions (`major.minor` with an optional `[.patch]`) and release phases like `beta`

**DON'Ts**<br>
❌ **Don't:** Include `applies_to` tags in admonitions<br>
❌ **Don't:** Add `applies_to` tags to general, broadly applicable content<br>
❌ **Don't:** Use `Coming (x.x.x)` tags, except in special cases (don't pre-announce features)
<br>
<br>

---

## Code blocks

Multi-line blocks for code, commands, configuration, and similar content. Use three backticks ` ``` ` on separate lines to start and end the block. For syntax highlighting, add a language identifier after the opening backticks.

:::{dropdown} Syntax
```markdown
    ```yaml
    server.host: "0.0.0.0"
    elasticsearch.hosts: ["http://localhost:9200"]
    ```
```
:::

:::{dropdown} Output
```yaml
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
```
:::


**DOs**<br>
✅ **Do:** Include code blocks within lists or other block elements as needed<br>
✅ **Do:** Add language identifiers like `yaml`, `json`, `bash`

**DON'Ts**<br>
❌ **Don't:** Place code blocks in admonitions<br>
❌ **Don't:** Use inline code formatting (single backticks) for multi-line content

[More details: Code →](https://elastic.github.io/docs-builder/syntax/code.md)
<br>
<br>

---

## Code callouts

Inline annotations that highlight or explain specific lines in a code block.

### Explicit callout
To explicitly create a code callout, add a number marker in angle brackets (`<1>`, `<2>`, ...) at the end of a line. Add the corresponding callout text below the code block, in a numbered list that matches the markers.

:::{dropdown} Syntax

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

:::{dropdown} Output

```json
{
  "match": {
    "message": "search text" <1>
  }
}
```
1. Searches the `message` field for the phrase "search text"<br>
:::

### Magic (comment-based) callout [magic-callout]
Add comments with `//` or `#` to magically create callouts.

:::{dropdown} Syntax
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

:::{dropdown} Output

```json
{
  "match": {
    "message": "search text" // Searches the message field
  }
}
```
:::

**DOs**<br>
✅ **Do:** Keep callout text short and specific<br>
✅ **Do:** Use only one type of callout per code block (don't mix [explicit](#explicit-callout) and [magic](#magic-callout))<br>
✅ **Do:** Make sure there's a corresponding list item for each explicit callout marker in a code block

**DON'Ts**<br>
❌ **Don't:** Overuse callouts &mdash; they can impede readability

[More details: Code callouts→](https://elastic.github.io/docs-builder/syntax/code.md#code-callouts)
<br>
<br>

---

## Comments

Use `%` to add single-line comments. Use HTML-style `<!--` and `-->` for multi-line comments.

:::{dropdown} Syntax
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

:::{dropdown} Output
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

**DOs**<br>
✅ **Do:** Add a space after the `%` in single-line comments

**DON'Ts**<br>
❌ **Don't:** Use `#` or `//` for comments (reserved for [magic callouts](#magic-callout))
<br>
<br>

---

## Dropdowns

Collapsible blocks for hiding and showing content.

::::{dropdown} Syntax
```markdown
    :::{dropdown} Title or label
    Collapsible content
    :::
```
::::

::::{dropdown} Output
:::{dropdown} Title or label
Collapsible content
:::
::::

**DOs**<br>
✅ **Do:** Use dropdowns for text, lists, images, code blocks, and tables<br>
✅ **Do:** Add `:open:` to auto-expand a dropdown by default

**DON'Ts**<br>
❌ **Don't:** Use dropdowns for very long paragraphs or entire sections

[More details: Dropdowns →](https://elastic.github.io/docs-builder/syntax/dropdowns.md)
<br>
<br>

---

## Headings
Title of a page or a section. To create a heading, add number signs `#` at the beginning of the line (one `#` for each heading level).

:::{dropdown} Syntax
```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```
:::

::::{dropdown} Output
:::{image} images/headings.png
:screenshot:
:alt: Heading levels
:width: 300px
:::

::::

**DOs**<br>
✅ **Do:** Start every page with a Heading 1<br>
✅ **Do:** Use only one Heading 1 per page<br>
✅ **Do:** Define custom anchors for repeated headings

**DON'Ts**<br>
❌ **Don't:** Use headings in tabs or dropdowns<br>
❌ **Don't:** Go deeper than Heading 4

[More details: Headings →](https://elastic.github.io/docs-builder/syntax/headings.md)
<br>
<br>

---

## Images
Standard Markdown images: `[alt text]` in square brackets, followed by the image path in parentheses.

:::{dropdown} Syntax
```markdown
![Bear emerging from hibernation](images/bear.png)
```
:::

:::{dropdown} Output
![Bear emerging from hibernation](images/bear.png)
:::

**DOs**<br>
✅ **Do:** Store images in a centralized directory<br>
✅ **Do:** Follow v3 [best practices for screenshots](../how-to/cumulative-docs/badge-placement.md#images)<br>
✅ **Do:** Specify `:screenshot:` in an [image directive](https://elastic.github.io/docs-builder/syntax/images.md#screenshots) to add a border

**DON'Ts**<br>
❌ **Don't:** Use lots of UI screenshots that create a maintenance burden<br>
❌ **Don't:** Include confidential info or PII in an image<br>
❌ **Don't:** Add a drop shadow or torn edge effect

[More details: Images →](https://elastic.github.io/docs-builder/syntax/images.md)
<br>
<br>

---


## Inline formatting
Elastic Docs v3 supports standard Markdown inline formatting.

`_emphasis_` &nbsp;&nbsp;&nbsp; _italics_ <br>
`**strong**` &nbsp;&nbsp;&nbsp;**bold**  <br>
\` `monospace` \` &nbsp;&nbsp;&nbsp; `inline code` (single backticks) <br>
`~~strikethrough~~` &nbsp;&nbsp;&nbsp; ~~strikethrough~~ <br>
`\* escaped` &nbsp;&nbsp;&nbsp; \* escaped character

**DOs**<br>
✅ **Do:** Use `_emphasis_` to introduce a term<br>
✅ **Do:** Use inline `code` in headings and other elements as needed

**DON'Ts**<br>
❌ **Don't:** Overuse `**strong**` or `_emphasis_` &mdash; aim for readability
<br>
<br>

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

**DOs**<br>
✅ **Do:** Use inline formatting in link text: `[**bold link**](https://elastic.github.io/docs-builder/syntax/bold-page.md)`<br>
✅ **Do:** Autogenerate link text from the page or section title: `[](https://elastic.github.io/docs-builder/syntax/use-title.md#section)`<br>
✅ **Do:** Define a custom [anchor](#anchors) by adding `[anchor-text]` at the end of a heading line

**DON'Ts**<br>
❌ **Don't:** Use unclear, inaccessible link text like "click here" or "this"<br>
❌ **Don't:** Include terminal punctuation in link text

[More details: Links →](https://elastic.github.io/docs-builder/syntax/links.md)
<br>
<br>

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

**DOs** <br>
✅ **Do:** Add code blocks, images, admonitions, and other content within a list item<br>
✅ **Do:** Nest lists, mixing ordered and unordered as needed<br>
✅ **Do:** Use parallel structure and phrasing in list items<br>
✅ **Do:** Capitalize only the first word of list items (sentence case)<br>
✅ **Do:** Use terminal punctuation consistently and only for complete sentences

**DON'Ts** <br>
❌ **Don't:** Use lists solely for layout purposes <br>
❌ **Don't:** Use lists for structured data or comparisons — use tables instead

[More details: Lists →](https://elastic.github.io/docs-builder/syntax/lists.md)
<br>
<br>

---

## Navigation title

Optional [front matter](https://elastic.github.io/docs-builder/syntax/frontmatter.md) element that sets a custom title for docs navigation features: appears in the left nav (table of contents), breadcrumbs, and previous/next links. Compare [headings](#headings) (H1 = page title).

:::{dropdown} Syntax

Page front matter (yaml):

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

:::{dropdown} Output

![Rendered nav title](images/nav-title.png)

:::


**DOs**<br>
✅ **Do:** Use active phrasing and shorter forms<br>
✅ **Do:** Make sure the navigation title clearly identifies the page topic<br>
✅ **Do:** Omit product names that appear in the full H1 page title

**DON'Ts**<br>
❌ **Don't:** Duplicate the H1 page title<br>
❌ **Don't:** Use a long navigation title or lots of punctuation<br>
❌ **Don't:** Abbreviate with periods or ellipses

[More details: Title →](https://elastic.github.io/docs-builder/syntax/titles.md)
<br>
<br>

---

## Substitutions
Key-value pairs that define reusable variables. They help ensure consistency and enable short forms. To use a substitution (or "sub"), surround the key with curly brackets: `{{variable}}`<br>

% TODO: link to our global docset.yml?

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

:::{dropdown} Syntax

In `myfile.md`:

```
{{ech}} supports most standard {{kib}} settings.
```
:::

:::{dropdown} Output
% TODO replace with actual subs once _docset.yml is updated

Elastic Cloud Hosted supports most standard Kibana settings.
:::

**DOs** <br>
✅ **Do:** Check the global `docset.yml` file for existing product and feature name subs<br>
✅ **Do:** Use substitutions in code blocks by setting `subs=true`  <br>
✅ **Do:** Define new page-specific substitutions as needed

**DON'Ts**<br>
❌ **Don't:** Override a `docset.yml` sub by defining a page-level sub with the same key (causes build errors)<br>
❌ **Don't:** Use substitutions for common words that don't need to be standardized

[More details: Substitutions →](https://elastic.github.io/docs-builder/syntax/substitutions.md)
<br>
<br>

---

## Tabs

Block element that displays content in switchable tabs to help users zero in on the right context (such as a deployment or language). [Synced tab groups](https://elastic.github.io/docs-builder/syntax/tabs.md#tab-groups) are supported.

:::::{dropdown} Syntax
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
:::::

:::::{dropdown} Output
::::{tab-set}

:::{tab-item} Tab 1 title
Tab 1 content
:::

:::{tab-item} Tab 2 title
Tab 2 content
:::

::::
:::::

**DOs**<br>
✅ **Do:** Use clear, descriptive tab labels<br>
✅ **Do:** Make sure all tabs have the same type of content and similar goals<br>
✅ **Do:** Keep tab content scannable and self-contained (don't make users switch tabs to follow steps or compare content)<br>
✅ **Do:** Include other block elements in tabs, like [admonitions](#admonitions)

**DON'Ts**<br>
❌ **Don't:** Nest tabs<br>
❌ **Don't:** Split step-by-step procedures across tabs<br>
❌ **Don't:** Use more than 6 tabs (use as few as possible)<br>
❌ **Don't:** Use tabs in [dropdowns](#dropdowns)


[More details: Tabs →](https://elastic.github.io/docs-builder/syntax/tabs.md)
<br>
<br>

---

## Tables

Standard table layout for structured data. Automatically scrolls horizontally if needed. The **header** row is optional.

:::{dropdown} Syntax
```markdown
    | Header | Header |
    | ------ | ------ |
    | Data   | Info   |
    | Info	 | Data   |
```
:::

:::{dropdown} Output
| Header | Header |
| ------ | ------ |
| Data   | Info   |
| Info	 | Data   |
:::

**DOs**<br>
✅ **Do:** Use leading and trailing pipes for clarity<br>
✅ **Do:** Add spaces for readability (they're trimmed)<br>
✅ **Do:** Keep cell content scannable and parallel<br>
✅ **Do:** Use standard Markdown text alignment when necessary (`:-- --: :--:`)

**DON'Ts**<br>
❌ **Don't:** Insert block elements or multiple paragraphs in a table cell<br>
❌ **Don't:** Use a table solely for position or spacing purposes

[More details: Tables →](https://elastic.github.io/docs-builder/syntax/tables.md)

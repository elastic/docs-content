# Headings

You create a heading by adding number signs `#` in front of a word or phrase. The number of number signs you use should correspond to the heading level. For example, to create a heading level three `<h3>`, use three number signs (e.g., `### My Header`).

## Basics

::::{tab-set}

:::{tab-item} Output

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

:::

:::{tab-item} Markdown

```markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
##### Heading 5
###### Heading 6

```

:::

::::

:::{note}

- Every page has to start with a level 1 heading.
- You should use only one level 1 heading per page.
- Headings inside directives like tabs or dropdowns causes the table of contents indicator to behave unexpectedly.
- If you are using the same heading text multiple times you should use a custom [anchor link](#anchor-links) to avoid conflicts.

:::

## Anchor Links

By default, the anchor links are generated based on the heading text.
You will get a hyphened, lowercase, alphanumeric version of any string you please, with any [diacritics](https://en.wikipedia.org/wiki/Diacritic) removed, whitespace and dashes collapsed, and whitespace trimmed.

### Default Anchor Links

::::{tab-set}

:::{tab-item} Output

#### Hello-World

:::

:::{tab-item} Markdown

```markdown

#### Hello-World

```

:::

::::


### Custom Anchor Links

You can also specify a custom anchor link using the following syntax.

::::{tab-set}

:::{tab-item} Output

#### Heading [custom-anchor]

:::

:::{tab-item} Markdown

```markdown

#### Heading [custom-anchor]

```

:::

::::

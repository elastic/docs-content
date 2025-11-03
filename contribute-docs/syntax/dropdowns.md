# Dropdowns

Dropdowns allow you to hide and reveal content on user interaction. By default, dropdowns are collapsed. This hides content until a user clicks the title of the collapsible block.

## Basic dropdown


:::::{tab-set}

::::{tab-item} Output

:::{dropdown} Dropdown Title
Dropdown content
:::

::::

::::{tab-item} Markdown
```markdown
:::{dropdown} Dropdown Title
Dropdown content
:::
```
::::

:::::

## Open by default

You can specify that the dropdown content should be visible by default. Do this by specifying the `open` option. Users can collapse content by clicking on the dropdown title.

:::::{tab-set}

::::{tab-item} Output

:::{dropdown} Dropdown Title
:open:
Dropdown content
:::

::::

::::{tab-item} Markdown
```markdown
:::{dropdown} Dropdown Title
:open:
Dropdown content
:::
```
::::

:::::

## With applies_to badge

:::{include} _snippets/applies-to-dropdowns.md
:::

## Multiple applies_to definitions

You can specify multiple `applies_to` definitions using YAML object notation with curly braces `{}`. This is useful when content applies to multiple deployment types or versions simultaneously.

:::::{tab-set}

::::{tab-item} Output

:::{dropdown} Dropdown Title
:applies_to: { ece:, ess: }
Dropdown content for ECE and ECH
:::

::::

::::{tab-item} Markdown
```markdown
:::{dropdown} Dropdown Title
:applies_to: { ece:, ess: }
Dropdown content for ECE and ECH
:::
```
::::

:::::

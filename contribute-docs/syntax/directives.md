# Directives

Directives extend Markdown with additional features:

```markdown
:::{note}
This is a callout box that stands out from regular text.
:::
```

How directive syntax works:
- `:::` opens and closes the directive block
- `{note}` is the directive type (always in curly braces)
- Content inside is regular Markdown

## Adding options

```markdown
:::{image} screenshot.png
:alt: Dashboard overview <1>
:width: 600px
:::
```

1. Options start with `:` and appear after the opening line.

## Adding arguments

```markdown
:::{include} shared-content.md
:::
```

The argument comes right after the directive name.

## Nesting directives

To nest directives, add more colons to the outer directive:

```markdown
::::{note}
Outer content

:::{hint}
Inner content
:::

More outer content
::::
```

Use four colons (`::::`) for the outer directive and three (`:::`) for the inner one. Need to nest deeper? Keep adding colons.

## Exception: Literal blocks

Code blocks and [`applies_to` blocks](applies.md) use backticks instead of colons to prevent content from being processed as Markdown:

````markdown
```js
const x = 1;
```
````

## Available directives

The following directives are available:

- [Admonitions](admonitions.md) - Callouts and warnings
- [Code blocks](code.md) - Syntax-highlighted code
- [CSV include](csv-include.md) - Render CSV files as tables
- [Diagrams](diagrams.md) - Visual diagrams and charts
- [Dropdowns](dropdowns.md) - Collapsible content
- [Images](images.md) - Enhanced image handling
- [Include](file_inclusion.md) - Include content from other files
- [Math](math.md) - Mathematical expressions and equations
- [Settings](automated_settings.md) - Configuration blocks
- [Stepper](stepper.md) - Step-by-step content
- [Tabs](tabs.md) - Tabbed content organization
- [Tables](tables.md) - Data tables
- [Version blocks](version-variables.md) - API version information
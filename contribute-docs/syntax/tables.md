# Tables

A table is an arrangement of data with rows and columns. Each row consists of cells containing arbitrary text in which inlines are parsed, separated by pipes `|`. The rows of a table consist of:

* a single header row
* a delimiter row separating the header from the data
* zero or more data rows

## Basic Table

::::{tab-set}

:::{tab-item} Output
| Country | Capital         |
| ------- | --------------- |
| USA     | Washington D.C. |
| Canada  | Ottawa          |
| Mexico  | Mexico City     |
| Brazil  | Brasília        |
| UK      | London          |
:::

:::{tab-item} Markdown
```markdown
| Country | Capital         |
| ------- | --------------- |
| USA     | Washington D.C. |
| Canada  | Ottawa          |
| Mexico  | Mexico City     |
| Brazil  | Brasília        |
| UK      | London          |
:::

::::

:::{note}

* A leading and trailing pipe is recommended for clarity of reading
* Spaces between pipes and cell content are trimmed
* Block-level elements cannot be inserted in a table

:::


## Table without header

::::{tab-set}

:::{tab-item} Output
|                   |         |
|-------------------|---------|
| **Country**       | Austria |
| **Capital**       | Vienna  |
| **Calling code**  | +43     |
| **ISO 3166 code** | AT      |
:::

:::{tab-item} Markdown
```markdown
|                   |         |
|-------------------|---------|
| **Country**       | Austria |
| **Capital**       | Vienna  |
| **Calling code**  | +43     |
| **ISO 3166 code** | AT      |
```
:::

::::

## Responsive Table

Every table is responsive by default. The table will automatically scroll horizontally when the content is wider than the viewport.

::::{tab-set}

:::{tab-item} Output
| Product Name | Price ($) | Stock  | Category  | Rating  | Color    | Weight (kg) | Warranty (months) |
|--------------|-----------|--------|-----------|---------|----------|-------------|-------------------|
| Laptop Pro   | 1299.99   | 45     | Computer  | 4.5     | Silver   | 1.8         | 24                |
| Smart Watch  | 299.99    | 120    | Wearable  | 4.2     | Black    | 0.045       | 12                |
| Desk Chair   | 199.50    | 78     | Furniture | 4.8     | Gray     | 12.5        | 36                |
:::

:::{tab-item} Markdown
```markdown
| Product Name | Price ($) | Stock  | Category  | Rating  | Color    | Weight (kg) | Warranty (months) |
|--------------|-----------|--------|-----------|---------|----------|-------------|-------------------|
| Laptop Pro   | 1299.99   | 45     | Computer  | 4.5     | Silver   | 1.8         | 24                |
| Smart Watch  | 299.99    | 120    | Wearable  | 4.2     | Black    | 0.045       | 12                |
| Desk Chair   | 199.50    | 78     | Furniture | 4.8     | Gray     | 12.5        | 36                |
:::
```

::::

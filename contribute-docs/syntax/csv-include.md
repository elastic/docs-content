# CSV files

The `{csv-include}` directive allows you to include and render CSV files as formatted tables in your documentation. The directive automatically parses CSV content and renders it using the standard table styles defined in `table.css`.

## Usage

:::::{tab-set}

::::{tab-item} Output

:::{csv-include} /contribute-docs/_snippets/sample-data.csv
:caption: Sample user data from the database
:::

::::

::::{tab-item} Markdown

```markdown
:::{csv-include} _snippets/sample-data.csv
:::
```

::::

:::::

## Options

The CSV file directive supports several options to customize the table rendering:

### Caption

Add a descriptive caption above the table:

```markdown
:::{csv-include} _snippets/sample-data.csv
:caption: Sample user data from the database
:::
```

### Custom separator

Specify a custom field separator (default is comma):

```markdown
:::{csv-include} _snippets/sample-data.csv
:separator: ;
:::
```

### Performance limits

The directive includes built-in performance limits to handle large files efficiently:

- **Row limit**: Maximum of 25,000 rows will be displayed
- **Column limit**: Maximum of 10 columns will be displayed  
- **File size limit**: Maximum file size of 10MB

## Performance considerations

The CSV directive is optimized for large files:

- Files are processed using streaming to avoid loading everything into memory
- Built-in size validation prevents processing of files that exceed 10MB
- Row and column limits protect against accidentally rendering massive tables
- Warning messages are displayed when limits are exceeded

For optimal performance with large CSV files, consider:
- Breaking very large files into smaller, more manageable chunks

---
navigation_title: Elastic Docs Utilities
---

# Elastic Docs Utilities

The Elastic Docs Utilities extension for Visual Studio Code and compatible IDEs provides autocompletion for Elastic Docs' Markdown, along with other features for authoring Elastic documentation.

:::{image} images/elastic-docs-vscode.gif
:screenshot:
:alt: Elastic Docs Utilities extension demo
:width: 800px
:::

## Installation

To install the extension:

1. Open the Visual Studio Marketplace or the **Extensions** view in your editor.
2. Search for `Elastic Docs Utilities`.
3. Select **Install** to add the extension to your editor.

:::{tip}
The extension is also available for editors that support the Open VSX Registry, like Cursor.
:::

## Availability

You can use the extension in the following ways:

- Working [locally](locally.md) in the Visual Studio Code desktop application.
- Working [in the browser](on-the-web.md) in Visual Studio Code web editors.

## Features

Elastic Docs Utilities provides the following features for authoring Elastic documentation.

### Syntax highlighting

The extension adds syntax highlighting for directives, parameters, roles, substitution variables, and mutation operators that works alongside standard Markdown highlighting.

### Autocompletion

The extension autocompletes standard and inline directives as you type. When you add frontmatter to your documents, it suggests valid field names and values. 

The extension also provides autocompletion for inline roles like `{icon}`, `{kbd}`, `{applies_to}`, and `{subs}`. Type `{{` to see substitution variables from your `docset.yml` files and document frontmatter, and type `|` after any variable to view available mutation operators for text and version transformations.

### Validation and diagnostics

The extension validates your frontmatter fields against the schema and provides real-time syntax validation for directives, showing red underlines and hover cards when it detects errors. It also warns you when you're using literal values that should be replaced with substitution variables, helping maintain consistency across your documentation.

### Tooltips

Hover over existing `{{variable}}` references to see their full values and mutation transformations. When variables use mutation operators, you can view step-by-step transformation results in the preview.

## Substitution variables

The extension supports autocompletion for substitution variables defined in `docset.yml` files and document frontmatter (`sub:` field). These variables can be used throughout your Markdown files with the `{{variable}}` syntax.

### Substitution validation and quick fixes

The extension automatically detects when you're using literal values that can be replaced with substitution variables. For example, the extension shows a warning when you type "APM" directly in your content, suggesting you use `{{product.apm}}` instead.

When the extension detects a literal value that should be replaced, you can:

- Click the lightbulb icon that appears.
- Use the **Quick Fix** menu (Ctrl+. or Cmd+. on macOS)
- Hover over the warning and click **Quick Fix**.

The extension automatically replaces the literal text with the correct substitution variable syntax. This helps maintain consistency across your documentation and makes it easier to update product names and other values globally.



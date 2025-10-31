# File inclusion

File inclusion is useful for
- including entire pages in a content set (usually done in the `docset.yml` file)
- breaking files into smaller units and including them where appropriate

If there are portions of content that are relevant to multiple pages, you can inject content from another file into any given MD file using the `include` directive.

:::{note}
Files to be included must live in a `_snippets` folder to be considered a snippet file. This folder can live anywhere. 
:::

### Syntax

```markdown
:::{include} _snippets/reusable-snippet.md
:::
```

:::{include} _snippets/reusable-snippet.md
:::

#### Linking to snippets with custom anchors

To link to a heading with a [custom anchor (ID)](./headings.md#custom-anchor-links) defined in a snippet, target the parent file + anchor. 

For example:

```markdown
[my favorite esql function](parent-file.md#id-from-included-snippet)
```

### Asciidoc syntax

```asciidoc
include::shared-monitor-config.asciidoc[]
```

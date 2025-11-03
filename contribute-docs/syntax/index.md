# Syntax guide

Learn about the custom Markdown syntax used in Elastic documentation.

## Quick reference

Refer to the [quick reference](quick-ref.md) for a condensed syntax cheat sheet.

## How it works

Elastic Docs V3 uses a custom implementation of [MyST](https://mystmd.org/) (Markedly Structured Text), which extends standard Markdown with directive syntax.

If you know [Markdown](https://commonmark.org), you already know most of what you need. If not, the CommonMark project offers a [10-minute tutorial](https://commonmark.org/help/). 

When you need more than basic Markdown, you can use [directives](directives.md) to add features like callouts, tabs, and diagrams.

## GitHub Flavored Markdown support

V3 supports some GitHub Flavored Markdown extensions:

**Supported:**
- Tables (basic pipe syntax)
- Strikethrough with `~~text~~` (renders as ~~text~~)

**Not supported:**
- Task lists
- Automatic URL linking: https://www.elastic.co
  - Links must use standard Markdown syntax: [Elastic](https://www.elastic.co)
- Using a subset of HTML

## Legacy asciidoc syntax

This syntax guide covers Markdown for [elastic.co/docs](https://elastic.co/docs).

If you need to work on [elastic.co/guide](https://elastic.co/guide) pages, which are written in AsciiDoc,refer to [Contribute to legacy documentation](../legacy-docs.md).
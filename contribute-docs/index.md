---
navigation_title: Contribute to the docs
---

# Contribute to Elastic documentation

In April 2025, Elastic migrated to a new documentation system at [elastic.co/docs](https://www.elastic.co/docs), using Markdown and the [`docs-builder`](https://elastic.github.io/docs-builder/) toolchain, which coincided with the release of {{stack}} 9.0.0, {{ece}} 4.0.0, and {{eck}} 3.0.0.

This documentation site includes docs for:
- {{stack}} 9.x
- {{ece}} 4.x
- {{eck}} 3.x
- {{ech}}
- {{serverless-full}}

Refer to [versioning and availability](/get-started/versioning-availability.md) to learn more.

This documentation is [**cumulative**](how-to/cumulative-docs/index.md): a new set of docs is not published for every minor release. Instead, each page stays valid over time and incorporates version-specific changes.

:::{tip}
To learn more about the new docs UX, read [how to use the documentation](/get-started/howto-use-the-docs.md).
:::

## Contribute to `elastic.co/docs` (Markdown)

|System|What it covers|Published at|Format|How to contribute
|----|----|----|----|----|----|
|Main docs|Guides, troubleshooting, release notes, etc.|[elastic.co/docs](https://www.elastic.co/docs)|Markdown|- [On the web](on-the-web.md) (quick edits) <br> - [Locally](locally.md) (complex changes) <br> - [Syntax guide](syntax/index.md)|
|API references|Elastic REST APIs|[elastic.co/docs/api](https://www.elastic.co/docs/api/)|[OpenAPI](https://swagger.io/specification/)|[Contribute to API docs](api-docs/index.md)|

:::{note}
If you need to update documentation in both the MarkDown and Asciidoc systems, you'll need two separate PRs. Refer to [Updating docs in both systems](asciidoc-guide.md#updating-docs-in-both-systems).
:::

## Report issues or request features

|Issue type|Where to report|
|----|----|
|Documentation|- [Open a docs issue](https://github.com/elastic/docs-content/issues/new?template=internal-request.yaml) or [fix it yourself](locally.md) <br> - Elastic employees can use the [internal repo](https://github.com/elastic/docs-content-internal/issues/new/choose)|
|`docs-builder`|- [Bug report](https://github.com/elastic/docs-builder/issues/new?template=bug-report.yaml) <br> - [Discussion](https://github.com/elastic/docs-builder/discussions)|

## Contribute to `elastic.co/guide` (Asciidoc)

|System|What it covers|Published at|Format/toolchain|How to contribute
|----|----|----|----|----|----|
|`elastic.co/guide` (Asciidoc)|Elastic docs & API references for 8.x and earlier|[elastic.co/guide](https://www.elastic.co/guide/index.html)|Asciidoc|[Contribute to the Asciidoc docs](./asciidoc-guide.md)|

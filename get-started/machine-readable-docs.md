---
navigation_title: Machine-readable docs
applies_to:
  serverless:
  stack:
products:
  - id: elastic-stack
description: "Access Elastic documentation as Markdown, bulk archives, a remote MCP server, or a CLI. Pick the method that fits your tool or workflow."
---

# Access Elastic Docs in machine-readable formats

The Elastic Docs website is one way to access Elastic Docs. The same content is also available as per-page Markdown, bulk archives, through a remote Model Context Protocol (MCP) server, and from the command line. Use this page to select the access method that best fits your tool.

All channels on this page cover the current documentation set: {{stack}} 9.0 and later, and {{serverless-full}}. Documentation for earlier versions at `elastic.co/guide` is not included. Refer to [](versioning-availability.md) for details.

| What you get | URL | Format |
|---|---|---|
| [Per-page Markdown](#single-page-markdown) | `https://www.elastic.co/docs/<path>.md` | `text/markdown` |
| [Documentation index](#llms-txt) | `https://www.elastic.co/docs/llms.txt` | Plain text |
| [Markdown bundle](#llm-zip) | `https://www.elastic.co/docs/llm.zip` | ZIP archive |
| [Structured bundle](#okf-zip) | `https://www.elastic.co/docs/okf.zip` | ZIP archive |
| [Docs MCP server](#docs-mcp-server) | `https://www.elastic.co/docs/_mcp/` | Streamable HTTP |
| [Elastic CLI](#elastic-cli) | `elastic docs search`, `ask`, `read` | CLI |

## Get a single page as Markdown [single-page-markdown]

Every page on `elastic.co/docs` has a Markdown equivalent. This is a machine-readable rendition, not the MyST authoring source. The rendition includes:

- Generated frontmatter: `title`, `description`, `url`, `products`, `applies_to`
- Substitutions resolved (for example, `{{stack}}` becomes `Elastic Stack`)
- Directives flattened to prose or CommonMark
- All links rewritten to absolute `https://www.elastic.co/docs/...` HTML URLs

To find the Markdown source, use **Edit this page** on the page you're viewing.

### Append .md to the URL [markdown-url]

Append `.md` to any documentation page URL. For example, this page is available at:

```
https://www.elastic.co/docs/get-started/machine-readable-docs.md
```

Two URL rules to keep in mind:

- Section landing pages sit one level up. The Markdown for `https://www.elastic.co/docs/get-started` is at `https://www.elastic.co/docs/get-started.md`, not `https://www.elastic.co/docs/get-started/index.md` (which returns a 404).
- The docs homepage has no Markdown equivalent at `/docs.md`. Use [llms.txt](#llms-txt) to get an overview of the whole site instead.

The **View as Markdown** link on each documentation page opens the same `.md` URL.

### Request Markdown with an Accept header [markdown-accept-header]

You can also fetch the HTML page URL and request Markdown by adding an `Accept` header. Send `Accept: text/markdown` or `Accept: text/plain`. A wildcard (`*/*`) or browser-default `Accept` returns HTML, so an explicit header is required.

```bash
curl -H "Accept: text/markdown" https://www.elastic.co/docs/get-started
```

Responses include `Vary: Accept`, so caches handle the two representations correctly.

## Download the full documentation set [bulk-downloads]

Three bulk artifacts cover the whole documentation site. Use the index (`llms.txt`) when you need a map of what exists. Use the Markdown bundle (`llm.zip`) to seed a local RAG index or process each page. Use the structured bundle (`okf.zip`) to import Elastic docs into a knowledge-management platform that supports the Open Knowledge Format.

### Documentation index (llms.txt) [llms-txt]

The `https://www.elastic.co/docs/llms.txt` file follows the [llmstxt.org](https://llmstxt.org/) convention: a prose introduction to Elastic Docs followed by per-section link lists with titles, descriptions, and absolute URLs.

The file is an index of where things are, not the content itself. It covers the top-level navigation groups and their first-level children. Use it to orient an agent or provide a high-level map of the documentation structure.

### Markdown bundle (llm.zip) [llm-zip]

The `https://www.elastic.co/docs/llm.zip` file is a ZIP archive containing one `.md` file per documentation page, mirroring the URL tree. Each file uses the same frontmatter and link format as the [per-page Markdown](#single-page-markdown) endpoint, so the two channels are interchangeable in content.

The archive is tens of megabytes in size. Two things to expect when processing it:

- It includes internal snippet fragments (files under `_snippets/` paths) that are not independently addressable pages.
- It includes an `llms.txt` file at the root, but this copy might not match the version served at `https://www.elastic.co/docs/llms.txt`. Use the live URL for the authoritative index.

### Structured bundle (okf.zip) [okf-zip]

The `https://www.elastic.co/docs/okf.zip` file is a ZIP archive conforming to [Open Knowledge Format v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). The bundle is tens of megabytes in size.

The OKF bundle differs from `llm.zip` in several ways:

| Feature | llm.zip | okf.zip |
|---|---|---|
| Frontmatter keys | `title`, `description`, `url`, `products`, `applies_to` | `type`, `title`, `navigation_title`, `description`, `resource`, `tags` |
| Applicability encoding | `applies_to` object | `tags` array, for example `Elastic Stack: Generally available` |
| Link style | Absolute HTML URLs | Root-relative `.md` paths, for example `/get-started/index.md` |
| Directory indexes | None | Synthesized `index.md` per folder |
| Body directives | Rendered to CommonMark | Preserved as pseudo-HTML tags, for example `<tip>` |

There is no per-page OKF endpoint. The bundle is the only distribution format.

## Connect an AI agent to the docs via MCP [docs-mcp-server]

:::{important}
This server gives agents access to Elastic **documentation**. To give an agent tools that query your own Elasticsearch data or Kibana resources, use the [{{agent-builder}} MCP server](/explore-analyze/ai-features/agent-builder/mcp-server.md) instead.
:::

The Elastic Docs MCP server is available at:

```
https://www.elastic.co/docs/_mcp/
```

It uses the streamable HTTP transport and requires no authentication. Every request is an independent POST with no session header.

### Available tools [mcp-tools]

| Tool | Description |
|---|---|
| `search_docs` | Search documentation by meaning |
| `find_related_docs` | Find pages related to a topic |
| `get_document_by_url` | Retrieve a specific page by URL |
| `analyze_document_structure` | Analyze the structure of a page |
| `check_docs_coherence` | Check how coherently a topic is covered |
| `find_docs_inconsistencies` | Find inconsistencies across pages covering the same topic |

### Configure your client [mcp-clients]

::::{tab-set}

:::{tab-item} Claude Code

Run the following command to add the Elastic Docs MCP server:

```bash
claude mcp add --transport http elastic-docs https://www.elastic.co/docs/_mcp/
```

:::

:::{tab-item} Cursor

Add the following to `.cursor/mcp.json` in your project or home directory:

```json
{
  "mcpServers": {
    "elastic-docs": {
      "url": "https://www.elastic.co/docs/_mcp/"
    }
  }
}
```

:::

:::{tab-item} VS Code

Add the following to `.vscode/mcp.json` in your project:

```json
{
  "servers": {
    "elastic-docs": {
      "type": "http",
      "url": "https://www.elastic.co/docs/_mcp/"
    }
  }
}
```

:::

::::

### Elastic plugin for Cursor [cursor-plugin]

The [Elastic plugin on the Cursor Marketplace](https://cursor.com/marketplace/elastic) bundles Elastic agent skills for Elasticsearch, Kibana, Observability, Security, and Cloud together with an `elastic-docs` MCP entry that points at the same server endpoint above. Installing the plugin is an alternative to manual Cursor configuration. The plugin source is available in the public [elastic/cursor-plugins](https://github.com/elastic/cursor-plugins) repository.

## Search and read the docs from the command line [elastic-cli]

The `docs` commands in the Elastic CLI let you search, ask questions about, and read Elastic documentation directly from a terminal.

:::{note}
The Elastic CLI is in technical preview. The `docs search` and `docs ask` commands print an experimental warning on stderr. The `docs read` command does not.
:::

Install the CLI with npm:

```bash
npm install -g @elastic/cli
```

Or run without installing:

```bash
npx -y @elastic/cli docs --help
```

The `docs` commands don't require authentication.

Three commands are available:

- `elastic docs search <query>` — search the documentation and return matching pages with summaries.
- `elastic docs ask <question>` — get an AI-generated answer based on the documentation.
- `elastic docs read <path | URL | free text>` — fetch a page as Markdown. This command reads the same `.md` endpoint described in [Get a single page as Markdown](#single-page-markdown), making it the terminal equivalent of that channel. Passing free text reads the top search result.

Pass `--json` to any command for structured output suitable for scripts or agents. Pass `--accept-experimental` to `search` and `ask` to suppress the experimental warning.

Refer to [Elastic CLI docs commands](cli://cli/docs/index.md) for the full command reference.

:::{note}
`docs-builder` is the tool that builds this documentation site. The `elastic docs` commands read the published output — the two tools serve different purposes.
:::

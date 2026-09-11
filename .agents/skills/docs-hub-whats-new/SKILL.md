---
name: docs-hub-whats-new
disable-model-invocation: true
description: Refresh the What's new cards on Elastic product hub pages. Use when updating hub-whats-new.yml after a stack release, or when the user asks to refresh hub What's new content.
---

# Refresh hub What's new cards

Update `hub-whats-new.yml` at the docs-content repo root. Hub pages render that file with `{whats-new}` and `:product: elasticsearch`, `kibana`, or `logstash`.

The Elastic Stack hub does not use this file. It links to product and solution release notes with a regular `{card-group}`.

## When to run

After a stack minor GA (for example 9.5.0), or when the user asks to refresh the hub cards. Patch releases (9.5.1) usually do not change the cards unless a highlight was wrong.

## Sources (in this order)

Read these. Do not scrape changelog YAML, docs-builder internals, or unpublished bundles.

1. **Published release notes** for the target minor. Use the rendered pages, not GitHub source that may lag:
   - [Elasticsearch](https://www.elastic.co/docs/release-notes/elasticsearch)
   - [Kibana](https://www.elastic.co/docs/release-notes/kibana)
   - [Logstash](https://www.elastic.co/docs/release-notes/logstash)
2. **Official what's-new blog** for the same minor, for example [Elastic 9.5](https://www.elastic.co/blog/whats-new-elastic-9-5-0). Use the blog to decide which items are the story of the release. Confirm each item against the published release notes before you keep it.
3. **Existing docs pages** in this repo (or `repo://` targets in other docs repos) for the `link:` on each card. Every link must resolve.

If the blog and the release notes disagree, the published release notes win for facts. The blog wins for which items belong on the hub.

## What to write

Schema: [what's new directive](https://elastic.github.io/docs-builder/syntax/whats-new/).

For each of `elasticsearch`, `kibana`, and `logstash`:

- Keep `id: whats-new` so the hub hero can jump to the panel.
- One `release-links` entry pointing at that product's release notes.
- One `upgrade-link` pointing at that product's upgrade page.
- Four or five `items`. Mark **one** item `featured: true`.
- `date` is the minor version, for example `9.5`.
- `tag` is a short category (Storage, Dashboards, Monitoring).
- `title` and `description` are sentence case, present tense, second person or impersonal. No em dashes. Do not use "click" or "choose".
- Say "Generally available" or "Technical preview" in the description when the release notes do.

## Links

Every `release-links[].url`, `upgrade-link.url`, and `items[].link` must be one of:

- Site-absolute with `.md`, for example `/manage-data/data-store/columnar.md`
- Cross-repo, for example `elasticsearch://reference/query-languages/promql.md`

Do not use `https://www.elastic.co/docs/...` for pages this site publishes. Do not use relative paths.

Confirm the file exists before you add the link. For docs-content pages, `git cat-file -e HEAD:<path>` or a working-tree glob. For other repos, use the `repo://` form and confirm the path in that repo.

If a highlight has no documentation page yet, link to the product release notes and add a `Pending links` note in the PR body.

## What not to do

- Do not invent highlights that are not in the published release notes or the blog.
- Do not copy changelog YAML entries wholesale. Those lists are complete; the hub is a short story.
- Do not add an Elastic Stack key to this file.
- Do not edit `{whats-new}` on the hub Markdown pages. Those pages only name the product key.

## PR

Title: `Refresh hub What's new cards for <version>`.

Body must list the items you kept, the sources you read (release notes URLs and blog URL), and any pending links.

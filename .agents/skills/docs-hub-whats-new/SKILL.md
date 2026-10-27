---
name: docs-hub-whats-new
disable-model-invocation: true
description: Refresh the What's new cards on Elastic product hub pages. Use when updating hub-whats-new.yml after a stack release, or when the user asks to refresh hub What's new content.
---

# Refresh hub What's new cards

Update `hub-whats-new.yml` at the docs-content repo root. Hub pages render that file with `{whats-new}` and `:product: elasticsearch`, `kibana`, or `logstash`.

The Elastic Stack hub does not use this file. Its "Elastic Stack components" section is a regular `{card-group}` with one card each for Elasticsearch, Kibana, Logstash, Elastic Agent, and Beats. Each card links to the product hub or home page, the release notes, and the reference. The release notes links do not name a version, so a Stack release does not change them. Solution release notes stay in the Elastic solutions section. Do not add a description that only repeats the card title.

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
- Set `intro` to `Highlights from recent releases.` The panel mixes cards from stack releases and from Serverless, so the intro names neither.
- Add two `release-links` entries when the product has a stack stream and a serverless stream:
  - The label is the substitution `'{{version.stack}}'`, so a patch release does not mean editing the file. Point it at the top of the release notes page, for example `kibana://release-notes/index.md`. Do not link to a `.0` heading.
  - `Serverless` pointing at `/release-notes/elastic-cloud-serverless/index.md`.
- If the product has only a stack stream, as Logstash does, one `release-links` entry is enough.
- One `upgrade-link` pointing at that product's upgrade page. For Kibana, use `/deploy-manage/upgrade/deployment-or-cluster.md` (all deployment types), not the self-managed Kibana upgrade page. The label can still be `Upgrade Kibana`.
- Exactly five `items`. Mark **one** item `featured: true`. The panel grid has three columns and the featured card takes two, so five cards fill every row. Four or six leave a short last row.
- `availability` is a list that says where the feature is available, taken from the `applies_to` tags on the page the card links to. Use `'9.5'` for a feature in the stack minor and `Serverless` for a feature on Serverless. When a card has both, write the stack version first, as in `'9.5'` then `Serverless`. Do not use `date`. It is only a fallback for an item with no availability.
- Serverless ships between stack releases, so a feature can be Serverless only. Put those cards first, with `availability: [Serverless]`. Confirm the page is tagged for Serverless and for no released stack version, or that its stack tag starts in a later version, for example `serverless: preview` with `stack: preview 9.6+`. Take candidates from the [Serverless changelog](https://www.elastic.co/docs/release-notes/elastic-cloud-serverless), and keep only features that have a documentation page to link to. A Serverless-only card is not a requirement. If no documented feature qualifies, do not add one.
- When a feature is in preview on the stack and generally available on Serverless, or the reverse, it is not Serverless only. Give it both entries and state the difference in the `description`.
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

Body must list the items you kept, the sources you read (release notes URLs, blog URL, and the Serverless changelog when you added a Serverless-only card), the `applies_to` tag you used for each `availability`, and any pending links.

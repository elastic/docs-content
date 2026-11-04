---
name: docs-hub-whats-new
disable-model-invocation: true
description: Keeps the What's new cards on Elastic product hub pages current, before and after a stack release. Use when updating hub-whats-new.yml for a stack minor, including before GA when the release notes are not published yet, or when the user asks to refresh hub What's new content.
---

# Refresh hub What's new cards

Update `hub-whats-new.yml` at the docs-content repo root. Hub pages render that file with `{whats-new}` and `:product: elasticsearch`, `kibana`, or `logstash`.

The Elastic Stack hub does not use this file. Its "Elastic Stack components" section is a regular `{card-group}` with one card each for Elasticsearch, Kibana, Logstash, Elastic Agent, and Beats. Each card links to the product hub or home page, the release notes, and the reference. The release notes links do not name a version, so a Stack release does not change them. Solution release notes stay in the Elastic solutions section. Do not add a description that only repeats the card title.

## When to run

Around a stack minor GA (for example 9.5.0), or when the user asks to refresh the hub cards. Patch releases (9.5.1) usually do not change the cards unless a highlight was wrong.

Run it in two passes:

1. **Before GA**, when the release notes and the official what's-new blog are not published yet. Pick the candidates from the Elastic Labs content project (see [Pick cards before GA from the Elastic Labs content project](#pick-cards-before-ga-from-the-elastic-labs-content-project)) and confirm each one against the docs pages.
2. **After GA**, when the release notes are published. Confirm every card against them and fix any that disagree.

## Sources (in this order)

Read these. Do not scrape changelog YAML, docs-builder internals, or unpublished bundles.

1. **Published release notes** for the target minor. Use the rendered pages, not GitHub source that may lag:
   - [Elasticsearch](https://www.elastic.co/docs/release-notes/elasticsearch)
   - [Kibana](https://www.elastic.co/docs/release-notes/kibana)
   - [Logstash](https://www.elastic.co/docs/release-notes/logstash)
2. **Official what's-new blog** for the same minor, for example [Elastic 9.5](https://www.elastic.co/blog/whats-new-elastic-9-5-0). Use the blog to decide which items are the story of the release. Confirm each item against the published release notes before you keep it.
3. **Elastic Labs content project**, when the release notes or the what's-new blog are not published yet. See [Pick cards before GA from the Elastic Labs content project](#pick-cards-before-ga-from-the-elastic-labs-content-project).
4. **Existing docs pages** in this repo (or `repo://` targets in other docs repos) for the `link:` on each card. Every link must resolve. Before GA, the `applies_to` tag on the page is the fact check.

If the blog and the release notes disagree, the published release notes win for facts. The blog wins for which items belong on the hub.

## Pick cards before GA from the Elastic Labs content project

Many launch blogs are not published until release day, so the release notes and the what's-new blog are empty or partial in the days before GA. The [Elastic Labs Content Process](https://github.com/orgs/elastic/projects/1446) project (internal, Elastic employees only) tracks every blog from idea to publication. Its issues live in `elastic/elastic-labs-blogs` and carry the abstract, the target version, a status, and a publishing date. Use it to see which features Elastic is about to announce.

Read it with the `gh` CLI. The token needs the `project` and `read:org` scopes (`gh auth status` lists them):

```sh
gh project item-list 1446 --owner elastic --limit 2000 --format json > /tmp/labs-items.json
```

Then filter the items:

- Keep an item when its issue body has a `### Version` value that names the target minor (for example `9.6`), when its title or abstract names the minor, or when its publishing date falls in the release window. Some blogs say "Available now in serverless & 9.6", so match on the minor, not on an exact string.
- Drop blogs that are not about a product feature: research, threat reports, partner and integration how-tos, and ideas still in `Article backlog`.

Weigh each blog by its `status`:

| Status | How to use it |
|---|---|
| `Done` with a publishing date on or before today | Published. A strong signal of what the story of the release is. |
| `Article ready to publish`, `Article staging`, `Article SEO/LLMO review`, `Article editorial review` | About to publish, usually on release day. A strong signal. |
| `Article technical review`, `Article in progress`, `Article ready to start` | A weaker signal. The feature can still slip. Keep it only when the docs page is already tagged for the target minor. |
| `Article backlog (available content)` | Ignore for the hub. |

A blog says what to highlight. It does not prove the feature is in the release. Before you keep a card:

1. Find the docs page for the feature in this repo at `origin/main`.
2. Read its `applies_to` tag. The card's `availability` comes from that tag, not from the blog. If the page has no tag for the target minor and no `serverless` tag, drop the card or ask the user.
3. If the abstract names a license level, a lifecycle (technical preview or GA), or a deployment (Serverless only, or stack too), check it against the page. Use the page when they disagree.

A new API can have no narrative page yet. In that case, link the generated API reference group on `https://www.elastic.co/docs/api/doc/kibana/` and take `availability` from the `x-state` of its operations in `oas_docs/output/kibana.yaml` (for example `Generally available; added in 9.6.0`) at `origin/main` in `elastic/kibana`. Open the group URL to confirm that it resolves, and list the card under `Pending links` in the PR body so a narrative page can replace it later.

Keep the project private. In the PR body, name each blog by its title and status. Do not paste abstracts, Google Doc links, or issue links into a public PR. Give the user the full list of blogs you read in chat.

Rerun the skill after GA, when the published release notes can confirm the cards.

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

Do not use `https://www.elastic.co/docs/...` for pages this site publishes. The generated API reference under `https://www.elastic.co/docs/api/doc/` is the one exception, because no source file in this repo builds it. Do not use relative paths.

Confirm the file exists before you add the link. For docs-content pages, `git cat-file -e HEAD:<path>` or a working-tree glob. For other repos, use the `repo://` form and confirm the path in that repo.

If a highlight has no documentation page yet, link to the product release notes and add a `Pending links` note in the PR body.

## What not to do

- Do not invent highlights that are not in the published release notes, the what's-new blog, or an Elastic Labs content project blog that you confirmed against a docs page.
- Do not add a card because a blog is in `Article technical review` or earlier when no docs page carries the `applies_to` tag for the target minor.
- Do not copy abstracts, Google Doc links, or Labs issue links into a public PR.
- Do not copy changelog YAML entries wholesale. Those lists are complete; the hub is a short story.
- Do not add an Elastic Stack key to this file.
- Do not edit `{whats-new}` on the hub Markdown pages. Those pages only name the product key.

## PR

Title: `Refresh hub What's new cards for <version>`.

Body must list the items you kept, the sources you read (release notes URLs, blog URL, the Serverless changelog when you added a Serverless-only card, and the titles and statuses of Elastic Labs content project blogs you used before GA), the `applies_to` tag you used for each `availability`, and any pending links.

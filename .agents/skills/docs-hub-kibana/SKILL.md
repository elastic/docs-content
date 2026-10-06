---
name: docs-hub-kibana
description: Maintain and update the Kibana product hub at products/kibana.md. Use when editing the Kibana hub, get-started steps, solutions cards, Explore Kibana sections, or link-card lists, or when the user asks to add, remove, or rebalance hub links. Checks search and page traffic before choosing links.
---

# Maintain the Kibana hub

Edit `products/kibana.md` only. Do not invent a second Kibana hub. For What's new cards, use `docs-hub-whats-new` and `hub-whats-new.yml`. Do not edit the `{whats-new}` block beyond `:product: kibana`.

Other hubs (`products/elasticsearch.md`, `products/elastic-stack.md`, `products/logstash.md`) are out of scope unless the user asks to extend this skill. The Solutions card-group is the exception: keep the same block on the Elasticsearch and Elastic Stack hubs.

## Before you edit

1. Read the current page. Do not shuffle sections or card-groups unless traffic or balance requires it (see Traffic check).
2. Run the traffic check below before you add, swap, or rebalance links.
3. Confirm every new URL exists (`git cat-file -e HEAD:<path>` or the `repo://` target).
4. Confirm UI labels and feature names against `elastic/kibana` at `origin/main` when the claim is about the product.
5. Build the page locally with `docs-builder --path . --output /tmp/hub-out` and confirm there are no errors.

Hubs stay out of the live nav. Keep `- hidden: products/kibana.md` in `docset.yml`. Do not add a `products` toc.

## Traffic check

Traffic decides which links earn a place. Page rules decide how the page stays balanced. When a rule below conflicts with a high-traffic page, traffic wins unless the page fails a correctness check.

1. **Pull traffic.** Use the `platform-analytics` repo (synced to `origin/main`, `.venv` active). Query `elastic-edm-prod.pa__stg.stg__certified_ga_general` for `event_name = 'page_view'`, `hostname = 'www.elastic.co'`, and `page_location_clean_local LIKE 'www.elastic.co/docs%'` over the last 90 days. Group by page and keep views, organic views (`ga_channel = 'Organic Search'`), and sessions. Cost is about 5 GB per run.
2. **Add search intent.** When the user has a Google Search Console export (landing page, query, clicks), join it by path. Clicks show what people search for. Views show volume. Anonymized queries are missing from GSC, so use it for intent, not totals.
3. **Scope.** Keep pages whose subject is Kibana: `/docs/explore-analyze/` (minus Elasticsearch-engine pages such as aggregations, Query DSL, EQL, SQL, Painless, EIS, and NLP models), `/docs/reference/kibana/`, `/docs/api/doc/kibana`, `/docs/release-notes/kibana`, `/docs/troubleshoot/kibana/`, and the Kibana install, configure, authentication, and upgrade pages under `/docs/deploy-manage/`.
4. **Rank and compare.** Mark which ranked pages the hub links. Check every link already on the hub against the same ranking.
5. **Decide.**
   - Add a page when it has about 800 or more organic views in 90 days, or about 100 or more search clicks, and it is a first-stop page for its topic.
   - Do not remove a link because it has low traffic. New and strategic features (Alerting V2, Context connectors, Vector Database) stay.
   - Link the page people land on, not its parent, when the two serve the same task and the child has clearly more traffic.
6. **Correctness checks still win.** Skip a page when:
   - it is deprecated and a current alternative exists (for example Playground),
   - its `applies_to` covers fewer deployments than the card implies (for example LDAP is self-managed, ECE, and ECK only, and `/deploy-manage/upgrade/deployment-or-cluster/kibana.md` is self-managed only),
   - it duplicates another item in the same card.
7. **Report.** In the PR body, list what you added with its traffic, and list high-traffic pages you skipped with the reason.

Refresh the check when a release changes the hub, and at least once per quarter.

## Page shape

Keep this order:

1. `{hero}`
2. `{get-started}`
3. `{whats-new}`
4. Solutions (`id: solutions`)
5. Explore Kibana (`id: explore`), with these card-groups in this order:
   - Quick links
   - Deploy and manage
   - Manage data and Kibana
   - Explore, visualize, and analyze
   - Alerting and incident response
   - AI and Workflows
   - Query data in Kibana
   - Secure Kibana
   - Troubleshoot
   - Reference

Do not add a Developer tools section. Developer tools is one card inside Query data in Kibana. Machine learning is one card inside Explore, visualize, and analyze.

When three or more high-traffic pages share a theme and no card fits, add a card. When a card grows past what its siblings can balance, split it or move items. Keep card titles user-facing (for example "Check server health", not a list of page types).

## Get started

- Title: `Get started with Kibana`.
- No `intro`. The steps carry the story.
- Keep three steps. The first step may fork Local | Cloud as one numbered step with `options`.

Visual experiments for this block live in docs-builder, not in this file.

## Solutions

The same Solutions card-group is on `products/elasticsearch.md` and `products/elastic-stack.md`, after What's new. When you change this block, copy the change to those two pages.

Card order: Elasticsearch, Vector Database, Observability, Security.

Vector Database is a fourth solution, Serverless only. Place it next to Elasticsearch. `{link-card}` has no `applies_to` field.

Solutions intro: "Solutions are packages of Elastic capabilities optimized for certain use cases. All solutions include the core storage, querying, and analytics capabilities of Elasticsearch and Kibana." Do not add a description on one solution card when the others have none. Match solution card link counts instead. Current target is six links each.

Elasticsearch card: Overview, Get started, Agent Builder, Query rules, Content connectors, Index management. Do not link Playground. It is deprecated in 9.4+ and on Serverless.

Observability card: Overview, Get started, APM, Logs, Infrastructure, Synthetics.

Security card: Overview, Get started, SIEM, Detection rules, Elastic Defend, Cases.

Vector Database card: Overview, Get started, Vector and full-text search, RAG, Hybrid search, Semantic search. Keep this card docs-first. Do not copy Agent Builder from the Elasticsearch card.

Icons: only keys in docs-builder `ProductIcons` (`elasticsearch`, `kibana`, `observability`, `security`, `vectordb`). `vectordb` is the EUI `logoVectorDB` mark. Do not invent or hand-draw a logo.

## Card titles and links

- Omit `link` on `{link-card}` so the title is plain text.
- Do not set `description` on a link-card inside `{explore}`. The builder drops it.
- If a page used to be the title URL, make it the first list item.
- Feature-app cards (Discover, Dashboards, Visualizations, Machine learning, Kibana alerting, Alerting V2, Agent Builder, Workflows, AI Agent chat):
  1. `<Name> overview`
  2. `Get started with <Name>` when that page exists
  3. A few key pages
- Keep labels to two or three words when you can.
- Each link in a card must be a unique entry point. Drop a page that only restates the overview or another item in the same list.
- Do not add an overview page when the card already lists the specific items (for example Query languages).
- Do not highlight a deprecated feature when a current alternative exists. Before you add a link, read the target page `applies_to` and title. If the page is deprecated, link the replacement instead (for example Agent Builder or Query rules, not Playground).
- Do not mix APIs and release notes in one list.
- Quick links stay four cards: Find your way, Release notes, APIs, Configuration. The APIs card may list a high-traffic operation page next to the two API docs (for example the Agent Builder MCP API).

## Balance links in a section

Aim for **3–6** links per Explore card, and keep siblings in the same card-group within about two links of each other. Solutions cards are six links each.

Traffic sets the links. Balance sets how you arrange them. When a card passes six links, split it into two cards or move items to a better card instead of dropping first-stop pages. Rename a card when a move changes what it covers.

When a card is short next to longer siblings, add high-traffic pages that are unique to that card. Do not pad with overviews or pages already linked nearby.

Do not add a link only to even the count. Leave a card short when it has only two real options (AutoOps overview and the Stack Monitoring comparison).

## Section rules

**Deploy.** Order: Managed on Elastic Cloud, Self-orchestrated (ECK, ECE), Self-managed, Maintain and monitor. Cloud Hosted links the deployment page and Access Kibana. ECK and ECE link the orchestrator page and the Kibana page. Serverless stays one link. Self-managed is Install, Docker, the top OS install pages by traffic (Windows, Debian and Ubuntu), and Configure. Link other packages only when the traffic check puts them above the threshold. **Upgrade Kibana** links to `/deploy-manage/upgrade/deployment-or-cluster.md` (all deployment types). Do not use `/deploy-manage/upgrade/deployment-or-cluster/kibana.md`. That page is self-managed only.

**Manage data.** Stack Monitoring and AutoOps are sibling cards. AutoOps links to the overview and the comparison with Stack Monitoring.

**Dashboards.** Include Reporting and sharing (`/explore-analyze/report-and-share.md`).

**Secure Kibana.** Authenticate users links Kibana authentication, Cloud organization authentication, and the high-traffic realms that apply to every deployment type (SAML, OpenID Connect). Skip realms that are self-managed only, such as LDAP. Authorize access links user roles, serverless custom roles, Kibana privileges, spaces, API keys, and audit logging. Protect data links secure saved objects and Kibana and Elasticsearch mutual TLS.

**Alerting.** Three cards: Kibana alerting (classic), Alerting V2, Alerting connectors. In Alerting connectors, order the popular connectors by traffic (Slack, Email, Microsoft Teams, Jira, PagerDuty).

**AI and Workflows.** Five cards: AI features, Agent Builder, Workflows, AI Agent chat, Context connectors. AI features is the product-wide entry point: AI-powered features, AI agent skills, Connect to LLMs, and Elastic Managed LLMs. Agent Builder includes the MCP server guide. AI assistants in Kibana meets the traffic threshold but stays off the hub as an editorial choice. Confirm with the hub owner before you add it. Context connectors lead with three popular connectors, then View all.

**Query data.** Languages, Developer tools, Search across clusters (CCS, remote clusters, CPS). No query-languages overview item. Languages lists KQL, the KQL reference, Lucene, ES|QL, Query DSL, and SQL.

**Troubleshoot.** Two cards of three links: Diagnose common issues (troubleshooting, Alerts, Server not ready) and Check server health (Server status, diagnostics, server logs).

## Copy

Second person, present tense, active voice. Sentence case. No em dashes. No "click" or "choose".

Section intros speak to the reader. Do not restate the heading, and do not use phrases such as "purpose-built experiences" or "apps and capabilities that help you understand and act on your data."

## What not to do

- Do not put hubs back in the production toc.
- Do not make card titles clickable.
- Do not shuffle categories or cards without a traffic or balance reason. State the reason in the PR body.
- Do not remove a link because it has low traffic.
- Do not refresh What's new items here. Use `docs-hub-whats-new`.
- Do not invent icons or screenshots.
- Do not land get-started visual prototypes in this repo.
- Do not put deprecated first-stop features on hub cards.

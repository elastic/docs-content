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
   - its `applies_to` covers fewer deployments than the card implies (for example LDAP is self-managed, ECE, and ECK only, and `/deploy-manage/upgrade/deployment-or-cluster/kibana.md` is self-managed only). A page that is only unavailable on Serverless (Graph, Watcher) can stay when its traffic is high and its own page states the limit. Note it in the PR body.
   - it duplicates another item in the same card.
7. **Report.** In the PR body, list what you added with its traffic, and list high-traffic pages you skipped with the reason.

Refresh the check when a release changes the hub, and at least once per quarter.

## Page shape

Keep this order:

1. `{hero}`
2. `{get-started}`
3. `{whats-new}`
4. Solutions (`id: solutions`)
5. Three `{explore}` blocks, in this order. Each block has its own H2 title and intro, and each card-group inside becomes an accordion.
   - Explore Kibana (`id: explore`, the hero jump target): Quick links
   - Use Kibana (`id: use-kibana`, tasks for people who work with data):
     - Explore, visualize, and analyze data
     - Query data in Kibana
     - Alerting and incident response
     - AI and Workflows
   - Set up and run Kibana (`id: run-kibana`, tasks for people who install and operate the stack):
     - Install and deploy
     - Get data in
     - Manage Kibana
     - Secure Kibana
     - Troubleshoot

There is no Reference section. Its cards live where the task is: Configuration and settings in Install and deploy, and Release notes and Related release notes in Manage Kibana. Quick links stays the only cross-cutting group. Split by task, not by role, because many readers do both.

Do not add a Developer tools section. Developer tools is one card inside Query data in Kibana. Machine learning is one card inside Explore, visualize, and analyze data.

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

Do not add a link only to even the count. Leave a card short when it has only two real options.

## Section rules

**Install and deploy.** Configuration and settings is the last card. Order: Managed on Elastic Cloud, Self-orchestrated (ECK, ECE), Install self-managed. Cloud Hosted links the deployment page and Access Kibana. ECK and ECE link the orchestrator page and the Kibana page, and ECK adds the Kibana quickstart. Serverless stays one link. Install self-managed is Install, Docker, and the top package pages by traffic (Windows, Debian and Ubuntu, RPM, Linux and macOS archive). Self-managed-only pages belong in the Install self-managed card, not in cards that imply every deployment type. Configure (kibana.yml) and Access Kibana (self-managed) are not on the hub. Configuration and settings covers configuration.

**Get data in and Manage Kibana.** Get data in has Data and indices, Integrations and Fleet, and Elastic Agent. Manage Kibana has Monitor, Upgrade and maintain, Spaces, objects, and connectors, Release notes, and Related release notes. Data and indices links the Transforms landing page, not the setup page. Integrations and Fleet links Integrations, Fleet, Manage agents, and Agent policies. Elastic Agent links Install Elastic Agent, Fleet Server, and the command reference. Skip the Fleet air-gapped page. It applies to ECE and self-managed only. Spaces, objects, and connectors includes Manage connectors. Monitor combines Stack Monitoring (Kibana monitoring data, configure, alerts) and AutoOps (overview, comparison with Stack Monitoring). Upgrade and maintain links Run in production, Upgrade Kibana, Upgrade Assistant, and Logging. **Upgrade Kibana** links to `/deploy-manage/upgrade/deployment-or-cluster.md` (all deployment types). Do not use `/deploy-manage/upgrade/deployment-or-cluster/kibana.md`. That page is self-managed only.

**Explore.** Dashboards links the overview, Get started, Create a dashboard, Ways to create, and Best practices. Interact and share links Add controls, Drilldowns, and Reporting and sharing (`/explore-analyze/report-and-share.md`). Visualizations includes Graph.

**Secure Kibana.** Authenticate users links Kibana authentication, Cloud organization authentication, Cloud SAML single sign-on, and the high-traffic realms that apply to every deployment type (SAML, OpenID Connect). Skip realms that are self-managed only, such as LDAP. Authorize access links user roles, Kibana role management, serverless custom roles, and Kibana privileges. Control and audit access links spaces, API keys, and audit logging. Protect data links secure saved objects and Kibana and Elasticsearch mutual TLS.

**Alerting.** Four cards: Alerting systems (the alerting overview and Watcher), Kibana alerting (classic), Alerting V2, Alerting connectors. In Alerting connectors, order the popular connectors by traffic (Slack, Email, Microsoft Teams, Jira, PagerDuty).

**AI and Workflows.** Six cards: AI features, Agent Builder, Models and MCP, Workflows, AI Agent chat, Context connectors. AI features is the product-wide entry point: AI-powered features, AI agent skills, Connect to LLMs, and Elastic Managed LLMs. Agent Builder links the overview, Get started, Agents, Tools, and Custom tools. Models and MCP links Models and the MCP server guide. AI assistants in Kibana meets the traffic threshold but stays off the hub as an editorial choice. Confirm with the hub owner before you add it. Context connectors lead with three popular connectors, then View all.

**Query data.** Query and filter, ES|QL, Developer tools, Search across clusters (CCS, remote clusters, CPS). No query-languages overview item. Query and filter lists KQL, the KQL reference, Lucene, Query DSL, SQL, and Filter data. ES|QL lists ES|QL in Kibana, the ES|QL reference, and Functions and operators. Developer tools leads with the Query tools overview.

**Troubleshoot.** Two cards: Diagnose common issues (troubleshooting, Alerts, Server not ready, Fleet and Agent problems) and Check server health (Server status, diagnostics, server logs).

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

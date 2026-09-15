---
name: docs-hub-kibana
description: Maintain and update the Kibana product hub at products/kibana.md. Use when editing the Kibana hub, get-started steps, solutions cards, Explore Kibana sections, or link-card lists, or when the user asks to add, remove, or rebalance hub links.
---

# Maintain the Kibana hub

Edit `products/kibana.md` only. Do not invent a second Kibana hub. For What's new cards, use `docs-hub-whats-new` and `hub-whats-new.yml`. Do not edit the `{whats-new}` block beyond `:product: kibana`.

Other hubs (`products/elasticsearch.md`, `products/elastic-stack.md`, `products/logstash.md`) are out of scope unless the user asks to extend this skill.

## Before you edit

1. Read the current page. Do not shuffle sections, card-groups, or cards unless the user asks.
2. Confirm every new URL exists (`git cat-file -e HEAD:<path>` or the `repo://` target).
3. Confirm UI labels and feature names against `elastic/kibana` at `origin/main` when the claim is about the product.

Hubs stay out of the live nav. Keep `- hidden: products/kibana.md` in `docset.yml`. Do not add a `products` toc.

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

## Get started

- Title: `Get started with Kibana`.
- No `intro`. The steps carry the story.
- Keep three steps. The first step may fork Local | Cloud as one numbered step with `options`.

Visual experiments for this block live in docs-builder, not in this file.

## Solutions

Card order: Elasticsearch, Vector Database, Observability, Security.

Vector Database is a fourth solution, Serverless only. Place it next to Elasticsearch. `{link-card}` has no `applies_to` field.

Solutions intro: "Solutions are packages of Elastic capabilities optimized for certain use cases." Do not add a description on one solution card when the others have none. Match solution card link counts instead. Current target is five links each.

Elasticsearch card: Overview, Get started, Agent Builder, Query rules, Content connectors. Do not link Playground. It is deprecated in 9.4+ and on Serverless.

Icons: only keys in docs-builder `ProductIcons` (`elasticsearch`, `kibana`, `observability`, `security`, `vectordb`). `vectordb` is the EUI `logoVectorDB` mark (docs-builder PR that adds it). Do not invent or hand-draw a logo. The icon will not render in preview until that docs-builder change is in the builder the preview uses.

## Card titles and links

- Omit `link` on `{link-card}` so the title is plain text.
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
- Quick links stay four cards: Find your way, Release notes, APIs, Configuration.

## Balance links in a section

Aim for **3–5** links per card, and keep siblings in the same card-group within about one link of each other.

When a card is long next to shorter siblings, drop 1–2 links that are not first-stop pages (extra install packages, niche languages, troubleshooting for a single app, a concept page already covered by the overview).

When a card is short next to 4–5-link siblings, add 1–2 high-value pages that are unique to that card. Do not pad with overviews or pages already linked nearby.

Do not add a link only to even the count. Leave a card short when it has only two real options (Cloud hosted vs Serverless, ECK vs ECE, the two Kibana API docs).

## Section rules

**Deploy.** Order: Managed on Elastic Cloud, Self-orchestrated (ECK, ECE), Self-managed, Maintain and monitor. Self-managed is Install, Docker, and Configure. Do not list every OS package.

**Alerting.** Three cards: Kibana alerting (classic), Alerting V2, Alerting connectors.

**AI and Workflows.** Four cards: Agent Builder, Workflows, AI Agent chat, Context connectors. Do not add AI Assistant or generative AI connectors. Context connectors lead with three popular connectors, then View all.

**Query data.** Languages, Developer tools, Search across clusters (CCS, remote clusters, CPS). No query-languages overview item.

## Copy

Second person, present tense, active voice. Sentence case. No em dashes. No "click" or "choose".

Section intros speak to the reader. Do not restate the heading, and do not use phrases such as "purpose-built experiences" or "apps and capabilities that help you understand and act on your data."

## What not to do

- Do not put hubs back in the production toc.
- Do not make card titles clickable.
- Do not shuffle categories or cards unless the user asks.
- Do not refresh What's new items here. Use `docs-hub-whats-new`.
- Do not invent icons or screenshots.
- Do not land get-started visual prototypes in this repo.
- Do not put deprecated first-stop features on hub cards.

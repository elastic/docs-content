---
navigation_title: Manage entities
description: Refine and group the entities that matter using watchlists, entity resolution, and privileged user monitoring in Elastic Security entity analytics.
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Manage entities

Once [entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) is running, you can refine which entities matter most and how they're grouped. These capabilities build on top of risk scoring: watchlist membership feeds the risk weighting, and entity resolution consolidates duplicate records and aggregates their scores.

* [Watchlists](/solutions/security/advanced-entity-analytics/watchlists.md): Define groups of important entities — such as executives or critical infrastructure hosts — and factor their membership into entity risk scoring.
* [Entity resolution](/solutions/security/advanced-entity-analytics/entity-resolution.md): Link multiple entity records that represent the same real-world identity and consolidate their risk scores into a single view.
* [Privileged user monitoring](/solutions/security/advanced-entity-analytics/privileged-user-monitoring.md): {applies_to}`stack: removed 9.4+, ga =9.3, preview 9.1-9.2` Track the activity of users with elevated permissions. Replaced by watchlists.

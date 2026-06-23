---
applies_to:
  stack: ga 9.4+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Watchlists 

::::{admonition} Requirements
This feature requires the appropriate [subscription](https://www.elastic.co/pricing) in {{stack}} or [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md) in {{serverless-short}}.
::::

Watchlists let you define and manage groups of entities that are important to your organization — such as executives or critical infrastructure hosts — and factor watchlist membership directly into entity risk scoring. This keeps your most critical entities visible and easy to find during threat investigations. Watchlists sync automatically every 10 minutes to reflect changes in the underlying data sources.

Watchlists replace the [Privileged user monitoring](/solutions/security/advanced-entity-analytics/privileged-user-monitoring.md) feature. No data is migrated from existing privileged user monitoring configurations; you set up watchlists from scratch.

## Default watchlist [watchlists-default]

A **Privileged Users** watchlist is available by default. It automatically pulls in administrative users from your [Active Directory Entity Analytics](integration-docs://reference/entityanalytics_ad.md) and [Okta Entity Analytics](integration-docs://reference/entityanalytics_okta.md) integrations, so you don't need to manually define these users.

## Risk weighting [watchlists-risk-weighting]

Each watchlist has a configurable risk weighting that influences the risk scores of its members. When an entity belongs to a watchlist, the risk score maintainer applies the watchlist's risk weighting using a Bayesian update — either increasing or decreasing the alert-based risk score depending on the configured weight.

For example, assigning a higher risk weighting to a watchlist of executives means that suspicious activity involving those users scores higher and surfaces sooner during investigations.

To learn how watchlist weighting fits into the overall risk score calculation, refer to [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md).

## Create a watchlist [watchlists-create]

To create a watchlist:

1. Go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
    * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
    * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
2. Go to the **Watchlists** tab.
3. Click **Create watchlist**.
4. Enter a name and, optionally, a description.
5. Set a **Risk Score Weighting** using the slider.
6. Under **Rule Based Data Sources**, define which entities belong to this watchlist:
   * **Entity Store**: Filter existing entities in the entity store using KQL syntax.
   * **IndexPattern**: Select an index pattern, apply a KQL filter, and choose the field used to identify entities.
7. Click **Save**.

An entity can belong to more than one watchlist.

## View and manage watchlists [watchlists-manage]

The **Watchlists** tab displays all watchlists in the current {{kib}} space. You can edit and delete individual watchlists using the icons in the relevant watchlist row.

:::{image} /solutions/images/security-watchlists.png
:alt: The Watchlists tab on the Entity analytics management page
:screenshot:
:::

## Filter entities by watchlist [watchlists-filter]

On the [Entity analytics page](/solutions/security/advanced-entity-analytics/overview.md), you can filter the **Entities** section by watchlist membership to focus on the entities most relevant to your investigation.

## Known limitations [watchlists-limitations]

* Up to 10,000 entities can be defined per data source.
* You cannot remove entities from a watchlist using CSV upload; use the [Entity Analytics API]({{kib-apis}}/group/endpoint-security-entity-analytics-api) instead.

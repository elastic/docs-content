---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-overview.html
applies:
  stack:
---

# Behavioral analytics [behavioral-analytics-overview]

Behavioral Analytics is an analytics event collection platform. Use these tools to analyze your users' searching and clicking behavior. Leverage this information to improve the relevance of your search results and identify gaps in your content.

[Get started](behavioral-analytics-start.md) by embedding one of our JavaScript clients on your website or application and instrumenting the user actions you want to track. For example, you can track when a user searches, when they click on a search result, or when a user visits a particular page on your website.

Data and analytics are stored in {{es}} indices, for advanced analysis and visualization.

Even if you don’t use Elastic for search, you can use these tools to collect analytics from your application/website.


## Availability and prerequisites [behavioral-analytics-overview-prerequisites] 

::::{note} 
Behavioral Analytics is a **beta feature**. Beta features are subject to change and are not covered by the support SLA of general release (GA) features. Elastic plans to promote this feature to GA in a future release.

::::


::::{dropdown} Expand to learn about version history
* Behavioral Analytics was introduced in Elastic **8.7.0** to the Enterprise Search service.
* There was a breaking schema change in **8.8.0**. (See [Migrating from 8.7 to 8.8](https://www.elastic.co/guide/en/enterprise-search/current/analytics-migration.html) in the Search documentation if you’re upgrading from 8.7 to 8.8.)
* The feature was moved to Elasticsearch in **8.10**, meaning the Enterprise Search service is no longer required as of 8.10.
::::


Analytics are available to all Elastic Cloud users.

Analytics are also available to **self-managed** deployments that satisfy subscription requirements. View the requirements for this feature under the **Elastic Search** section of the [Elastic Stack subscriptions](https://www.elastic.co/subscriptions) page.

Your Elastic deployment must include the {{es}} and {{kib}}services.


## Documentation [behavioral-analytics-overview-docs] 

The following documentation is available in the {{es}} docs:

* [Get started](behavioral-analytics-start.md)
* [API overview](behavioral-analytics-api.md)
* [Set up CORs](behavioral-analytics-cors.md)
* [View events](behavioral-analytics-event.md)
* [Events reference](behavioral-analytics-event-reference.md)

Additional documentation is available in the following places:

* The [Behavioral Analytics Tracker Mono Repo](https://github.com/elastic/behavioral-analytics-tracker/tree/main#readme) contains the source code for the Behavioral Analytics Tracker, which can be embedded using either the JavaScript or Browser trackers:

    * Read the [JavaScript tracker README](https://github.com/elastic/behavioral-analytics-tracker/blob/main/packages/javascript-tracker/README.md).
    * Read the [Browser tracker README](https://github.com/elastic/behavioral-analytics-tracker/blob/main/packages/browser-tracker/README.md).

* The Search UI documentation contains information about the [Search UI Analytics Plugin](https://docs.elastic.co/search-ui/api/core/plugins/analytics-plugin).
* Behavioral Analytics uses a number of [APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-analytics) to manage analytics collections.

::::{admonition} GDPR compliance
:class: note

Users may be concerned about the privacy implications of analytics data collection. Behavioral Analytics is fully GDPR compliant, because no personal data are collected.

To integrate the behavioral analytics client, session data are stored in two tokens:

* **User Token**. A unique identifier for the user. Stored under `EA_UID` cookie. Default time length is 24 hours from the first time the user visits the site.
* **Session Token**. A unique identifier for the session. Stored under `EA_SID` cookie. Time length is 30 minutes from the last time the user visits the site.

These tokens enable the client to identify a user across sessions. They do not collect sensitive information, such as IP addresses or location data, or any other personal data.

::::








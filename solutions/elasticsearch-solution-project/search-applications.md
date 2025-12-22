---
navigation_title: Search Applications
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-application-overview.html
applies_to:
  stack: beta
  serverless: beta
products:
  - id: elasticsearch
---

# Search applications [search-application-overview]

::::{important}
Search Applications is a beta feature and is not recommended for new users in {{es}} 9.x. Beta features are subject to change and are not covered by the support SLA of general release (GA) features.
::::

*Search Applications* enable users to build search-powered applications that leverage the full power of {{es}} and its Query DSL, with a simplified user experience. Create search applications based on your {{es}} indices, build queries using search templates, and easily preview your results directly in the {{kib}} Search UI.

You can also interact with your search applications using the [Search Application APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search_application). Search Applications are designed to simplify building unified search experiences across a range of enterprise search use cases, using the Elastic platform.

::::{admonition} Search Applications documentation
Documentation for the Search Applications feature lives in two places:

* The documentation in this section covers the basics of Search Applications, information about working with Search Applications in the {{kib}} UI, and use case examples.
* The [{{es}} API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-search_application) contains the API references for working with Search Applications programmatically. Jump there if you’re only interested in the APIs.

::::



## Availability and prerequisites [search-application-overview-prerequisites] 

The Search Applications feature was introduced in Elastic version **8.8.0**.

This feature is available to all **{{ech}}** deployments.

This feature is also available to **self-managed** deployments when Elastic subscription requirements are satisfied. View the requirements for this feature under the **Elastic Search** section of the [Elastic Stack subscriptions](https://www.elastic.co/subscriptions) page.

For Serverless users, this is an API-only feature. You can create and manage search applications using the [Search Application APIs](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/group/endpoint-search_application).

Your deployment must include the {{es}} and {{kib}} services.

Managing search applications requires the `manage_search_application` cluster privilege, and also requires the `manage` [index privilege](elasticsearch://reference/elasticsearch/security-privileges.md#privileges-list-indices) on all indices associated with the search application.


## Overview [search-application-overview-summary] 

The {{es}} [Query DSL](../../explore-analyze/query-filter/languages/querydsl.md) is powerful and flexible, but it comes with a steep learning curve. Complex queries are verbose and hard to understand for non-experts. We’ve designed search applications to be easier to search over, but with the flexibility of working with an {{es}} index.

Search Applications use [search templates](/solutions/search/search-templates.md) to simplify the process of building queries. Templates are defined when creating a search application, and can be customized according to your needs. Read [Search API and templates](search-applications/search-application-api.md) for the details.


## Get started [search-application-overview-get-started] 

### Option 1: Get started in the UI [search-application-overview-get-started-ui] 

```{applies_to}
serverless: unavailable 
```
:::{warning}
:applies_to: {"stack": "unavailable 9.2.0"}
This feature is unavailable for new users and is hidden from the navigation menu. It remains accessible for users who started using the feature before 9.2.
::::


You can create build, and manage your search applications directly in the {{kib}} UI under **Search**. Make sure you have at least one {{es}} index to work with on your deployment. The indices underlying your search application are searched together, similar to how an [alias](../../manage-data/data-store/aliases.md) searches over multiple indices.

To create a new search application in {{kib}}:

1. Go to **Search > Search Applications**.
2. Select **Create**.
3. Select the {{es}} indices you want to use for your search application.
4. Name your search application.
5. Select **Create**.

Your search application should now be available in the list.

Once created, you can explore the documents in your search application under **Search > Search Applications >** *your-search-application* > **Docs Explorer**. From there, you can expand a matching {{es}} document to see its full contents.


### Option 2: Get started with the API [search-application-overview-get-started-api] 

Use the {{es}} [Put Search Application API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search-application-put) to create a search application.

The following example creates a search application named `my_search_application` that searches over the `my_search_index1` and `my_search_index2` indices, along with defining a simple search template (Refer to [Default template example](search-applications/search-application-api.md#search-application-api-default-template)).

```console
PUT /_application/search_application/my_search_application
{
  "indices": [ "my_search_index1", "my_search_index2" ],
  "template": {
    "script": {
      "source": {
        "query": {
          "query_string": {
            "query": "{{query_string}}",
            "default_field": "{{default_field}}"
          }
        }
      },
      "params": {
        "query_string": "*",
        "default_field": "*"
      }
    }
  }
}
```


### Search templates [search-application-overview-get-started-templates] 

Search templates are the heart of your search applications. The [default template](search-applications/search-application-api.md#search-application-api-default-template) created for a search application is very minimal, and you’ll want to customize it to suit your needs. [Search API and templates](search-applications/search-application-api.md) contains a number of examples to get you started, including the default template, as well as templates for text search, semantic search and hybrid search.





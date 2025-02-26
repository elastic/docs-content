---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-api-console.html
---

# Access the Elasticsearch API console [ech-api-console]

Interact with a specific Elasticsearch cluster directly from the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body) without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for Elasticsearch API calls.

::::{note} 
API console is intended for admin purposes. Avoid running normal workload like indexing or search request.
::::


You are unable to make Elasticsearch Add-On for Heroku platform changes from the Elasticsearch API.

1. Log in to the [Elasticsearch Add-On for Heroku console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Deployments** page, select your deployment.

    Narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From the Elasticsearch menu, go to the **API Console** page.
4. Make a selection from the operation drop-down list and complete the path.

    For example, select `GET`, then use the `_cluster/health?pretty=true` path for cluster status and other pertinent details.

5. If needed, add the body information.

    ::::{tip} 
    To display the body area, select PUT, POST, or DELETE from the drop-down list.
    ::::

6. Select **Submit**.

The results of the API operation are displayed, along with the time it took to complete the operation.

To learn more about what kinds of Elasticsearch API calls you can make from the Cloud UI, check the [Elasticsearch Reference](https://www.elastic.co/guide/en/elasticsearch/reference/current).


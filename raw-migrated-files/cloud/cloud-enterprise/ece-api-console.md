# Access the Elasticsearch API console [ece-api-console]

Interact with a specific Elasticsearch cluster directly from the Cloud UI without having to authenticate again. This RESTful API access is limited to the specific cluster and works only for Elasticsearch API calls.

::::{note} 
API console is intended for admin purposes. Avoid running normal workload like indexing or search request.
::::


You are unable to make Elastic Cloud Enterprise platform changes from the Elasticsearch API. If you want to work with the platform, check the [Elastic Cloud Enterprise RESTful API](asciidocalypse://docs/cloud/docs/reference/cloud-enterprise/restful-api.md).

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

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


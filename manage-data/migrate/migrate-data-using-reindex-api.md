---
navigation_title: Migrate data using the reindex API
applies_to:
  serverless: preview 9.3
  deployment:
    ess: ga
    self: unavailable
products:
  - id: elasticsearch
  - id: cloud-hosted
---

# Migrate {{es}} data using the reindex API [migrate-reindex-from-remote]

The [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) offers a convenient way for you to migrate your {{es}} documents from a source index, data stream, or alias in one deployment to another.

This guide gives the example of reindexing a full index from an {{ech}} deployment an {{serverless-full}} project using the remote host parameters as shown in the [reindex from remote](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) example. These steps can be adapted to other deployment types according to the tables listed in [User data migration guides](/manage-data/migrate-data.md#data-migration-guides).

For more advanced use cases, including data modification using scripts or ingest pipelines, refer to the [Reindex indices examples](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) and the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) documentation. 

:::{tip}
If you're migrating from a self-managed cluster that uses non–publicly trusted TLS certificates, including self-signed certificates and certificates signed by a private certificate authority (CA), refer to our guide [Reindex from a self-managed cluster using a private CA](/manage-data/migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md).
:::

## Prerequisites [migrate-reindex-from-remote-prereqs]

- An {{ech}} deployment with data to migrate
- A [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) project configured and running
- An [API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) for authentication with the {{ech}} deployment

  Basic authentication can be used in place of an API key, but an API key is recommended as a more secure option.

- The target deployment must be able to access your original source cluster to perform the reindex operation. Access is controlled by the {{es}} `reindex.remote.whitelist` user setting.

    Domains matching the patterns `["*.io:*", "*.com:*"]` are allowed by default, so if your remote host URL matches that pattern you do not need to explicitly define `reindex.remote.whitelist`.

    Otherwise, if your remote endpoint is not covered by the default patterns, adjust the setting to add the remote {{es}} cluster as an allowed host:

    1. From your deployment menu, go to the **Edit** page.
    2. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you might have to expand the **Edit elasticsearch.yml** caret for each node type instead.
    3. Add the following `reindex.remote.whitelist: [REMOTE_HOST:PORT]` user setting, where `REMOTE_HOST` is a pattern matching the URL for the remote {{es}} host that you are reindexing from, and `PORT` is the host port number. Do not include the `https://` prefix.

        If you override the parameter, it replaces the defaults: `["*.io:*", "*.com:*"]`. If you still want these patterns to be allowed, you need to specify them explicitly in the value.

        For example:

        `reindex.remote.whitelist: ["*.us-east-1.aws.found.io:9243", "*.com:*"]`

    4. Save your changes.



:::{important} 
Kibana assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually.

Templates, data stream definitions, and ILM policies, must be in place _before_ you start data migration. However, be mindful that if you have any [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) configured, it's typically best to add these _after_ data migration so as to avoid re-transforming data that had already been transformed at the time that it was ingested into your source deployment (though if the data is idempotent, re-transforming is not a concern).

Visual components, such dashboard and visualizations, can be migrated after you have migrated the data.
:::

## Migrate documents from {{ech}} to {{serverless-short}}

1. In your {{ech}} deployment:

    1. Navigate to the deployment home page and copy the {{es}} endpoint. 

    1. Go to the **Index Management** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    1. Use the search field to identify the indices that you want to migrate.

1. In your {{serverless-short}} project:

    1. Open the Developer Tools [Console](/explore-analyze/query-filter/tools/console.md).

    1. Call the reindex API to migrate your index. If you have multiiple indices to migrate, we recommend doing a separate call for each.

        Example: Reindex from an {{ech}} deployment to a {[serverless-short]} project using an API key:

        ```
        POST _reindex
        {
          "source": {
            "remote": {
              "host": "https://<SERVERLESS_HOST_URL>:443", <1>
              "api_key": "<ECH_API_KEY>" <2>
            },
            "index": "<SOURCE_INDEX>" <3>
          },
          "dest": {
            "index": "<DESTINATION_INDEX>" <4>
          }
        }
        ```
        1. The URL for your {{serverless-short}} project. This is the {{es}} endpoint that you copied in Step 1. If you're migrating to, for example, an {{ech}} cluster, you can modify the remote host address accordingly.
        1. The API key for authenticating the connection to your {{ech}} deployment.
        1. The source index to copy from your {{ech}} deployment.
        1. The destination index in your {{serverless-short}} project.

    1. Verify that the new index is present:

        ```sh
        GET INDEX-NAME/_search?pretty
        ```

    1. If you are not planning to reindex more data from the remote and you configured a `reindex.remote.whitelist` user setting, that setting can now be removed.
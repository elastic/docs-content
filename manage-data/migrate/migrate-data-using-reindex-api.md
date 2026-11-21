---
navigation_title: Migrate data using the reindex API
applies_to:
  serverless: ga
  stack: ga
products:
  - id: elasticsearch
  - id: cloud-serverless
  - id: cloud-hosted
---

# Migrate {{es}} data using the reindex API [migrate-reindex-from-remote]

The [reindex API]({{es-apis}}operation/operation-reindex) offers a convenient way for you to copy your {{es}} documents from a source index, data stream, or alias in one deployment to another.

:::{important}
This guide gives the example of reindexing a full index from an {{ech}} deployment to an {{serverless-full}} project using the remote host parameters as shown in the [reindex from remote](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) example. These steps can be adapted to other deployment types as well. When you copy your data to deployment types other than {{serverless-short}}, there are [additional considerations](#migrate-reindex-from-remote-others) to make note of.
:::

For more advanced use cases, including data modification using scripts or ingest pipelines, refer to the [Reindex indices examples](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) and the [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) documentation.

## Prerequisites [migrate-reindex-from-remote-prereqs]

- An {{ech}} deployment with data to migrate
- An [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) project configured and running
- An [{{es}} API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) for authentication with the {{ech}} deployment
- Network access from the destination project to the source {{ech}} endpoint. Any network security policy on the source must permit the connection.

  Basic authentication can be used in place of an API key, but an API key is recommended as a more secure option.


:::{important} 
Kibana assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually. Refer to [Migration options](/manage-data/migrate.md#migration-options) for details about migrating different types of {{es}} data.

Index templates, data stream definitions, and data lifecycle settings must be in place _before_ you start reindexing data. However, if you have any [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) configured, it's typically best to add these _after_ data migration so as to avoid re-transforming data that had already been transformed at the time that it was ingested into your source deployment. If the data is idempotent, re-transforming is not a concern.

Visual components, such dashboard and visualizations, can be migrated after you have migrated the data.
:::

## Migrate documents from {{ech}} to {{serverless-short}} [migrate-reindex-from-remote-ech-serverless]

The following steps walk you through locating the source index and {{es}} endpoint in your {{ech}} deployment, then running a remote reindex from your {{serverless-short}} project so documents are copied into a destination index.

1. In your {{ech}} deployment:

    1. Navigate to the deployment home page and copy the {{es}} endpoint. 

    1. Open {{kib}} and go to the **Index Management** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    1. Use the search field to identify the indices that you want to migrate.

1. In your {{serverless-short}} project:

    1. Open the Developer Tools [Console](/explore-analyze/query-filter/tools/console.md).

    1. Call the reindex API to migrate your index. If you have multiple indices to migrate, then you should perform a separate call for each.

        Example: Reindex from an {{ech}} deployment to a {{serverless-short}} project using an API key:

        ```console
        POST _reindex
        {
          "source": {
            "remote": {
              "host": "<ECH_ELASTICSEARCH_ENDPOINT>", <1>
              "api_key": "<ENCODED_ELASTICSEARCH_API_KEY>" <2>
            },
            "index": "<SOURCE_INDEX>" <3>
          },
          "dest": {
            "index": "<DESTINATION_INDEX>" <4>
          }
        }
        ```
        1. The complete {{es}} endpoint for your source {{ech}} deployment, including its scheme and port, that you copied in Step 1.
        1. The encoded {{es}} API key for authenticating the connection to your {{ech}} deployment.
        1. The source index to copy from your {{ech}} deployment.
        1. The destination index in your {{serverless-short}} project.

    1. Verify that the new index is present:

        ```console
        GET <DESTINATION_INDEX>/_search?pretty
        ```

## Notes for migrating between other deployment types [migrate-reindex-from-remote-others]

The page demonstrates copying data from an {{ech}} deployment to {{serverless-short}}. When you use the reindex API to copy data across other deployment types there are a couple of things to consider.

### Authenticating to the source

The `source.remote.api_key` field is available in {{serverless-short}} and in the versioned {{stack}} 9.3 and later. For an earlier {{stack}} destination, use basic authentication or set `source.remote.headers.Authorization` to `ApiKey <ENCODED_ELASTICSEARCH_API_KEY>`.

Use an {{es}} REST API key for the source. A cross-cluster API key does not authenticate requests to the REST API.

### Using non–publicly trusted TLS certificates

This option applies only to destinations where you can configure certificate authority settings. A {{serverless-short}} destination can't reindex from a self-managed source.

If you're migrating from a self-managed cluster that uses non–publicly trusted TLS certificates, including self-signed certificates and certificates signed by a private certificate authority (CA), refer to our guide [Reindex from a self-managed cluster using a private CA](/manage-data/migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md).

### Connecting to the source cluster

The target deployment must be able to access your source cluster to perform the reindex operation. A {{serverless-short}} destination can reindex from remote {{ech}} deployments and other {{serverless-short}} projects. Other remote source types are not supported.

The remote host allowlist controls which host names the destination can contact. It does not bypass network security policies on the source. The source endpoint must be reachable from the destination, and its network policy must permit the connection.

For destinations that run the versioned {{stack}}, access is controlled by the {{es}} `reindex.remote.whitelist` setting. In {{ech}} and {{ece}}, domains matching the patterns `["*.io:*", "*.com:*"]` are allowed by default, so you don't need to configure the setting if your remote host URL matches one of these patterns.

If an {{ech}} or {{ece}} destination needs to access a remote endpoint that the default patterns don't cover, add the source {{es}} cluster as an allowed host:

  1. From your deployment menu, go to the **Edit** page.
  2. In the **Elasticsearch** section, select **Manage user settings and extensions**. For deployments with existing user settings, you might have to expand the **Edit elasticsearch.yml** caret for each node type instead.
  3. Add the following `reindex.remote.whitelist: [REMOTE_HOST:PORT]` user setting, where `REMOTE_HOST` is a pattern matching the URL for the remote {{es}} host that you are reindexing from, and `PORT` is the host port number. Do not include the `https://` prefix.

      If you override the parameter, it replaces the defaults: `["*.io:*", "*.com:*"]`. If you still want these patterns to be allowed, you need to specify them explicitly in the value.

      For example:

      `reindex.remote.whitelist: ["*.us-east-1.aws.found.io:9243", "*.com:*"]`
      
  4. Save your changes.

After the migration, remove the source host from `reindex.remote.whitelist` if the destination no longer needs to access it.

For {{eck}} and self-managed destinations, configure `reindex.remote.whitelist` in `elasticsearch.yml`. Refer to [`reindex.remote.whitelist`](elasticsearch://reference/elasticsearch/configuration-reference/index-management-settings.md#reindex-settings) for details.

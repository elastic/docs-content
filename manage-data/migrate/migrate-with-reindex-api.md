---
navigation_title: Migrate with the reindex API
applies_to:
  serverless: preview
  deployment:
    ess: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
---

# Migrate {{ech}} data to {{serverless-short}} with the reindex API [migrate-reindex-from-remote]

The [reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) offers a convenient way for you to migrate your documents from a source index, data stream, or alias in an {{ech}} deployment to an index in a {{serverless-full}} project.

:::{admonition} Basic migration
This guide focuses on a basic data migration scenario for moving either full index or selected documents in an index from an {{ech}} deployment to a {{serverless-full}} project.

For more advanced use cases, including data modification using scripts or ingest pipelines, refer to the [Reindex indices examples](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) and the [Reindex API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex) documentation. 

To migrate data from {{ech}}, you need to include the remote host parameters as shown in the [reindex from remote](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#reindex-from-remote) example and as described here.
:::

## Prerequisites [migrate-reindex-from-remote-prereqs]

- An {{ech}} deployment with data to migrate
- A [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) project configured and running
- An [API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) for authentication with the {{ech}} deployment

  Basic authentication can be used in place of an API key, but an API key is recommended as a more secure option.

:::{important} 
Kibana assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually.
Templates, data stream definitions, and ILM policies, must be in place _before_ you start data migration. 

Visual components, such dashboard and visualizations, can be migrated after you have migrated the data.
:::

## Migrate documents from {{ech}} to {{serverless-short}}

1. In your {{ech}} deployment:

    1. Navigate to the deployment home page and copy the {{es}} endpoint. 

    1. Go to the **Index Management** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    1. Use the search field to identify the indices that you want to migrate.

1. In your {{serverless-short}} project:

    1. Open the Developer Tools [Console](/explore-analyze/query-filter/tools/console.md).

    1. Call the reindex API to migrate your documents.

        Migrate a single index using an API key:
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
        1. Your {{serverless-short}} host URL. This is the {{es}} endpoint that you copied in Step 1.
        1. The API key for authenticating the connection to your {{ech}} deployment.
        1. The source index to copy from your {{ech}} deployment.
        1. The destination index in your {{serverless-short}} project.

        Migrate documents from multilple indices in a single request:
        ```
        POST _reindex
        {
          "source": {
            "remote": {
              "host": "https://<SERVERLESS_HOST_URL>:443", <1>
              "api_key": "<ECH_API_KEY>" <2>
            },
            "index": ["<SOURCE_INDEX01>", "<SOURCE_INDEX02>", "<SOURCE_INDEX03>"] <3>
          },
          "dest": {
            "index": "<DESTINATION_INDEX>" <4>
          }
        }
        ```
        1. Your {{serverless-short}} host URL. This is the {{es}} endpoint that you copied in Step 1.
        1. The API key for authenticating the connection to your {{ech}} deployment.
        1. The source indices to copy from your {{ech}} deployment.
        1. The destination index in your {{serverless-short}} project.

        Migrate selected documents from an index using basic authentication:
        ```
        POST _reindex
        {
          "source": {
            "remote": {
              "host": "https://<SERVERLESS_HOST_URL>:443", <1>
              "username": "<USERNAME>", <2>
              "password": "<PASSWORD>" <3>
            },
            "index": "<SOURCE_INDEX>", <4>
            "query": {
              "match": {
                "<FIELD>": "<VALUE>" <5>
              }
            }
          },
          "dest": {
            "index": "<DESTINATION_INDEX>" <6>
          }
        }
        ```
        1. Your {{serverless-short}} host URL. This is the {{es}} endpoint that you copied in Step 1.
        1. Your {{es}} username and password for authenticating the connection to your {{ech}} deployment.
        1. The source index in your {{ech}} deployment.
        1. The field and value to match when selecting documents from the source index.
        1. The destination index in your {{serverless-short}} project.

    1. Go to the **Index Management** page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    1. Use the search field to confirm that your destination index has been created with the expected number of documents.











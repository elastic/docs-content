---
navigation_title: Find connection details
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/search-space-connection-details.html
applies_to:
  stack:
  serverless:
products:
  - id: kibana
---

# Find connection details [search-space-connection-details]


To connect to your {{es}} deployment, you need either a Cloud ID or an {{es}} endpoint, depending on your deployment type. For secure connections, we recommend using an API key for authentication.

The following sections describe how to find your Cloud ID and create API keys in both {{ecloud}} and {{serverless-short}} deployments.

## Elastic Cloud and self-hosted deployments [_elastic_cloud_and_self_hosted_deployments]


### Find your Cloud ID [find-cloud-id-cloud-self-managed]

1. Go to the {{ecloud}} home page.
2. In the main menu, select **Manage this deployment**.

    :::{image} /solutions/images/kibana-manage-deployment.png
    :alt: manage deployment
    :screenshot:
    :::

3. The Cloud ID is displayed on the right side of the page.

    :::{image} /solutions/images/kibana-cloud-id.png
    :alt: cloud id
    :screenshot:
    :::



### Create an API key [create-an-api-key-cloud-self-managed]

1. To navigate to **API keys**, use the [**global search bar**](../../explore-analyze/find-and-organize/find-apps-and-objects.md).

    :::{image} /solutions/images/kibana-api-keys-search-bar.png
    :alt: api keys search bar
    :screenshot:
    :::

2. Select **Create API key**.

    :::{image} /solutions/images/kibana-click-create-api-key.png
    :alt: click create api key
    :screenshot:
    :::

3. Enter the API key details, and select **Create API key**.
4. Copy and securely store the API key, since it won't appear again.


## Serverless deployments [_serverless_deployments]

### Find your Elasticsearch endpoint [find-cloud-id-serverless]

1. Select the Help icon in the top right corner and then select **Connection Details**.
2. Copy the **Elasticsearch endpoint** from the **Endpoints** tab.

    :::{image} /solutions/images/kibana-serverless-connection-details.png
    :alt: serverless connection details
    :screenshot:
    :::

::::{note}
The **Cloud ID** is also available in the **Connection Details** section. Toggle the **Show Cloud ID** option to view it.

::::


### Create an API key [create-an-api-key-serverless]

1. Go to the serverless project’s home page.
2. Select the settings icon in the **Elasticsearch endpoint** section.
3. On the **API keys** page, select **Create API key**.

    :::{image} /solutions/images/kibana-serverless-create-an-api-key.png
    :alt: serverless create an api key
    :screenshot:
    :::

4. Enter the API key details, and select **Create API key**.
5. Copy and securely store the API key, since it won't appear again.

### Test connection [elasticsearch-get-started-test-connection]

Use [`curl`](https://curl.se) to verify your connection to {{es}}.

In a terminal, assign the {{es}} endpoint and `encoded` API key to the `ES_URL` and `API_KEY` environment variables respectively. `curl` needs access to these values.

For example:

```bash
export ES_URL="https://dda7de7f1d264286a8fc9741c7741690.es.us-east-1.aws.elastic.cloud:443"
export API_KEY="ZFZRbF9Jb0JDMEoxaVhoR2pSa3Q6dExwdmJSaldRTHFXWEp4TFFlR19Hdw=="
```

Next, run the following command to test your connection:

```bash
curl "${ES_URL}" \
  -H "Authorization: ApiKey ${API_KEY}" \
  -H "Content-Type: application/json"
```

You should receive a response similar to the following:

```json
{
  "name" : "serverless",
  "cluster_name" : "dda7de7f1d264286a8fc9741c7741690",
  "cluster_uuid" : "ws0IbTBUQfigmYAVMztkZQ",
  "version" : { ... },
  "tagline" : "You Know, for Search"
}
```

Now you’re ready to start adding data to your {{es-serverless}} project.

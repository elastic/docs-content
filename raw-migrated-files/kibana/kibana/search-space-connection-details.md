---
navigation_title: "Connection details"
---

# Find your connection details [search-space-connection-details]


To connect to your {{es}} deployment, you need either a Cloud ID or an {{es}} endpoint, depending on the deployment type you use. For secure connections, it’s recommended to use an API key for authentication.

* Learn how to [find your Cloud ID](../../../solutions/search/get-started.md#find-cloud-id-cloud-self-managed) for Elastic Cloud or self-hosted deployments.
* Learn how to [create an API key](../../../solutions/search/get-started.md#create-an-api-key-cloud-self-managed) for Elastic Cloud or self-hosted deployments.
* Learn how to [find your {{es}} endpoint or Cloud ID](../../../solutions/search/get-started.md#find-cloud-id-serverless) for a serverless deployment.
* Learn how to [create an API key](../../../solutions/search/get-started.md#create-an-api-key-serverless) for a serverless deployment.


## Elastic Cloud and self-hosted deployments [_elastic_cloud_and_self_hosted_deployments]


### Find your Cloud ID [find-cloud-id-cloud-self-managed]

1. Navigate to the Elastic Cloud home page.
2. In the main menu, click **Manage this deployment**.

    :::{image} ../../../images/kibana-manage-deployment.png
    :alt: manage deployment
    :class: screenshot
    :::

3. The Cloud ID is displayed on the right side of the page.

    :::{image} ../../../images/kibana-cloud-id.png
    :alt: cloud id
    :class: screenshot
    :::



### Create an API key [create-an-api-key-cloud-self-managed]

1. To navigate to **API keys**, use the [**global search bar**](../../../get-started/the-stack.md#kibana-navigation-search).

    :::{image} ../../../images/kibana-api-keys-search-bar.png
    :alt: api keys search bar
    :class: screenshot
    :::

2. Click **Create API key**.

    :::{image} ../../../images/kibana-click-create-api-key.png
    :alt: click create api key
    :class: screenshot
    :::

3. Enter the API key details, and click **Create API key**.
4. Copy and securely store the API key, as it will not be shown again.


## Serverless deployments [_serverless_deployments]


### Find your Elasticsearch endpoint [find-cloud-id-serverless]

1. Navigate to the serverless project’s home page.
2. Scroll down to the **Copy your connection details** section, and copy the **Elasticsearch endpoint**.

    :::{image} ../../../images/kibana-serverless-connection-details.png
    :alt: serverless connection details
    :class: screenshot
    :::


::::{note}
The **Cloud ID** is also displayed in the Copy your connection details section, which you can use with specific client libraries and connectors.

::::



### Create an API key [create-an-api-key-serverless]

1. Navigate to the serverless project’s home page.
2. Scroll down to the **Add an API Key** section, and click **New**.

    :::{image} ../../../images/kibana-serverless-create-an-api-key.png
    :alt: serverless create an api key
    :class: screenshot
    :::

3. Enter the API key details, and click **Create API key**.
4. Copy and securely store the API key, as it will not be shown again.


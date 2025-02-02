---
navigation_title: "Connect to your endpoint"
---

# Connect to your Elasticsearch Serverless endpoint [elasticsearch-connecting-to-es-serverless-endpoint]


::::{tip}
This page assumes you have already [created an {{es-serverless}} project](../../../solutions/search/get-started.md#elasticsearch-get-started-create-project).

::::


Learn how to securely connect to your Elasticsearch Serverless instance.

To connect to your Elasticsearch instance from your applications, client libraries, or tools like `curl`, you’ll need two key pieces of information: an API key and your endpoint URL. This guide shows you how to get these connection details and verify they work.


## Create a new API key [elasticsearch-get-started-create-api-key]

Create an API key to authenticate your requests to the {{es}} APIs. You’ll need an API key for all API requests and client connections.

To create a new API key:

1. On the **Getting Started** page, scroll to **Add an API Key** and select **New**. You can also search for **API keys** in the [global search field](https://www.elastic.co/guide/en/kibana/current/kibana-concepts-analysts.html#_finding_your_apps_and_objects).

    :::{image} ../../../images/serverless-create-an-api-key.png
    :alt: Create an API key.
    :::

2. In **Create API Key**, enter a name for your key and (optionally) set an expiration date.
3. (Optional) Under **Control Security privileges**, you can set specific access permissions for this API key. By default, it has full access to all APIs.
4. (Optional) The **Add metadata** section allows you to add custom key-value pairs to help identify and organize your API keys.
5. Select **Create API Key** to finish.

After creation, you’ll see your API key displayed as an encoded string. Store this encoded API key securely. It is displayed only once and cannot be retrieved later. You will use this encoded API key when sending API requests.

::::{note}
You can’t recover or retrieve a lost API key. Instead, you must delete the key and create a new one.

::::



## Get your {{es}} endpoint URL [elasticsearch-get-started-endpoint]

The endpoint URL is the address for your {{es}} instance. You’ll use this URL together with your API key to make requests to the {{es}} APIs. To find the endpoint URL:

1. On the **Getting Started** page, scroll to **Copy your connection details** section, and find the **Elasticsearch endpoint** field.
2. Copy the URL for the Elasticsearch endpoint.

:::{image} ../../../images/serverless-copy-connection-details.png
:alt: Copy your Elasticsearch endpoint.
:::


## Test connection [elasticsearch-get-started-test-connection]

Use [`curl`](https://curl.se) to verify your connection to {{es}}.

`curl` will need access to your Elasticsearch endpoint and `encoded` API key. Within your terminal, assign these values to the `ES_URL` and `API_KEY` environment variables.

For example:

```bash
export ES_URL="https://dda7de7f1d264286a8fc9741c7741690.es.us-east-1.aws.elastic.cloud:443"
export API_KEY="ZFZRbF9Jb0JDMEoxaVhoR2pSa3Q6dExwdmJSaldRTHFXWEp4TFFlR19Hdw=="
```

Then run the following command to test your connection:

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

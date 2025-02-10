---
navigation_title: Index lifecycle management
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/start-ilm.html
---

# Start index lifecycle management [start-ilm]

% marciw consider moving out of troubleshooting and into how-tos
% marciw or add troubleshooting info from elsewhere

Automatic index lifecycle and data retention management is currently disabled.

In order to start the automatic {{ilm}} service, follow these steps:

:::::::{tab-set}

::::::{tab-item} Elasticsearch Service
In order to start {{ilm}} we need to go to Kibana and execute the [start command](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html).

**Use {{kib}}**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the **Elasticsearch Service** panel, click the name of your deployment.

    ::::{note}
    If the name of your deployment is disabled your {{kib}} instances might be unhealthy, in which case please contact [Elastic Support](https://support.elastic.co). If your deployment doesn’t include {{kib}}, all you need to do is [enable it first](../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
    ::::

3. Open your deployment’s side navigation menu (placed under the Elastic logo in the upper left corner) and go to **Dev Tools > Console**.

    :::{image} ../../images/elasticsearch-reference-kibana-console.png
    :alt: {{kib}} Console
    :class: screenshot
    :::

4. [Start](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html) {{ilm}}:

    ```console
    POST _ilm/start
    ```

    The response will look like this:

    ```console-result
    {
      "acknowledged": true
    }
    ```

5. Verify {{ilm}} is now running:

    ```console
    GET _ilm/status
    ```

    The response will look like this:

    ```console-result
    {
      "operation_mode": "RUNNING"
    }
    ```
::::::

::::::{tab-item} Self-managed
[Start](https://www.elastic.co/guide/en/elasticsearch/reference/current/ilm-start.html) {{ilm}}:

```console
POST _ilm/start
```

The response will look like this:

```console-result
{
  "acknowledged": true
}
```

Verify {{ilm}} is now running:

```console
GET _ilm/status
```

The response will look like this:

```console-result
{
  "operation_mode": "RUNNING"
}
```
::::::

:::::::

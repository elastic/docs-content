<!--
This snippet is in use in the following locations:
- solutions/elasticsearch-solution-project/search-connection-details.md
- solutions/search/set-up/api-key-and-endpoints.md
-->

A personal API key authenticates your client with your own privileges when it sends requests to {{es}}. The following steps show you where to create one for your deployment type.

:::::{applies-switch}

::::{applies-item} serverless: ga

Follow these steps to create an API key for your project.

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your project and select **Open**.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Select the **API key** tab.
4. In the **API key name** field, enter a name, then select **Create API key**.
5. Select an **API key format**: **Encoded** for {{es}} REST API requests, or **{{beats}}** or **{{ls}}** to configure those products.
6. Copy the key. It isn't available after you close the panel.

Keys created here expire in 90 days and carry your own privileges. To set an expiration or restrict privileges, select **Manage API keys** and create the key there instead.

:::{note}
You can also use an [{{ecloud}} API key](/deploy-manage/api-keys/elastic-cloud-api-keys.md) to access {{es}}. Use it when the same key needs to access more than one project, or when you use [{{cps}}](/deploy-manage/cross-project-search-config/cps-config-access-and-scope.md#manage-user-and-api-key-access).
:::
::::

::::{applies-item} ech: ga

Follow these steps to create an API key for {{ech}}.

1. In the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), find your deployment and select **Open**.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Select the **API key** tab.
4. In the **API key name** field, enter a name, then select **Create API key**.
5. Select an **API key format**: **Encoded** for {{es}} REST API requests, or **{{beats}}** or **{{ls}}** to configure those products.
6. Copy the key. It isn't available after you close the panel.

Keys created here expire in 90 days and carry your own privileges. To set an expiration or restrict privileges, select **Manage API keys** and create the key there instead.
::::

::::{applies-item} ece: ga

Follow these steps to create an API key for {{ece}}.

1. Open {{kib}} for your deployment or project.
2. From the **Help menu** {icon}`question`, select **Connection details**.
3. Select the **API key** tab.
4. In the **API key name** field, enter a name, then select **Create API key**.
5. Select an **API key format**: **Encoded** for {{es}} REST API requests, or **{{beats}}** or **{{ls}}** to configure those products.
6. Copy the key. It isn't available after you close the panel.

Keys created here expire in 90 days and carry your own privileges. To set an expiration or restrict privileges, select **Manage API keys** and create the key there instead.
::::

::::{applies-item} {"deployment": {"self": "ga"}}

Follow these steps to create an API key for a self-managed cluster, one you install and manage.

1. Go to the **API keys** management page, using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find it.
2. Select **Create API key**.
3. Enter a name, then select **Create API key**.
4. Copy the key. It isn't available after you leave the page.

Keys created here don't expire unless you add an expiration date.
::::

::::{applies-item} {"deployment": {"eck": "ga"}}

Follow these steps to create an API key for {{eck}}.

1. Go to the **API keys** management page, using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to find it.
2. Select **Create API key**.
3. Enter a name, then select **Create API key**.
4. Copy the key. It isn't available after you leave the page.

Keys created here don't expire unless you add an expiration date.
::::

:::::

For privileges and expiration options, refer to [](/deploy-manage/api-keys.md).

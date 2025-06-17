1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).

2. Under **Hosted deployments**, find your deployment.

:::{tip}
If you have many deployments, you can instead go to the **Hosted deployments** ({{ech}}) page. On that page, you can narrow your deployments by name, ID, or choose from several other filters.
:::

3. Select **Manage**.
4. In the deployment overview, under **Applications**, find the application that you want to test.
5. Click **Copy endpoint**. The value looks something like the following:

```text subs=true
https://my-deployment-d53192.es.{{example-default-dn}}
```

In this endpoint, `my-deployment-d53192` is an alias, and `es` is the product you want to access within your deployment.
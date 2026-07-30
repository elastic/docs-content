1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Under **Serverless projects**, find your projects.

    :::{tip}
    If you have many projects, you can instead go to the **Serverless projects** page. On that page, you can narrow your projects by name, ID, or choose from several other filters.
    :::

3. Select **Manage**.
4. In the project overview, under **Application endpoints, cluster and component IDs**, select the application that you want to access.
5. Under **Private endpoint**, copy the endpoint URL. It looks something like the following:

    ```text subs=true
    https://my-project-d53192.es.{{example-serverless-phz-dn}}
    ```

In this endpoint, `my-project-d53192` is an alias, and `es` is the product you want to access within your project.

You can also connect using the project ID, for example, https://6b111580caaa4a9e84b18ec7c600155e.{{example-serverless-phz-dn}}.

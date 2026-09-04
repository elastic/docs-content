**Find your endpoint**

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co/).
2. Find your deployment in **Hosted deployments**, and select **Manage**.
3. In the **Application endpoints, cluster and component IDs** section, select **Managed OTLP**.
4. Copy the public endpoint value.

**Create an API key**

:::{note}
The {{motlp}} validates API keys using {{product.apm}} application privileges. Index-level privilege scoping is not yet supported, meaning that API keys with custom index-level role descriptors return a `PermissionDenied` error.
:::

:::{dropdown} Using {{kib}}
1. Go to **{{stack-manage-app}}** → **API keys**.
2. Click **Create API key**, enter a name, and enable **Control security privileges**.
3. In the role descriptors box, enter the following privileges:

   ```json
   {
     "otlp_writer": {
       "applications": [
         {
           "application": "apm",
           "resources": ["*"],
           "privileges": ["event:write"]
         }
       ]
     }
   }
   ```

4. Click **Create API key** and copy the encoded value.
:::

:::{dropdown} Using the {{es}} API
Use the [Create API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key) API:

```console
POST /_security/api_key
{
  "name": "otlp-writer",
  "role_descriptors": {
    "otlp_writer": {
      "applications": [
        {
          "application": "apm",
          "resources": ["*"],
          "privileges": ["event:write"]
        }
      ]
    }
  }
}
```

The `event:write` privilege for the `apm` application is the minimum required to send data through the {{motlp}}.
:::

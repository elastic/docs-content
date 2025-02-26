# Custom endpoint aliases [ec-regional-deployment-aliases]

Custom aliases for your deployment endpoints on {{ech}} allow you to have predictable, human-readable URLs that can be shared easily. An alias is unique to only one deployment within a region.


## Create a custom endpoint alias for a deployment [ec-create-regional-deployment-alias] 

::::{note} 
New deployments are assigned a default alias derived from the deployment name. This alias can be modified later, if needed.
::::


To add an alias to an existing deployment:

1. From the **Deployments** menu, select a deployment.
2. Under **Custom endpoint alias**, select **Edit**.
3. Define a new alias. Make sure you choose something meaningful to you.

    ::::{tip} 
    Make the alias as unique as possible to avoid collisions. Aliases might have been already claimed by other users for deployments in the region.
    ::::

4. Select **Update alias**.


## Remove a custom endpoint alias [ec-delete-regional-deployment-alias] 

To remove an alias from your deployment, or if you want to re-assign an alias to another deployment, follow these steps:

1. From the **Deployments** menu, select a deployment.
2. Under **Custom endpoint alias**, select **Edit**.
3. Remove the text from the **Custom endpoint alias** text box.
4. Select **Update alias**.

::::{note} 
After removing an alias, your organisation’s account will hold a claim on it for 30 days. After that period, other users can re-use this alias.
::::



## Using the custom endpoint URL [ec-using-regional-deployment-alias] 

To use your new custom endpoint URL to access your Elastic products, note that each has its own alias to use in place of the default application UUID. For example, if you configured the custom endpoint alias for your deployment to be `test-alias`, the corresponding alias for the Elasticsearch cluster in that deployment is `test-alias.es`.

::::{note} 
You can get the application-specific custom endpoint alias by selecting **Copy endpoint** for that product. It should contain a subdomain for each application type, for example `es`, `kb`, `apm`, or `ent`.
::::



### With the REST Client [ec-rest-regional-deployment-alias] 

* As part of the host name:

    After configuring your custom endpoint alias, select **Copy endpoint** on the deployment overview page, which gives you the fully qualified custom endpoint URL for that product.

* As an HTTP request header:

    Alternatively, you can reach your application by passing the application-specific custom endpoint alias, for example, `test-alias.es`, as the value for the `X-Found-Cluster` HTTP header.



### With the `TransportClient` [ec-transport-regional-deployment-alias] 

While the `TransportClient` is deprecated, your custom endpoint aliases still work with it. Similar to the REST Client, there are two ways to use your custom endpoint alias with the `TransportClient`:

* As part of the host name:

    Similar to HTTP, you can find the fully qualified host on the deployment overview page by selecting **Copy endpoint** next to Elasticsearch. Make sure to remove the unnecessary `https://` prefix as well as the trailing HTTP port.

* As part of the **Settings**:

    Include the application-specific custom endpoint alias as the value for `request.headers.X-Found-Cluster` setting in place of the `clusterId`:

    ```java
    // Build the settings for our client.
    String alias = "test-alias.es"; // Your application-specific custom endpoint alias here
    String region = "us-east-1"; // Your region here
    boolean enableSsl = true;

    Settings settings = Settings.settingsBuilder()
        .put("transport.ping_schedule", "5s")
        //.put("transport.sniff", false) // Disabled by default and *must* be disabled.
        .put("action.bulk.compress", false)
        .put("shield.transport.ssl", enableSsl)
        .put("request.headers.X-Found-Cluster", alias)
        .put("shield.user", "username:password") // your shield username and password
        .build();

    String hostname = alias + "." + region + ".aws.found.io";
    // Instantiate a TransportClient and add the cluster to the list of addresses to connect to.
    // Only port 9343 (SSL-encrypted) is currently supported.
    Client client = TransportClient.builder()
            .addPlugin(ShieldPlugin.class)
            .settings(settings)
            .build()
            .addTransportAddress(new InetSocketTransportAddress(InetAddress.getByName(hostname), 9343));
    ```


For more information on configuring the `TransportClient`, see


## Create a custom domain with NGINX [ec-custom-domains-with-nginx] 

If you don’t get the level of domain customization you’re looking for by using the [custom endpoint aliases](../../../deploy-manage/deploy/elastic-cloud/custom-endpoint-aliases.md), you might consider creating a CNAME record that points to your Elastic Cloud endpoints. However, that can lead to some issues. Instead, setting up your own proxy could provide the desired level of customization.

::::{important} 
The setup described in the following sections is not supported by Elastic, and if your proxy cannot connect to the endpoint, but curl can, we may not be able to help.
::::



### Avoid creating CNAMEs [ec_avoid_creating_cnames] 

To achieve a fully custom domain, you can add a CNAME that points to your Elastic Cloud endpoint. However, this will lead to invalid certificate errors, and moreover, may simply not work. Your Elastic Cloud endpoints already point to a proxy internal to Elastic Cloud, which may not resolve your configured CNAME in the desired way.

So what to do, instead?


### Setting up a proxy [ec_setting_up_a_proxy] 

Here we’ll show you an example of proxying with NGINX, but this can be extrapolated to HAProxy or some other proxy server.

You need to set `proxy_pass` and `proxy_set_header`, and include the `X-Found-Cluster` header with the cluster’s UUID. You can get the cluster ID by clicking the `Copy cluster ID` link on your deployment’s main page.

```
server {
    listen 443 ssl;
    server_name elasticsearch.example.com;

    include /etc/nginx/tls.conf;

    location / {
        proxy_pass        https://<UUID>.eu-west-1.aws.elastic-cloud.com/;
        proxy_set_header  X-Found-Cluster <UUID>;
    }
}
```

This should work for all of your applications, not just {{es}}. To set it up for {{kib}}, for example, you can select `Copy cluster ID` next to {{kib}} on your deployment’s main page to get the correct UUID.

::::{note} 
Doing this for {{kib}} or won't work with Cloud SSO.
::::


To configure `tls.conf in this example, check out [https://ssl-config.mozilla.org/](https://ssl-config.mozilla.org/) for more fields.


---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-regional-deployment-aliases.html
applies_to:
  deployment:
    ece: all
products:
  - id: cloud-enterprise
navigation_title: Custom endpoint aliases
---

# Configure custom endpoint aliases on {{ece}} [ece-regional-deployment-aliases]

Custom aliases for your deployment endpoints on {{ece}} allow you to have predictable, human-readable URLs that can be shared easily.

::::{important}
Before setting up your custom alias, your platform administrator must enable the feature. Check [Enable custom endpoint aliases](enable-custom-endpoint-aliases.md) for more information.
::::

## Create a custom endpoint alias for a deployment [ece-create-regional-deployment-alias]

To add an alias to an existing deployment:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Deployments** menu, select a deployment.
3. Under **Custom endpoint alias**, select **Edit**.
4. Define a new alias. Make sure you choose something meaningful to you.

    ::::{tip}
    Make the alias as unique as possible to avoid collisions. Aliases might have been already claimed by other users for deployments in the region.
    ::::

5. Select **Update alias**.

## Remove a custom endpoint alias [ece-delete-regional-deployment-alias]

To remove an alias from your deployment, or if you want to re-assign an alias to another deployment, follow these steps:

1. [Log into the Cloud UI](log-into-cloud-ui.md).
2. From the **Deployments** menu, select a deployment.
3. Under **Custom endpoint alias**, select **Edit**.
4. Remove the text from the **Custom endpoint alias** text box.
5. Select **Update alias**.

## Using the custom endpoint URL [ece-using-regional-deployment-alias]

To use your new custom endpoint URL to access your Elastic products, note that each has its own alias to use in place of the default application UUID. For example, if you configured the custom endpoint alias for your deployment to be `test-alias`, the corresponding alias for the {{es}} cluster in that deployment is `test-alias.es`.

::::{note}
You can get the application-specific custom endpoint alias by selecting **Copy endpoint** for that product. It should contain a subdomain for each application type, for example `es`, `kb`, `apm`, or `ent`.
::::

### With the REST Client [ece-rest-regional-deployment-alias]

* As part of the host name:

    After configuring your custom endpoint alias, select **Copy endpoint** on the deployment overview page, which gives you the fully qualified custom endpoint URL for that product.

* As an HTTP request header:

    Alternatively, you can reach your application by passing the application-specific custom endpoint alias, for example, `test-alias.es`, as the value for the `X-Found-Cluster` HTTP header.


For more information on setting up a load balancer to ensure proper routing, check [Load balancers](ece-load-balancers.md).


### With the `TransportClient` [ece-transport-regional-deployment-alias]

While the `TransportClient` is deprecated, your custom endpoint aliases still work with it. Similar to the REST Client, there are two ways to use your custom endpoint alias with the `TransportClient`:

* As part of the host name:

    Similar to HTTP, you can find the fully qualified host on the deployment overview page by selecting **Copy endpoint** next to {{es}}. Make sure to remove the unnecessary `https://` prefix as well as the trailing HTTP port.

* As part of the **Settings**:

    Include the application-specific custom endpoint alias as the value for `request.headers.X-Found-Cluster` setting in place of the `clusterId`:

    ```java
    // Build the settings for our client.
    String alias = "test-alias.es"; // Your application-specific custom endpoint alias here
    String region = "us-east-1"; // Your region here
    boolean enableSsl = true;

    Settings settings = Settings.settingsBuilder()
        .put("transport.ping_schedule", "5s")
        //.put("transport.sniff", false) // Disabled by default and must be kept disabled.
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


For more information on configuring the `TransportClient`, see [Configure the Java Transport Client](elasticsearch-java://reference/index.md).


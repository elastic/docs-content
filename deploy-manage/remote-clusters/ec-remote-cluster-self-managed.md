---
navigation_title: To a self-managed cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-remote-cluster-self-managed.html
applies_to:
  deployment:
    ess: ga
    self: ga
products:
  - id: cloud-hosted
---

# Connect {{ech}} deployments to self-managed clusters [ec-remote-cluster-self-managed]

This section explains how to configure a deployment to connect remotely to self-managed clusters.

:::{include} _snippets/terminology.md
:::

## Allow the remote connection [ec_allow_the_remote_connection_4]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::


### Prerequisites and limitations [ec_prerequisites_and_limitations_4]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::


### Create a cross-cluster API key on the remote deployment [ec_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::

### Configure the local deployment [ec_configure_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the Certificate Authority (CA) of the remote environment’s {{es}} remote cluster server, proxy, or load balancing infrastructure is public or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ech-remote-public.md
:::

::::


::::{dropdown} The CA is private
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. On the home page, find your hosted deployment and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Hosted deployments** page to view all of your deployments.

    On the **Hosted deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. Access the **Security** page of the deployment.
4. Select **Remote Connections > Add trusted environment** and choose **Self-managed**. Then click **Next**.
5. Select **API keys** as authentication mechanism and click **Next**.
6. Add a the API key:

    1. Fill both fields.

        * For the **Remote cluster name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.
    3. Repeat these steps for each API key you want to add. For example, if you want to use several clusters of the remote environment for CCR or CCS.

7. Add the CA certificate of the remote self-managed environment.
8. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
9. Select **Create trust** to complete the configuration.
10. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ec-edit-remove-trusted-environment.md#ec-edit-remove-trusted-environment-api-key).

::::
::::::

::::::{tab-item} TLS certificate (deprecated)
### Specify the deployments trusted to be used as remote clusters [ec-trust-self-managed]

A deployment can be configured to trust all or specific deployments in any environment:

1. From the **Security** page, select **Remote Connections > Add trusted environment** and choose **Self-managed**. Then click **Next**.
2. Select **Certificates** as authentication mechanism and click **Next**.
3. Upload the public certificate for the Certificate Authority of the self-managed environment (the one used to sign all the cluster certificates). The certificate needs to be in PEM format and should not contain the private key. If you only have the key in p12 format, then you can create the necessary file like this: `openssl pkcs12 -in elastic-stack-ca.p12 -out newfile.crt.pem -clcerts -nokeys`
4. Select the clusters to trust. There are two options here depending on the subject name of the certificates presented by the nodes in your self managed cluster:

    * Following the {{ecloud}} pattern. In {{ecloud}}, the certificates of all {{es}} nodes follow this convention: `CN = {{node_id}}.node.{{cluster_id}}.cluster.{{scope_id}}`. If you follow the same convention in your self-managed environment, then choose this option and you will be able to select all or specific clusters to trust.
    * If your clusters don’t follow the previous convention for the certificates subject name of your nodes, you can still specify the node name of each of the nodes that should be trusted by this deployment. (Keep in mind that following this convention will simplify the management of this cluster since otherwise this configuration will need to be updated every time the topology of your self-managed cluster changes along with the trust restriction file. For this reason, it is recommended migrating your cluster certificates to follow the previous convention).

        ::::{note}
        Trust management will not work properly in clusters without an `otherName` value specified, as is the case by default in an out-of-the-box [{{es}} installation](../deploy/self-managed/installing-elasticsearch.md). To have the {{es}} certutil generate new certificates with the `otherName` attribute, use the file input with the `cn` attribute as in the example below.
        ::::

5. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
6. Select **Create trust** to complete the configuration.
7. Configure the self-managed cluster to trust this deployment, so that both deployments are configured to trust each other:

   * Download the Certificate Authority used to sign the certificates of your deployment nodes (it can be found in the Security page of your deployment)
   * Trust this CA either using the [setting](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md) `xpack.security.transport.ssl.certificate_authorities` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) or by [adding it to the trust store](../security/different-ca.md).

8. Generate certificates with an `otherName` attribute using the {{es}} certutil. Create a file called `instances.yaml` with all the details of the nodes in your on-premise cluster like below. The `dns` and `ip` settings are optional, but `cn` is mandatory for use with the `trust_restrictions` path setting in the next step. Next, run `./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12 -in instances.yaml` to create new certificates for all the nodes at once. You can then copy the resulting files into each node.

    ```yaml
    instances:
      - name: "node1"
        dns: ["<NODE1_FQDN>"]
        ip: ["192.0.2.1"]
        cn: ["node1.node.1234567abcd.cluster.myscope.account"]
      - name: "node2"
        dns: ["<NODE2_FQDN>"]
        ip: ["192.0.2.2"]
        cn: ["node2.node.1234567abcd.cluster.myscope.account"]
    ```

9. Restrict the trusted clusters to allow only the ones which your self-managed cluster should trust.

    * All the clusters in an {{ecloud}} region are signed by the same certificate authority. Therefore, adding this CA would make the self-managed cluster trust all the clusters in that region, including clusters from other organizations.  This can be limited using the setting `xpack.security.transport.ssl.trust_restrictions.path` which points to a file that limits the certificates to trust based on their `otherName`-attribute.
    * For example, the following file would trust:

      ```yaml
        trust.subject_name:
        - *.node.aaaabbbbaaaabbbb.cluster.1053523734.account <1>
        - *.node.xxxxyyyyxxxxyyyy.cluster.1053523734.account <1>
        - *.node.*.cluster.83988631.account <2>
        - node*.<CLUSTER_FQDN> <3>
      ```
      1. Two specific clusters with cluster ids `aaaabbbbaaaabbbb` and `xxxxyyyyxxxxyyyy` in an ECE environment with Environment ID `1053523734`
      2. Any cluster from an ECE environment with Environment ID `83988631`
      3. The nodes from its own cluster (whose certificates follow a different convention: `CN = node1.<CLUSTER_FQDN>`, `CN = node2.<CLUSTER_FQDN>` and `CN = node3.<CLUSTER_FQDN>`)

::::{tip}
Generate new node certificates for an entire cluster using the file input mode of the certutil.
::::


::::{dropdown} Using the API
You can update a deployment using the appropriate trust settings for the {{es}} payload.

In order to trust a cluster whose nodes present certificates with the subject names: "CN = node1.<CLUSTER_FQDN>", "CN = node2.<CLUSTER_FQDN>" and "CN = node3.<CLUSTER_FQDN>" in a self-managed environment, you could update the trust settings with an additional direct trust relationship like this:

```json
{
  "trust":{
    "accounts":[
      {
         "account_id":"ec38dd0aa45f4a69909ca5c81c27138a",
         "trust_all":true
      }
    ],
    "direct": [
      {
        "type" : "generic",
        "name" : "My Self-managed environment",
        "additional_node_names" : ["node1.<CLUSTER_FQDN>", "node2.<CLUSTER_FQDN>", "node3.<CLUSTER_FQDN>",],
        "certificates" : [
            {
                "pem" : "-----BEGIN CERTIFICATE-----\nMIIDTzCCA...H0=\n-----END CERTIFICATE-----"
            }
         ],
         "trust_all":false
       }
    ]
  }
}
```

::::
::::::
:::::::
You can now connect remotely to the trusted clusters.


## Connect to the remote cluster [ec_connect_to_the_remote_cluster_4]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.


### Using {{kib}} [ec_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ec_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ec_configure_roles_and_users_4]

:::{include} _snippets/configure-roles-and-users.md
:::

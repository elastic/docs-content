---
navigation_title: To a self-managed cluster
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-remote-cluster-self-managed.html
applies_to:
  deployment:
    ece: ga
    self: ga
products:
  - id: cloud-enterprise
---

# Connect {{ece}} deployments to self-managed clusters [ece-remote-cluster-self-managed]

This section explains how to configure a deployment to connect remotely to self-managed clusters.


## Allow the remote connection [ece_allow_the_remote_connection_4]

Before you start, consider the security model that you would prefer to use for authenticating remote connections between clusters, and follow the corresponding steps.

API key
:   For deployments based on {{stack}} 8.14 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model offers administrators of both the local and the remote deployment fine-grained access controls.

TLS certificate (deprecated in {{stack}} 9.0.0)
:   This model uses mutual TLS authentication for cross-cluster operations. User authentication is performed on the local cluster and a user’s role names are passed to the remote cluster. A superuser on the local deployment gains total read access to the remote deployment, so it is only suitable for deployments that are in the same security domain.

:::::::{tab-set}

::::::{tab-item} API key
API key authentication enables a local cluster to authenticate itself with a remote cluster via a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key and grants access, based on the API key’s privileges.

All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search and/or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. Note it is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).


### Prerequisites and limitations [ece_prerequisites_and_limitations_4]

* The local and remote deployments must be on {{stack}} 8.14 or later.


### Create a cross-cluster API key on the remote deployment [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

* On the deployment you will use as remote, use the [{{es}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) or [{{kib}}](../api-keys/elasticsearch-api-keys.md) to create a cross-cluster API key. Configure it with access to the indices you want to use for {{ccs}} or {{ccr}}.
* Copy the encoded key (`encoded` in the response) to a safe location. You will need it in the next step.


### Configure the local deployment [ece_configure_the_local_deployment_2]

The API key created previously will be used by the local deployment to authenticate with the corresponding set of permissions to the remote deployment. For that, you need to add the API key to the local deployment’s keystore.

The steps to follow depend on whether the Certificate Authority (CA) of the remote environment’s {{es}} HTTPS server, proxy or, load balancing infrastructure is public or private.

::::{dropdown} The CA is public
1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the deployment menu, select **Security**.
4. Locate **Remote Connections > Trust management > Connections using API keys** and select **Add API key**.

    1. Fill both fields.

        * For the **Remote cluster name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Cross-cluster API key**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.

5. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ece-edit-remove-trusted-environment.md#ece-edit-remove-trusted-environment-api-key).

::::


::::{dropdown} The CA is private
1. [Log into the Cloud UI](../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the **Deployments** page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. Access the **Security** page of the deployment.
4. Select **Remote Connections > Add trusted environment** and choose **Self-managed**. Then click **Next**.
5. Select **API keys** as authentication mechanism and click **Next**.
6. Add a the API key:

    1. Fill both fields.

        * For the **Setting name**, enter the the alias of your choice. You will use this alias to connect to the remote cluster later. It must be lowercase and only contain letters, numbers, dashes and underscores.
        * For the **Secret**, paste the encoded cross-cluster API key.

    2. Click **Add** to save the API key to the keystore.
    3. Repeat these steps for each API key you want to add. For example, if you want to use several clusters of the remote environment for CCR or CCS.

7. Add the CA certificate of the remote self-managed environment.
8. Provide a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.
9. Select **Create trust** to complete the configuration.
10. Restart the local deployment to reload the keystore with its new setting. To do that, go to the deployment’s main page (named after your deployment’s name), locate the **Actions** menu, and select **Restart {{es}}**.<br>

    ::::{note}
    If the local deployment runs on version 8.14 or greater, you no longer need to perform this step because the keystore is reloaded automatically with the new API keys.
    ::::


If you need to update the remote connection with different permissions later, refer to [Change a cross-cluster API key used for a remote connection](ece-edit-remove-trusted-environment.md#ece-edit-remove-trusted-environment-api-key).

::::
::::::

::::::{tab-item} TLS certificate (deprecated)
### Specify the deployments trusted to be used as remote clusters [ece-trust-self-managed]

A deployment can be configured to trust all or specific deployments in any environment:

1. From the **Security** menu, select **Remote Connections > Add trusted environment** and choose **Self-managed**, then click **Next**.
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

    * All the clusters in your {{ece}} environment are signed by the same certificate authority. Therefore, adding this CA would make the self-managed cluster trust all your clusters in your ECE environment. This should be limited using the setting `xpack.security.transport.ssl.trust_restrictions.path` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md), which points to a file that limits the certificates to trust based on their `otherName`-attribute.
    * For example, the following file would trust:

      ```yaml
        trust.subject_name:
        - *.node.aaaabbbbaaaabbbb.cluster.1053523734.account <1>
        - *.node.xxxxyyyyxxxxyyyy.cluster.1053523734.account <1>
        - *.node.*.cluster.83988631.account <2>
        - node*.<CLUSTER_FQDN> <3>
      ```
      1. two specific clusters with cluster ids `aaaabbbbaaaabbbb` and `xxxxyyyyxxxxyyyy` in an ECE environment with Environment ID `1053523734`
      2. any cluster from an ECE environment with Environment ID `83988631`
      3. the nodes from its own cluster (whose certificates follow a different convention: `CN = node1.<CLUSTER_FQDN>`, `CN = node2.<CLUSTER_FQDN>` and `CN = node3.<CLUSTER_FQDN>`)

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


## Connect to the remote cluster [ece_connect_to_the_remote_cluster_4]

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.

::::{note}
This configuration of remote clusters uses the [Proxy mode](/deploy-manage/remote-clusters/remote-clusters-self-managed.md#proxy-mode) and requires the ECE allocators to be able to connect to the remote address endpoint.
::::

### Using {{kib}} [ece_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ece_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ece_configure_roles_and_users_4]

To use a remote cluster for {{ccr}} or {{ccs}}, you need to create user roles with [remote indices privileges](../users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) on the local cluster. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key).
---
navigation_title: To an external cluster or deployment
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
sub:
  local_type_generic: cluster
  remote_type_generic: deployment or cluster
---

# Connect an ECK-managed cluster to an external cluster or deployment

These steps describe how to configure a remote cluster connection from an {{es}} cluster managed by {{eck}} (ECK) to an external {{es}} cluster, not managed by ECK. The remote cluster can be self-managed, or part of an {{ech}} (ECH) or {{ece}} (ECE) deployment.

After the connection is established, you’ll be able to [run {{ccs-init}} queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up {{ccr-init}}](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

:::{include} _snippets/terminology.md
:::

In this scenario, most of the configuration must be performed manually, as {{eck}} cannot orchestrate the setup across both clusters. For fully automated configuration between ECK-managed clusters, refer to [](./eck-remote-clusters.md).

For other remote cluster scenarios with ECK, such as connecting clusters in different ECK environments, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md#eck-rcs-setup).

## Allow the remote connection

:::{include} _snippets/apikeys-intro.md
:::

:::{note}
For the deprecated [TLS certificate–based authentication](./security-models.md#tls-certificate-authentication) model, the steps to allow the remote connection and establish mutual trust between clusters are effectively the same regardless of which cluster acts as the local or remote one. Once trust is established, remote connections can be configured in either direction.

Because of this, if you want to configure TLS certificate–based authentication for any of the scenarios covered in this guide, refer to:

* [](./ec-enable-ccs-for-eck.md)
* [](./ece-enable-ccs-for-eck.md)
* [](./self-remote-cluster-eck.md)
:::

### Enable the remote cluster server interface on the remote cluster [enable-rcs]

Follow the steps corresponding to the deployment type of your remote cluster:

:::::::{applies-switch}

::::::{applies-item} ess:
If the remote cluster is part of an {{ech}} deployment, the remote cluster server is enabled by default and it uses a publicly trusted certificate provided by the platform proxies. Therefore, you can skip this step.
::::::

::::::{applies-item} ece:
If the remote cluster is part of an {{ece}} deployment, the remote cluster server is enabled by default, and secured with TLS certificates.

Depending on the type of certificate used by the ECE proxies or load-balancing layer, the local cluster requires the associated certificate authority (CA) to establish trust:

* If your ECE proxies use publicly trusted certificates, no additional CA is required.

* If your ECE proxies use certificates signed by a private CA, retrieve the root CA from the [ECE Cloud UI](/deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md):

  1. In the remote ECE environment, go to **Platform > Settings > TLS certificates**.

  2. Under **Proxy**, select **Show certificate chain**.

  3. Click **Copy root certificate** and paste it into a new file. The root certificate is the last certificate shown in the chain.

  4. Save the file as `.crt`, and keep it available for the trust configuration on the local cluster.
::::::

::::::{applies-item} self:

#### Enable and secure the remote cluster server

By default, the remote cluster server interface is not enabled on self-managed clusters. Follow the steps below to enable the interface:

:::{include} _snippets/self_rcs_enable.md
:::

#### Retrieve the certificate authority (CA)

    If the remote cluster server is exposed with a certificate signed by private certificate authority (CA), save the corresponding `ca.crt` file. It is required when configuring trust on the local cluster.

::::::
:::::::

### Create a cross-cluster API key on the remote cluster

:::{include} _snippets/apikeys-create-key.md
:::

### Configure the local cluster [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the certificate authority (CA) presented by the remote cluster server, proxy, or load-balancing infrastructure is publicly trusted or private.

:::{note}
If the remote cluster is part of an {{ech}} deployment, follow the **The CA is public** path. {{ech}} proxies use publicly trusted certificates, so no CA configuration is required.
:::

::::{dropdown} The CA is public

1. **Store the API key encoded value in a Secret**

    :::{include} _snippets/eck_apikey_secret.md
    :::

2. **Configure the {{es}} resource**

    Update the {{es}} manifest to:
    * Load the API key from the previously created secret using [`secureSettings`](/deploy-manage/security/k8s-secure-settings.md)
    * Enable the remote cluster SSL client in the `config` section of each `nodeSet`

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: <local-cluster-name>
    spec:
      version: {{version.stack}}
      secureSettings:
        - secretName: remote-api-keys <1>
      nodeSets:
        - name: default
          count: 3
          config:
            xpack:
              security:
                remote_cluster_client:
                  ssl:
                    enabled: true <2>
    ```
    1. The secret name must match the secret created in the previous step.
    2. Repeat this configuration for all `nodeSets`.
::::

::::{dropdown} The CA is private

1. **Store the API key encoded value in a Secret**

    :::{include} _snippets/eck_apikey_secret.md
    :::

2. **Store the CA certificate in a ConfigMap or Secret**

    Store the CA certificate [retrieved earlier](#enable-rcs) in a ConfigMap or Secret. The following example creates a ConfigMap named `remote-ca` that stores the content of a local file (`my-ca.crt`) under the `remote-cluster-ca.crt` key:

    ```sh
    kubectl create configmap remote-ca -n <namespace> --from-file=remote-cluster-ca.crt=my-ca.crt
    ```

3. **Configure the {{es}} resource**

    Update the {{es}} manifest to:

    * Load the API key from the previously created secret using [`secureSettings`](/deploy-manage/security/k8s-secure-settings.md)
    * Mount the CA certificate from the previously created ConfigMap [as a custom file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret) in the {{es}} Pods
    * Enable and configure the remote cluster SSL client in the `config` section of each `nodeSet`

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: <local-cluster-name>
    spec:
      version: {{version.stack}}
      secureSettings:
        - secretName: remote-api-keys
      nodeSets: <1>
        - name: default
          count: 3
          config:
            xpack:
              security:
                remote_cluster_client:
                  ssl:
                    enabled: true
                    certificate_authorities: [ "remote-certs/remote-cluster-ca.crt" ] <2>
          podTemplate:
            spec:
              containers:
              - name: elasticsearch
                volumeMounts:
                - name: remote-ca
                  mountPath: /usr/share/elasticsearch/config/remote-certs
              volumes:
              - name: remote-ca
                configMap:
                  name: remote-ca <3>
    ```
    1. Repeat this configuration for all `nodeSets`.
    2. The file name must match the `key` of the ConfigMap that contains the CA certificate.
    3. Must match the name of the ConfigMap created previously.
::::

## Connect to the remote cluster

On the local cluster, add the remote cluster using {{kib}} or the {{es}} API.

:::{admonition} About connection modes
This guide uses the `proxy` connection mode, which is the only practical option when connecting to {{ech}}, {{ece}}, or {{eck}} clusters from outside their Kubernetes environment.

If the remote cluster is self-managed (or another ECK cluster within the same Kubernetes network) and the local cluster can reach the remote nodes’ publish addresses directly, you can use `sniff` mode instead. Refer to [connection modes](./connection-modes.md) documentation for details on each mode and their connectivity requirements.
:::

### Using {{kib}} [using-kibana]

% ECK and self-managed clusters present a different Kibana UI when adding remote clusters than ECE/ECH deployments

1. Go to the **Remote Clusters** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Add a remote cluster**.
3. In **Select connection type**, choose the **API keys** authentication mechanism and click **Next**.
4. Set the **Remote cluster name**: This name must match the `<remote-cluster-name>` you configured when [adding the API key in the local cluster's keystore](#configure-local-cluster).

5. In **Connection mode**, select **Manually enter proxy address and server name** to enable the proxy mode and fill in the following fields:

    * **Proxy address**: Identify the endpoint of the remote cluster, including the hostname, FQDN, or IP address, and the port:
        
      :::{include} _snippets/eck_rcs_external_endpoint_switch.md
      :::

      Starting with {{kib}} 9.2, this field also supports IPv6 addresses. When using an IPv6 address, enclose it in square brackets followed by the port number. For example: `[2001:db8::1]:9443`.

    * **Server name (optional)**: Specify a value if the TLS certificate presented by the remote cluster is signed for a different name than the remote address.

5. Click **Next**.
6. In **Confirm setup**, click **Add remote cluster** (you have already established trust in a previous step).

### Using the {{es}} API [using-api]

To add a remote cluster, use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). Configure the following fields:

* **Remote cluster alias**: The cluster alias must match the `<remote-cluster-name>` you configured when [adding the API key in the local cluster's keystore](#configure-local-cluster).
* **mode**: Use `proxy` mode in almost all cases. `sniff` mode is only applicable when the remote cluster is self-managed and the local cluster can reach the nodes’ publish addresses directly.
* **proxy_address**: Identify the endpoint of the remote cluster, including the hostname, FQDN, or IP address, and the port. Both IPv4 and IPv6 addresses are supported.

  :::{include} _snippets/eck_rcs_external_endpoint_switch.md
  :::

  When using an IPv6 address, enclose it in square brackets followed by the port number. For example: `[2001:db8::1]:9443`.

* **server_name**: Specify a value if the certificate presented by the remote cluster is signed for a different name than the proxy_address.

This is an example of the API call to add or update a remote cluster:

```json
PUT /_cluster/settings
{
  "persistent": {
    "cluster": {
      "remote": {
        "alias-for-my-remote-cluster": { // Align the alias with the remote cluster name used when adding the API key as a secure setting.
          "mode":"proxy",
          "proxy_address": "<REMOTE_CLUSTER_ADDRESS>:9443",
          "server_name": "<REMOTE_CLUSTER_SERVER_NAME>"
        }
      }
    }
  }
}
```

For a full list of available client connection settings, refer to the [remote cluster settings reference](elasticsearch://reference/elasticsearch/configuration-reference/remote-clusters.md).

## Verify the remote cluster connection

From the local cluster, check the status of the connection to the remote cluster. If you encounter issues, refer to the [Troubleshooting guide](/troubleshoot/elasticsearch/remote-clusters.md).

```console
GET _remote/info
```

In the response, verify that connected is `true`:

```
{
  "<remote-alias>": {
    "connected": true,
    "mode": "proxy",
    "proxy_address": "<REMOTE_CLUSTER_ADDRESS>:9443",
    "server_name": "<REMOTE_CLUSTER_SERVER_NAME>",
    "num_proxy_sockets_connected": 18,
    "max_proxy_socket_connections": 18,
    "initial_connect_timeout": "30s",
    "skip_unavailable": true,
    "cluster_credentials": "::es_redacted::"
  }
}
```

## Configure roles and users

:::{include} _snippets/configure-roles-and-users.md
:::


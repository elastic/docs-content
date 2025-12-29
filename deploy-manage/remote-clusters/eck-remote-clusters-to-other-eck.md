---
navigation_title: To a different ECK environment
applies_to:
  deployment:
    eck: ga
products:
  - id: cloud-kubernetes
sub:
  local_type_generic: cluster
  remote_type_generic: deployment or cluster
---

# Connect to {{es}} clusters in a different {{eck}} environment

These steps describe how to configure a remote cluster connection between {{es}} clusters handled by different {{eck}} (ECK) operators.

After the connection is established, you’ll be able to [run {{ccs-init}} queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up {{ccr-init}}](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

:::{include} _snippets/terminology.md
:::

In this scenario, most of the configuration must be performed manually, as {{eck}} cannot orchestrate the setup across both clusters. For fully automated configuration between ECK-managed clusters, refer to [Connect to {{es}} clusters in the same ECK environment](./eck-remote-clusters.md).

For other remote cluster scenarios with ECK, refer to [Remote clusters on ECK](./eck-remote-clusters-landing.md#eck-rcs-setup).

## Allow the remote connection

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

#### Prerequisites and limitations

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::

#### Enable the remote cluster server interface on the remote ECK cluster [enable-rcs]

:::{include} _snippets/eck_rcs_enable.md
:::

#### Configure external access to the remote cluster server interface

:::{include} _snippets/eck_rcs_expose.md
:::

#### Retrieve the ECK-managed CA certificate of the remote cluster server [fetch-ca-cert]

:::{include} _snippets/eck_rcs_retrieve_ca.md
:::

#### Create a cross-cluster API key on the remote cluster

:::{include} _snippets/apikeys-create-key.md
:::

#### Configure the local deployment [configure-local-cluster]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the certificate authority (CA) presented by the remote cluster server, proxy, or load-balancing infrastructure is publicly trusted or private.

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
::::::

::::::{tab-item} TLS certificate (deprecated)

:::{include} _snippets/tlscerts-intro.md
:::

#### Make sure both clusters trust each other's certificate authority [mtls-setup-eck]

:::{include} _snippets/eck_rcs_mtls_intro.md
:::

The following steps assume that the local and remote clusters are handled by different ECK installations.

1. Extract and save the transport CAs of both clusters:

    :::{include} _snippets/eck_rcs_certs_retrieve_ca.md
    :::

2. Configure the local cluster to trust the transport CA of the remote cluster:

    1. In the Kubernetes cluster and namespace where the local cluster is running, create a config map with the CA certificate of the remote cluster you extracted previously:

        ```sh
        kubectl create configmap remote-certs --from-file=ca.crt=<quickstart_transport_ca.crt> <1>
        ```
        1. Substitute `<quickstart_transport_ca.crt>` with the name of the file you saved in the previous step.

    2. Configure the {{es}} resource manifest to trust the previous config map through the `spec.transport.tls.certificate_authorities` setting:

        ```yaml subs=true
        apiVersion: elasticsearch.k8s.elastic.co/v1
        kind: Elasticsearch
        metadata:
          name: <local-cluster-name>
        spec:
          version: {{version.stack}}
          transport:
            tls:
              certificateAuthorities:
                configMapName: remote-certs
          nodeSets:
          - count: 3
            name: default
        ```
    
3. Repeat the previous step for the remote cluster to trust the CA of the local cluster.

#### Configure external access to the transport interface of the remote cluster

:::{include} _snippets/eck_expose_transport.md
:::

::::::
:::::::

## Connect to the remote cluster

:::{include} _snippets/eck_rcs_connect_intro.md
:::

:::{admonition} About connection modes
This guide uses the `proxy` connection mode, connecting to the remote cluster through the Kubernetes service abstraction.

If the remote cluster resides in the same Kubernetes cluster as the local cluster, and if the local cluster can reach the remote nodes’ publish addresses directly, you can use `sniff` mode instead. Refer to [connection modes](./connection-modes.md) documentation for details on each mode and their connectivity requirements.
:::

### Using {{kib}}

:::{include} _snippets/rcs-self-kibana-to-self.md
:::

### Using the {{es}} API

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Verify remote cluster connection

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


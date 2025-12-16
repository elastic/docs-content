---
navigation_title: To {{eck}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-enable-ccs-for-eck.html
applies_to:
  deployment:
    ece: ga
    eck: ga
products:
  - id: cloud-enterprise
sub:
  remote_type: Self-managed
---

# Connect {{ece}} deployments to {{eck}} clusters [ece-enable-ccs-for-eck]

These steps describe how to configure remote clusters between an {{es}} cluster in {{ece}} (ECE) and an {{es}} cluster running within [{{eck}} (ECK)](/deploy-manage/deploy/cloud-on-k8s.md). Once that's done, you'll be able to [run CCS queries from {{es}}](/explore-analyze/cross-cluster-search.md) or [set up CCR](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).

:::{include} _snippets/terminology.md
:::


## Allow the remote connection [ece_allow_the_remote_connection_4]

:::{include} _snippets/allow-connection-intro.md
:::

:::::::{tab-set}

::::::{tab-item} API key

:::{include} _snippets/apikeys-intro.md
:::

### Prerequisites and limitations [ece_prerequisites_and_limitations_4]

:::{include} _snippets/apikeys-prerequisites-limitations.md
:::

### Enable the remote cluster server interface on the remote ECK cluster

:::{include} _snippets/eck_rcs_enable.md
:::

### Configure external access to the remote cluster server interface

:::{include} _snippets/eck_rcs_expose.md
:::


### Retrieve the ECK-managed CA certificate of the remote cluster server [fetch-ca-cert]

:::{include} _snippets/eck_rcs_retrieve_ca.md
:::

### Create a cross-cluster API key on the remote cluster [ece_create_a_cross_cluster_api_key_on_the_remote_deployment_4]

:::{include} _snippets/apikeys-create-key.md
:::


### Configure the local deployment [ece_configure_the_local_deployment_2]

:::{include} _snippets/apikeys-local-config-intro.md
:::

The steps to follow depend on whether the certificate authority (CA) presented by the remote cluster server, proxy, or load-balancing infrastructure is publicly trusted or private.

::::{dropdown} The CA is public

:::{include} _snippets/apikeys-local-ece-remote-public.md
:::

::::

::::{dropdown} The CA is private (ECK-managed transport certificates)

When adding the CA certificate in the next steps, use either the ECK-managed transport CA obtained [previously](#fetch-ca-cert), or the CA of the component that terminates TLS connections to clients.

:::{include} _snippets/apikeys-local-ece-remote-private.md
:::
::::

::::::

::::::{tab-item} TLS certificate (deprecated)
### Establish mutual trust between the clusters [ece_establish_trust_between_two_clusters]

When using TLS certificates-based authentication, the first step is to establish trust between the two clusters, by adding the CA certificate and trust details of each environment into the other.

#### Establish trust in the {{ece}} cluster [ece_establish_trust_in_the_elastic_cloud_enterprise_cluster]

1. Save the ECK CA certificate to a file. For a cluster named `quickstart`, run:

    ```sh
    kubectl get secret quickstart-es-transport-certs-public -o go-template='{{index .data "ca.crt" | base64decode}}' > eck.ca.crt
    ```


1. Update the trust settings for the {{ece}} deployment. Follow the steps provided in [Access clusters of a self-managed environment](ece-remote-cluster-self-managed.md), and specifically the first three steps in **Specify the deployments trusted to be used as remote clusters** using TLS certificate as security model.

    * Use the certificate file saved in the first step.
    * Select the {{ecloud}} pattern and enter `default.es.local` for the `Scope ID`.

2. Select `Save` and then download the CA Certificate and `trust.yml` file. These files can also be retrieved in the `Security` page of the deployment. You will use these files in the next set of steps.


#### Establish trust in the ECK cluster [ece_establish_trust_in_the_eck_cluster]

1. Upload the {{ece}} certificate (that you downloaded in the last step of the previous section) as a Kubernetes secret.

    ```sh
    kubectl create secret generic ce-aws-cert --from-file=<path to certificate file>
    ```

2. Upload the `trust.yml` file (that you downloaded in the last step of the previous section) as a Kubernetes config map.

    ```sh
    kubectl create configmap quickstart-trust --from-file=<path to trust.yml>
    ```

3. Edit the {{es}} kubernetes resource to ensure the following sections are included. This assumes the {{es}} deployment is named `quickstart`. Make sure to replace the `CA-Certificate-Filename` placeholder with the correct value. Note that these configuration changes are required for all `nodeSets`. Applying this change requires all pods in all `nodeSets` to be deleted and recreated, which might take quite a while to complete.

    ```yaml
    spec:
      nodeSets:
      - config:
           xpack.security.transport.ssl.certificate_authorities:
           - /usr/share/elasticsearch/config/other/<CA-Certificate-Filename>
           xpack.security.transport.ssl.trust_restrictions.path:  /usr/share/elasticsearch/config/trust-filter/trust.yml
        podTemplate:
          spec:
            containers:
            - name: elasticsearch
               volumeMounts:
               - mountPath: /usr/share/elasticsearch/config/other
                  name: ce-aws-cert
               - mountPath: /usr/share/elasticsearch/config/trust-filter
                 name: quickstart-trust
            volumes:
            - name: ce-aws-cert
               secret:
                 secretName: ce-aws-cert
            - configMap:
                 name: quickstart-trust
               name: quickstart-trust
    ```

### Configure external access to the transport interface of your ECK cluster

:::{include} _snippets/eck_expose_transport.md
:::

::::::
:::::::

## Connect to the remote cluster [ece_connect_to_the_remote_cluster_4]

:::{include} _snippets/eck_rcs_connect_intro.md
:::

### Using {{kib}} [ece_using_kibana_4]

:::{include} _snippets/rcs-kibana-api-snippet-self.md
:::

### Using the {{es}} API [ece_using_the_elasticsearch_api_4]

:::{include} _snippets/rcs-elasticsearch-api-snippet-self.md
:::

## Configure roles and users [ece_configure_roles_and_users_4]

:::{include} _snippets/configure-roles-and-users.md
:::

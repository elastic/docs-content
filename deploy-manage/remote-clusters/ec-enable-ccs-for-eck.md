---
navigation_title: To {{eck}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs-for-eck.html
applies_to:
  deployment:
    ess: ga
    eck: ga
products:
  - id: cloud-hosted
---

# Connect {{ech}} deployments to {{eck}} clusters [ec-enable-ccs-for-eck]

These steps describe how to configure remote clusters between an {{es}} cluster in {{ech}} (ECH) and an {{es}} cluster running within [{{eck}} (ECK)](/deploy-manage/deploy/cloud-on-k8s.md). Once that’s done, you’ll be able to [run CCS queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up CCR](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).


## Establish trust between the two clusters [ec_establish_trust_between_two_clusters]

The first step is to establish trust between the two clusters, by adding the CA certificate and trust details of each environment into the other.

This guide uses TLS certificates to secure remote cluster connections and follows a similar approach to [Access clusters of a self-managed environment](ec-remote-cluster-self-managed.md).

### Establish trust in the ECH cluster [ec_establish_trust_in_the_elasticsearch_service_cluster]

To configure trust in the ECH deployment:

1. Save the {{es}} transport CA certificate of your ECK deployment. For an {{es}} cluster named `quickstart`, run:

    ```sh
    kubectl get secret quickstart-es-transport-certs-public -o go-template='{{index .data "ca.crt" | base64decode}}' > eck-ca.crt
    ```

    This command saves the certificate to `eck-ca.crt`.

2. Update the trust settings for the {{ech}} deployment:

    1. From the **Security** menu, select **Remote Connections > Add trusted environment**, choose **Self-managed**, and click **Next**.

    2. Select **Certificates** as the authentication mechanism and click **Next**.

    3. In **Add trusted CA certificate**, upload the `eck-ca.crt` file retrieved in the previous step.

    4. In **Select trusted clusters**, configure the following:
        * Select **Trust clusters whose Common Name follows the Elastic pattern**.
        * For **Scope ID**, enter `<kubernetes-namespace>.es.local`, replacing `<kubernetes-namespace>` with the namespace of your ECK cluster.
        * In **Trust**, select **All deployments**.

    5. In **Name the environment**, enter a name for the trusted environment. That name will appear in the trust summary of your deployment’s **Security** page.

    6. Select **Create trust** to complete the configuration.

    7. On the confirmation screen, when prompted **Have you already set up trust from the other environment?**, select **No, I have NOT set up trust from the other environment yet**. Download both the ECH deployment CA certificate and the `trust.yml` file. These files can also be retrieved from the **Security** page of the deployment. You’ll use these files to configure trust in the ECK deployment.

### Update the downloaded `trust.yml` file for ECK compatibility

The `trust.yml` file you downloaded from the Cloud UI includes a subject name pattern that isn't valid for your ECK cluster. Before using it in your ECK cluster, you need to update the file with the pattern that matches your cluster.

Replace the line corresponding to the `Scope ID` you entered when configuring trust in the ECH deployment:

```sh
"*.node.*.cluster.<kubernetes-namespace>.es.local.account"
```

Replace it with the correct subject name for your ECK cluster. The new subject name should use the following pattern:

```sh
"*.node.<cluster-name>.<kubernetes-namespace>.es.local"
```

::::{important}
If you don’t update this entry, {{es}} nodes of your ECK deployment might fail to start or join the cluster due to failed trust validation.
::::

For example, the original downloaded file might contain the following:

```yaml
trust.subject_name:
  - "*.node.2dc556bb4bd040e00d0135683b66a2f6.cluster.1075999151.account" <1>
  - "*.node.*.cluster.<kubernetes-namespace>.es.local.account" <2>
```
1. This entry identifies your ECH deployment. Leave it unchanged.
2. This entry identifies your ECK deployment incorrectly, and must be updated.

For an ECK cluster named `quickstart` in the `default` namespace, the updated file should look like the following:

```yaml
trust.subject_name:
  - "*.node.2dc556bb4bd040e89d0135683b66a2f6.cluster.1075708151.account"
  - "*.node.quickstart.default.es.local"
```

Apply the changes and save the `trust.yml` file.


### Establish trust in the ECK cluster [ec_establish_trust_in_the_eck_cluster]

To configure trust in the ECK deployment:

1. In the same namespace as your {{es}} cluster, upload the ECH CA certificate that you downloaded from the Cloud UI as a Kubernetes secret:

    ```sh
    kubectl create secret generic remote-ech-ca --from-file=ca.crt=<path-to-CA-certificate-file> -n <namespace>
    ```

2. In the same namespace as your {{es}} cluster, upload the updated `trust.yml` file as a Kubernetes config map. For a cluster named `quickstart`, run the following command:

    ```sh
    kubectl create configmap quickstart-trust-ech --from-file=trust.yml=<path-to-trust.yml> -n <namespace>
    ```

3. Edit the {{es}} Kubernetes resource to reference the ECH CA certificate and trust.yml file. This example assumes that the Kubernetes secret and config map created in the previous steps are named `remote-ech-ca` and `quickstart-trust-ech`, respectively:

    ::::{note}
    Apply these changes to all `nodeSets` of your cluster. Updating this configuration will restart all {{es}} pods, which might take some time to complete.
    ::::

    ```yaml
    spec:
      nodeSets:
      - config:
          xpack.security.transport.ssl.certificate_authorities:
            - /usr/share/elasticsearch/config/ech-ca/ca.crt
          xpack.security.transport.ssl.trust_restrictions.path: /usr/share/elasticsearch/config/trust-filter/trust.yml
        podTemplate:
          spec:
            containers:
            - name: elasticsearch
              volumeMounts:
                - mountPath: /usr/share/elasticsearch/config/ech-ca
                  name: remote-ech-ca
                - mountPath: /usr/share/elasticsearch/config/trust-filter
                  name: eck-ech-trust
            volumes:
              - name: remote-ech-ca
                secret:
                  secretName: remote-ech-ca <1>
              - name: eck-ech-trust
                configMap:
                  name: quickstart-trust-ech <2>
    ```
    1. Ensure `secretName` matches the name of the Secret you created earlier.
    2. Ensure `name` matches the name of the ConfigMap you created earlier.

## Set up CCS/R [ec_setup_ccsr]

Now that trust has been established, you can set up CCS/R from the ECK cluster to the ECH cluster or from the ECH cluster to the ECK cluster.

### ECK Cluster to {{ech}} cluster [ec_eck_cluster_to_elasticsearch_service_cluster]

Configure the ECH deployment as a remote on your ECK cluster following [](ec-remote-cluster-self-managed.md#ec_connect_to_the_remote_cluster_4) steps.

### {{ech}} cluster to ECK Cluster [ec_elasticsearch_service_cluster_to_eck_cluster]

Follow the steps outlined in the [ECK documentation](/deploy-manage/remote-clusters/eck-remote-clusters.md#k8s_configure_the_remote_cluster_connection_through_the_elasticsearch_rest_api) to expose the transport layer of your ECK cluster, and configure the ECK cluster as a remote of your ECH deployment.

---
navigation_title: With {{eck}}
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs-for-eck.html
applies_to:
  deployment:
    ess: ga
    eck: ga
products:
  - id: cloud-hosted
---

# Remote clusters between {{ech}} and ECK [ec-enable-ccs-for-eck]

These steps describe how to configure remote clusters between an {{es}} cluster in {{ech}} and an {{es}} cluster running within [{{eck}} (ECK)](/deploy-manage/deploy/cloud-on-k8s.md). Once that’s done, you’ll be able to [run CCS queries from {{es}}](/solutions/search/cross-cluster-search.md) or [set up CCR](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md).


## Establish trust between two clusters [ec_establish_trust_between_two_clusters]

The first step is to establish trust between the two clusters.


### Establish trust in the {{ech}} cluster [ec_establish_trust_in_the_elasticsearch_service_cluster]

1. Save the ECK CA certificate to a file. For a cluster named `quickstart`, run:

    ```sh
    kubectl get secret quickstart-es-transport-certs-public -o go-template='{{index .data "ca.crt" | base64decode}}' > eck.ca.crt
    ```


1. Update the trust settings for the {{ech}} deployment. Follow the steps provided in [Access clusters of a self-managed environment](ec-remote-cluster-self-managed.md), and specifically the first three steps in **Specify the deployments trusted to be used as remote clusters** using TLS certificate as security model.

    * Use the certificate file saved in the first step.
    * Select the {{ecloud}} pattern and enter `default.es.local` for the `Scope ID`.

2. Select `Save` and then download the CA Certificate and `trust.yml` file. These files can also be retrieved in the `Security` page of the deployment. You will use these files in the next set of steps.


### Establish trust in the ECK cluster [ec_establish_trust_in_the_eck_cluster]

1. Upload the {{ech}} certificate (that you downloaded in the last step of the previous section) as a Kubernetes secret.

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



## Set up CCS/R [ec_setup_ccsr]

Now that trust has been established, you can set up CCS/R from the ECK cluster to the {{ech}} cluster or from the {{ech}} cluster to the ECK cluster.


### ECK Cluster to {{ech}} cluster [ec_eck_cluster_to_elasticsearch_service_cluster]

Configure the ECK cluster [using certificate based authentication](ec-remote-cluster-self-managed.md).


### {{ech}} cluster to ECK Cluster [ec_elasticsearch_service_cluster_to_eck_cluster]

Follow the steps outlined in the [ECK documentation](/deploy-manage/remote-clusters/eck-remote-clusters.md#k8s_configure_the_remote_cluster_connection_through_the_elasticsearch_rest_api).

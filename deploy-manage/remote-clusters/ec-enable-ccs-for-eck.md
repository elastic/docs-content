---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-enable-ccs-for-eck.html
---

# Enabling CCS/R between Elasticsearch Service and ECK [ec-enable-ccs-for-eck]

These steps describe how to configure remote clusters between an {{es}} cluster in Elasticsearch Service and an {{es}} cluster running within [Elastic Cloud on Kubernetes (ECK)](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-overview.html). Once that’s done, you’ll be able to [run CCS queries from {{es}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-cross-cluster-search.html) or [set up CCR](https://www.elastic.co/guide/en/elasticsearch/reference/current/ccr-getting-started.html).


## Establish trust between two clusters [ec_establish_trust_between_two_clusters]

The first step is to establish trust between the two clusters.


### Establish trust in the Elasticsearch Service cluster [ec_establish_trust_in_the_elasticsearch_service_cluster]

1. Save the ECK CA certificate to a file. For a cluster named `quickstart`, run:

    ```sh
    kubectl get secret quickstart-es-transport-certs-public -o go-template='{{index .data "ca.crt" | base64decode}}' > eck.ca.crt
    ```


1. Update the trust settings for the Elasticsearch Service deployment. Follow the steps provided in [Access clusters of a self-managed environment](ec-remote-cluster-self-managed.md), and specifically the first three steps in **Specify the deployments trusted to be used as remote clusters** using TLS certificate as security model.

    * Use the certificate file saved in the first step.
    * Select the {{ecloud}} pattern and enter `default.es.local` for the `Scope ID`.

2. Select `Save` and then download the CA Certificate and `trust.yml` file. These files can also be retrieved in the `Security` page of the deployment. You will use these files in the next set of steps.


### Establish trust in the ECK cluster [ec_establish_trust_in_the_eck_cluster]

1. Upload the Elasticsearch Service certificate (that you downloaded in the last step of the previous section) as a Kubernetes secret.

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



## Setup CCS/R [ec_setup_ccsr]

Now that trust has been established, you can set up CCS/R from the ECK cluster to the Elasticsearch Service cluster or from the Elasticsearch Service cluster to the ECK cluster.


### ECK Cluster to Elasticsearch Service cluster [ec_eck_cluster_to_elasticsearch_service_cluster]

Configure the ECK cluster [using certificate based authentication](ec-remote-cluster-self-managed.md).


### Elasticsearch Service cluster to ECK Cluster [ec_elasticsearch_service_cluster_to_eck_cluster]

Follow the steps outlined in the [ECK documentation](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-remote-clusters.html#k8s_configure_the_remote_cluster_connection_through_the_elasticsearch_rest_api).

---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-apm-eck-managed-es.html
---

# Use an Elasticsearch cluster managed by ECK [k8s-apm-eck-managed-es]

Managing APM Server, Kibana and Elasticsearch with ECK allows a smooth and secured integration between the stack components. The output configuration of the APM Server is setup automatically to establish a trust relationship with Elasticsearch. Specifying the Kibana reference allows ECK to automatically configure the [Kibana endpoint](https://www.elastic.co/guide/en/apm/server/current/setup-kibana-endpoint.html).

1. To deploy an APM Server and connect it to the Elasticsearch cluster and Kibana instance you created in the [quickstart](deploy-an-orchestrator.md), apply the following specification:

    ```yaml
    cat <<EOF | kubectl apply -f -
    apiVersion: apm.k8s.elastic.co/v1
    kind: ApmServer
    metadata:
      name: apm-server-quickstart
      namespace: default
    spec:
      version: 8.16.1
      count: 1
      elasticsearchRef:
        name: quickstart
      kibanaRef:
        name: quickstart
    EOF
    ```

1. A reference to a Kibana instance is only required for APM Server versions 8.0.0 and later.


::::{note}
Starting with version 8.0.0 the following Kibana configuration is required to run APM Server
::::


```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
config:
  xpack.fleet.packages:
  - name: apm
    version: latest
```

By default `elasticsearchRef` targets all nodes in your Elasticsearch cluster. If you want to direct traffic to specific nodes of your cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.

1. Monitor APM Server deployment.

    You can retrieve details about the APM Server instance:

    ```sh
    kubectl get apmservers
    ```

    ```sh
    NAME                     HEALTH    NODES    VERSION   AGE
    apm-server-quickstart    green     1        8.16.1      8m
    ```

    And you can list all the Pods belonging to a given deployment:

    ```sh
    kubectl get pods --selector='apm.k8s.elastic.co/name=apm-server-quickstart'
    ```

    ```sh
    NAME                                                READY   STATUS    RESTARTS   AGE
    apm-server-quickstart-apm-server-69b447ddc5-fflc6   1/1     Running   0          2m50s
    ```

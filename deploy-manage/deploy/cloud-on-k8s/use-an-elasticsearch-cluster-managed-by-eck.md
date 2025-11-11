---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-apm-eck-managed-es.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Use an {{es}} cluster managed by ECK [k8s-apm-eck-managed-es]

Managing APM Server, {{kib}} and {{es}} with ECK allows a smooth and secured integration between the stack components. The output configuration of the APM Server is setup automatically to establish a trust relationship with {{es}}. Specifying the {{kib}} reference allows ECK to automatically configure the [{{kib}} endpoint](/solutions/observability/apm/apm-server/configure-kibana-endpoint.md).

1. To deploy an APM Server and connect it to the {{es}} cluster and {{kib}} instance you created in [](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md), apply the following specification:

    ```yaml subs=true
    cat <<EOF | kubectl apply -f -
    apiVersion: apm.k8s.elastic.co/v1
    kind: ApmServer
    metadata:
      name: apm-server-quickstart
      namespace: default
    spec:
      version: {{version.stack}}
      count: 1
      elasticsearchRef:
        name: quickstart
      kibanaRef:
        name: quickstart <1>
    EOF
    ```

    1. A reference to a {{kib}} instance is only required for APM Server versions 8.0.0 and later.


::::{note}
Starting with version 8.0.0 the following {{kib}} configuration is required to run APM Server
::::


```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
config:
  xpack.fleet.packages:
  - name: apm
    version: latest
```

By default `elasticsearchRef` targets all nodes in your {{es}} cluster. If you want to direct traffic to specific nodes of your cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.

1. Monitor APM Server deployment.

    You can retrieve details about the APM Server instance:

    ```sh
    kubectl get apmservers
    ```

    ```sh subs=true
    NAME                     HEALTH    NODES    VERSION   AGE
    apm-server-quickstart    green     1        {{version.stack}}      8m
    ```

    And you can list all the Pods belonging to a given deployment:

    ```sh
    kubectl get pods --selector='apm.k8s.elastic.co/name=apm-server-quickstart'
    ```

    ```sh
    NAME                                                READY   STATUS    RESTARTS   AGE
    apm-server-quickstart-apm-server-69b447ddc5-fflc6   1/1     Running   0          2m50s
    ```

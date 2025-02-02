---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-quickstart.html
---

# Quickstart [k8s-logstash-quickstart]

Add the following specification to create a minimal {{ls}} deployment that will listen to a Beats agent or Elastic Agent configured to send to Logstash on port 5044, create the service and write the output to an Elasticsearch cluster named `quickstart`, created in the [Elasticsearch quickstart](deploy-an-orchestrator.md).

```yaml
cat <<'EOF' | kubectl apply -f -
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  count: 1
  elasticsearchRefs:
    - name: quickstart
      clusterName: qs
  version: 8.16.1
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${QS_ES_HOSTS}" ]
            user => "${QS_ES_USER}"
            password => "${QS_ES_PASSWORD}"
            ssl_certificate_authorities => "${QS_ES_SSL_CERTIFICATE_AUTHORITY}"
          }
        }
  services:
    - name: beats
      service:
        spec:
          type: NodePort
          ports:
            - port: 5044
              name: "filebeat"
              protocol: TCP
              targetPort: 5044
EOF
```

Check [Configuration examples](configuration-examples-logstash.md) for more ready-to-use manifests.

1. Check the status of Logstash

    ```sh
    kubectl get logstash
    ```

    ```sh
    NAME              AVAILABLE   EXPECTED   AGE   VERSION
    quickstart        3           3          4s    8.16.1
    ```

2. List all the Pods that belong to a given Logstash specification.

    ```sh
    kubectl get pods --selector='logstash.k8s.elastic.co/name=quickstart'
    ```

    ```sh
    NAME              READY   STATUS    RESTARTS   AGE
    quickstart-ls-0   1/1     Running   0          91s
    ```

3. Access logs for a Pod.

```sh
kubectl logs -f quickstart-ls-0
```


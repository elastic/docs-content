---
navigation_title: Quickstart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-quickstart.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Quickstart: Running {{ls}} on {{eck}} [k8s-logstash-quickstart]

Add the following specification to create a minimal {{ls}} deployment that will listen to a Beats agent or Elastic Agent configured to send to Logstash on port 5044, create the service and write the output to an {{es}} cluster named `quickstart`, created in [](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md).

```yaml subs=true
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
  version: {{version.stack}}
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

    ```sh subs=true
    NAME              AVAILABLE   EXPECTED   AGE   VERSION
    quickstart        3           3          4s    {{version.stack}}
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


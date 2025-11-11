---
navigation_title: Quickstart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-quickstart.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Quickstart: Running standalone {{agent}} on {{eck}} [k8s-elastic-agent-quickstart]

1. Apply the following specification to deploy Elastic Agent with the System metrics integration to harvest CPU metrics from the Agent Pods. ECK automatically configures the secured connection to an {{es}} cluster named `quickstart`, created in [](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md).

    ```yaml subs=true
    cat <<EOF | kubectl apply -f -
    apiVersion: agent.k8s.elastic.co/v1alpha1
    kind: Agent
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      elasticsearchRefs:
      - name: quickstart
      daemonSet:
        podTemplate:
          spec:
            securityContext:
              runAsUser: 0 <1>
      config:
        inputs:
          - name: system-1
            revision: 1
            type: system/metrics
            use_output: default
            meta:
              package:
                name: system
                version: 0.9.1
            data_stream:
              namespace: default
            streams:
              - id: system/metrics-system.cpu
                data_stream:
                  dataset: system.cpu
                  type: metrics
                metricsets:
                  - cpu
                cpu.metrics:
                  - percentages
                  - normalized_percentages
                period: 10s
    EOF
    ```

    1. The root user is required to persist state in a `hostPath` volume. See [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for options to not run the Agent container as root.


    Check [Configuration examples](configuration-examples-standalone.md) for more ready-to-use manifests.

2. Monitor the status of Elastic Agent.

    ```sh
    kubectl get agent
    ```

    ```sh subs=true
    NAME            HEALTH   AVAILABLE   EXPECTED   VERSION   AGE
    quickstart      green    3           3          {{version.stack}}    15s
    ```

3. List all the Pods that belong to a given Elastic Agent specification.

    ```sh
    kubectl get pods --selector='agent.k8s.elastic.co/name=quickstart'
    ```

    ```sh
    NAME                     READY   STATUS    RESTARTS   AGE
    quickstart-agent-6bcxr   1/1     Running   0          68s
    quickstart-agent-t49fd   1/1     Running   0          68s
    quickstart-agent-zqp55   1/1     Running   0          68s
    ```

4. Access logs for one of the Pods.

    ```sh
    kubectl logs -f quickstart-agent-6bcxr
    ```

5. Access the CPU metrics ingested by Elastic Agent.

    You have two options:

    * Follow the {{es}} deployment [guide](elasticsearch-deployment-quickstart.md) and run:

        ```sh
        curl -u "elastic:$PASSWORD" -k "https://localhost:9200/metrics-system.cpu-*/_search"
        ```

    * Follow the {{kib}} deployment [guide](kibana-instance-quickstart.md), log in and go to **Kibana** > **Discover**.



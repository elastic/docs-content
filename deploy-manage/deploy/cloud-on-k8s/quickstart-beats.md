---
navigation_title: Quickstart
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-quickstart.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Quickstart: Running {{beats}} on {{eck}} [k8s-beat-quickstart]

1. Apply the following specification to deploy Filebeat and collect the logs of all containers running in the Kubernetes cluster. ECK automatically configures the secured connection to an {{es}} cluster named `quickstart`, created in [](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md).

    ```yaml subs=true
    cat <<EOF | kubectl apply -f -
    apiVersion: beat.k8s.elastic.co/v1beta1
    kind: Beat
    metadata:
      name: quickstart
    spec:
      type: filebeat
      version: {{version.stack}}
      elasticsearchRef:
        name: quickstart
      config:
        filebeat.inputs:
        - type: container
          paths:
          - /var/log/containers/*.log
      daemonSet:
        podTemplate:
          spec:
            dnsPolicy: ClusterFirstWithHostNet
            hostNetwork: true
            securityContext:
              runAsUser: 0
            containers:
            - name: filebeat
              volumeMounts:
              - name: varlogcontainers
                mountPath: /var/log/containers
              - name: varlogpods
                mountPath: /var/log/pods
              - name: varlibdockercontainers
                mountPath: /var/lib/docker/containers
            volumes:
            - name: varlogcontainers
              hostPath:
                path: /var/log/containers
            - name: varlogpods
              hostPath:
                path: /var/log/pods
            - name: varlibdockercontainers
              hostPath:
                path: /var/lib/docker/containers
    EOF
    ```

    Check [Configuration Examples](configuration-examples-beats.md) for more ready-to-use manifests.

2. Monitor Beats.

    Retrieve details about the Filebeat.

    ```sh
    kubectl get beat
    ```

    ```sh subs=true
    NAME                  HEALTH   AVAILABLE   EXPECTED   TYPE       VERSION   AGE
    quickstart            green    3           3          filebeat   {{version.stack}}     2m
    ```

3. List all the Pods belonging to a given Beat.

    ```sh
    kubectl get pods --selector='beat.k8s.elastic.co/name=quickstart-beat-filebeat'
    ```

    ```sh
    NAME                                      READY   STATUS    RESTARTS   AGE
    quickstart-beat-filebeat-tkz65            1/1     Running   0          3m45s
    quickstart-beat-filebeat-kx5jt            1/1     Running   0          3m45s
    quickstart-beat-filebeat-nb6qh            1/1     Running   0          3m45s
    ```

4. Access logs for one of the Pods.

    ```sh
    kubectl logs -f quickstart-beat-filebeat-tkz65
    ```

5. Access logs ingested by Filebeat.

    You have two options:

    * Follow the {{es}} deployment [guide](elasticsearch-deployment-quickstart.md) and run:

        ::::{tip}
        If the remote endpoint uses a certificate that is not publicly trusted (for example, one signed by a private or corporate CA), provide the corresponding CA certificate using `--cacert /path/to/ca.pem` so that `curl` can verify it.

For testing only, you can use [`--insecure`](https://curl.se/docs/manpage.html#-k) (or `-k`) to skip certificate verification. This flag turns off TLS trust checks and should not be used in production.
        ::::

        ```sh
        curl -u "elastic:$PASSWORD" "https://localhost:9200/filebeat-*/_search"
        ```

    * Follow the {{kib}} deployment [guide](kibana-instance-quickstart.md), log in and go to **Kibana** > **Discover**.



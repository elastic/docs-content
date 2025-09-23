---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-openshift-beats.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Grant privileged permissions to Beats [k8s-openshift-beats]

Deploying Beats on Openshift may require some privileged permissions. This section describes how to create a ServiceAccount, add the ServiceAccount to the `privileged` SCC, and use it to run Beats.

The following example assumes that Beats is deployed in the Namespace `elastic` with the ServiceAccount `heartbeat`. You can replace these values according to your environment.

::::{note}
If you used the examples from the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/beats), the ServiceAccount may already exist.
::::


1. Create a dedicated ServiceAccount:

    ```shell
    oc create serviceaccount heartbeat -n elastic
    ```

2. Add the ServiceAccount to the required SCC:

    ```shell
    oc adm policy add-scc-to-user privileged -z heartbeat -n elastic
    ```

3. Update the Beat manifest to use the new ServiceAccount, for example:

    ```yaml subs=true
    apiVersion: beat.k8s.elastic.co/v1beta1
    kind: Beat
    metadata:
      name: heartbeat
    spec:
      type: heartbeat
      version: {{version.stack}}
      elasticsearchRef:
        name: elasticsearch
      config:
        heartbeat.monitors:
        - type: tcp
          schedule: '@every 5s'
          hosts: ["elasticsearch-es-http.default.svc:9200"]
        - type: tcp
          schedule: '@every 5s'
          hosts: ["kibana-kb-http.default.svc:5601"]
      deployment:
        replicas: 1
        podTemplate:
          spec:
            serviceAccountName: heartbeat
            securityContext:
              runAsUser: 0
    ```


If SELinux is enabled, the Beat Pod might fail with the following message:

```shell
Exiting: Failed to create Beat meta file: open /usr/share/heartbeat/data/meta.json.new: permission denied
```

To fix this error, apply the label `svirt_sandbox_file_t` to the directory `/var/lib/elastic/heartbeat/heartbeat-data/` on the Kubernetes node:

```shell
chcon -Rt svirt_sandbox_file_t /var/lib/elastic/heartbeat/heartbeat-data/
```

Repeat this step on all the hosts where the heartbeat Pod can be deployed.

Some Beats may require additional permissions. For example, `Filebeat` needs additional privileges to read other container logs on the host. In this case, you can use the `privileged` field in the security context of the container spec:

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: filebeat
spec:
  type: filebeat
...
  daemonSet:
    podTemplate:
      spec:
        serviceAccountName: filebeat
        automountServiceAccountToken: true
...
        containers:
        - name: filebeat
          securityContext:
            runAsUser: 0
            privileged: true # This is required to access other containers logs
          volumeMounts:
          - name: varlibdockercontainers
            mountPath: /var/lib/docker/containers
        volumes:
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
```

Check the complete examples in the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/beats).


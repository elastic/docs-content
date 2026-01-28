To run {{agent}} as a non-root user you must choose how you want to persist data to the Agent’s volume.

::::{tab-set}

:::{tab-item} {{agent}} 8.16 and later

* Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
* Run {{agent}} with a `hostPath` volume.

:::

:::{tab-item} {{agent}} 8.15 and earlier

* Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
* Run {{agent}} with a `hostPath` volume which has the advantage of persisting data between restarts of the {{agent}}.

In addition to these decisions, if you are running {{agent}} in {{fleet}} mode as a non-root user, you must configure `ssl.certificate_authorities` in each `xpack.fleet.outputs` to trust the CA of the {{es}} Cluster.

To run {{agent}} with an `emptyDir` volume:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server
spec:
  deployment:
    podTemplate:
      spec:
        securityContext: <1>
          fsGroup: 1000
        volumes:
        - name: agent-data
          emptyDir: {}
...
```

1. Gid 1000 is the default group at which the Agent container runs. Adjust as necessary if `runAsGroup` has been modified.


To run {{agent}} with a `hostPath` volume:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server-sample
  namespace: elastic-apps
spec:
  mode: fleet
  fleetServerEnabled: true
  deployment: {}
...
---
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent-sample
  namespace: elastic-apps
spec:
  daemonSet: {}
...
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: manage-agent-hostpath-permissions
  namespace: elastic-apps
spec:
  selector:
    matchLabels:
      name: manage-agent-hostpath-permissions
  template:
    metadata:
      labels:
        name: manage-agent-hostpath-permissions
    spec:
      # serviceAccountName: elastic-agent <1>
      volumes:
        - hostPath:
            path: /var/lib/elastic-agent
            type: DirectoryOrCreate
          name: "agent-data"
      initContainers:
        - name: manage-agent-hostpath-permissions
          # image: registry.access.redhat.com/ubi9/ubi-minimal:latest <2>
          image: docker.io/bash:5.2.15
          resources:
            limits:
              cpu: 100m
              memory: 32Mi
          securityContext:
            # privileged: true <3>
            runAsUser: 0
          volumeMounts:
            - mountPath: /var/lib/elastic-agent
              name: agent-data
          command:
          - 'bash'
          - '-e'
          - '-c'
          - |-
            # Adjust this with /var/lib/elastic-agent/YOUR-NAMESPACE/YOUR-AGENT-NAME/state
            # Multiple directories are supported for the fleet-server + agent use case.
            dirs=(
              "/var/lib/elastic-agent/default/elastic-agent/state"
              "/var/lib/elastic-agent/default/fleet-server/state"
              )
            for dir in ${dirs[@]}; do
              mkdir -p "${dir}"
              # chcon is only required when running an an SELinux-enabled/OpenShift environment.
              # chcon -Rt svirt_sandbox_file_t "${dir}"
              chmod g+rw "${dir}"
              # Gid 1000 is the default group at which the Agent container runs. Adjust as necessary if `runAsGroup` has been modified.
              chgrp 1000 "${dir}"
              if [ -n "$(ls -A ${dir} 2>/dev/null)" ]
              then
                # Gid 1000 is the default group at which the Agent container runs. Adjust as necessary if `runAsGroup` has been modified.
                chgrp 1000 "${dir}"/*
                chmod g+rw "${dir}"/*
              fi
            done
      containers:
        - name: sleep
          image: gcr.io/google-containers/pause-amd64:3.2
```

1. This is only required when running in an SElinux-enabled/OpenShift environment. Ensure this user has been added to the privileged security context constraints (SCC) in the correct namespace. `oc adm policy add-scc-to-user privileged -z elastic-agent -n elastic-apps`
2. UBI is only required when needing the `chcon` binary when running in an SELinux-enabled/OpenShift environment. If that is not required then the following smaller image can be used instead: `docker.io/bash:5.2.15`
3. Privileged is only required when running in an SElinux-enabled/OpenShift environment.

When running Agent in fleet mode as a non-root user {{kib}} must be configured in order to properly accept the CA of the {{es}} cluster.

```yaml
---
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  config:
    # xpack.fleet.agents.elasticsearch.hosts: <1>
    xpack.fleet.agents.fleet_server.hosts: ["<FLEET_SERVER_HOST_URL>-agent-http.default.svc:8220"]
    xpack.fleet.outputs:
    - id: eck-fleet-agent-output-elasticsearch
      is_default: true
      name: eck-elasticsearch
      type: elasticsearch
      hosts:
      - "<ELASTICSEARCH-HOST_URL>-es-http.default.svc:9200" <2>
      ssl:
        certificate_authorities: ["/mnt/elastic-internal/elasticsearch-association/default/elasticsearch-sample/certs/ca.crt"] <3>
```

1. This entry must not exist when running agent in fleet mode as a non-root user.
2. Note that the correct URL for {{es}} is `<ELASTICSEARCH_HOST_URL>-es-http.<YOUR-NAMESPACE>.svc:9200`
3. Note that the correct path for {{es}} `certificate_authorities` is `/mnt/elastic-internal/elasticsearch-association/YOUR-NAMESPACE/ELASTICSEARCH-NAME/certs/ca.crt`
:::

::::
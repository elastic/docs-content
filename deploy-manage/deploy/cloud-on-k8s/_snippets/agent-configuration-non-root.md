To run {{agent}} as a non-root user, you need to understand how permissions work for the Agent's data volume. The approach differs based on your {{agent}} version, cluster type, and persistence requirements.

## Quick reference

| Scenario | Volume type | Additional setup required |
|----------|-------------|---------------------------|
| {{agent}} 8.16+ on standard {{k8s}} | `hostPath` | allowPrivilegeEscalation: true, capabilities: add: ["CHOWN", "SETPCAP"] |
| {{agent}} 8.16+ on OpenShift/SELinux | `hostPath` | DaemonSet for permissions (SELinux prevents Agent from managing its own permissions) |
| {{agent}} 8.15 and earlier (ECK 2.10+) | `hostPath` | DaemonSet for permissions |
| Any version | `emptyDir` | `fsGroup` security context only |

::::{note}
Running {{agent}} with an `emptyDir` volume has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
::::

## Option 1: Use `emptyDir`

This is the simplest approach that will work in all {{k8s}} environments but data won't persist between Agent pod restarts.

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server
spec:
  deployment:
    podTemplate:
      spec:
        securityContext:
          fsGroup: 1000 # <1>
        volumes:
        - name: agent-data
          emptyDir: {}
...
```

1. GID 1000 is the default group the Agent container runs as. Adjust if you've modified `runAsGroup`.

## Option 2: Use `hostPath`

::::{tab-set}

:::{tab-item} {{agent}} 8.16+ (standard {{k8s}})

Starting with {{agent}} 8.16, the Agent automatically manages ownership of its volume mounts at startup. No additional DaemonSet or permission setup is required on standard {{k8s}} clusters.

You can run the Agent with a minimal set of capabilities:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent
spec:
  daemonSet:
    podTemplate:
      spec:
        containers:
        - name: agent
          securityContext:
            allowPrivilegeEscalation: true
            runAsNonRoot: true
            capabilities:
              drop:
              - ALL
              add:
              - CHOWN # <1>
              - SETPCAP # <2>
...
```

1. Required for the Agent to change ownership of its data directories.
2. Required for the Agent to modify process capabilities.

:::

:::{tab-item} {{agent}} 8.16+ (OpenShift/SELinux)

On OpenShift or other SELinux-enabled clusters, the Agent cannot elevate its privileges to change volume ownership due to SELinux restrictions. You must use a DaemonSet to manage permissions, the same as with {{agent}} 8.15 and earlier.

Refer to the **{{agent}} 8.15 and earlier** tab for the required configuration.

:::

:::{tab-item} {{agent}} 8.15 and earlier (ECK 2.10+)

For {{agent}} versions before 8.16, or when running on OpenShift/SELinux-enabled clusters with any version, you need a separate DaemonSet that runs as root to set up directory permissions before the Agent starts.

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
      # serviceAccountName: elastic-agent # <1>
      volumes:
        - hostPath:
            path: /var/lib/elastic-agent
            type: DirectoryOrCreate
          name: "agent-data"
      initContainers:
        - name: manage-agent-hostpath-permissions
          # image: registry.access.redhat.com/ubi9/ubi-minimal:latest # <2>
          image: docker.io/bash:5.2.15
          resources:
            limits:
              cpu: 100m
              memory: 32Mi
          securityContext:
            # privileged: true # <3>
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
              # chcon is only required when running on an SELinux-enabled/OpenShift environment.
              # chcon -Rt svirt_sandbox_file_t "${dir}"
              chmod g+rw "${dir}"
              # GID 1000 is the default group the Agent container runs as. Adjust if runAsGroup has been modified.
              chgrp 1000 "${dir}"
              if [ -n "$(ls -A ${dir} 2>/dev/null)" ]
              then
                chgrp 1000 "${dir}"/*
                chmod g+rw "${dir}"/*
              fi
            done
      containers:
        - name: sleep
          image: gcr.io/google-containers/pause-amd64:3.2
```

1. Only required when running in an SELinux-enabled/OpenShift environment. Ensure this user has been added to the privileged security context constraints (SCC) in the correct namespace: `oc adm policy add-scc-to-user privileged -z elastic-agent -n elastic-apps`
2. The UBI image is only required when you need the `chcon` binary for SELinux-enabled/OpenShift environments. Otherwise, use the smaller `docker.io/bash:5.2.15` image.
3. Only required when running in an SELinux-enabled/OpenShift environment.

:::

::::

## {{fleet}} mode: Additional {{kib}} configuration

```yaml {applies_to}
stack: ga 7.14-8.15
```

When running {{agent}} in {{fleet}} mode as a non-root user with versions before 8.16, you must also configure `ssl.certificate_authorities` in `xpack.fleet.outputs` to trust the CA of the {{es}} cluster.

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  config:
    # xpack.fleet.agents.elasticsearch.hosts: # <1>
    xpack.fleet.agents.fleet_server.hosts: ["https://fleet-server-agent-http.default.svc:8220"]
    xpack.fleet.outputs:
    - id: eck-fleet-agent-output-elasticsearch
      is_default: true
      name: eck-elasticsearch
      type: elasticsearch
      hosts:
      - "https://elasticsearch-es-http.default.svc:9200" # <2>
      ssl:
        certificate_authorities: ["/mnt/elastic-internal/elasticsearch-association/default/elasticsearch-sample/certs/ca.crt"] # <3>
```

1. This entry must not exist when running agent in {{fleet}} mode as a non-root user.
2. The correct URL for {{es}} is `https://<ELASTICSEARCH_NAME>-es-http.<NAMESPACE>.svc:9200`.
3. The correct path for {{es}} `certificate_authorities` is `/mnt/elastic-internal/elasticsearch-association/<NAMESPACE>/<ELASTICSEARCH_NAME>/certs/ca.crt`.

---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration
---

# Configuration for standalone Elastic Agents on {{eck}} [k8s-elastic-agent-configuration]

## Upgrade the Elastic Agent specification [k8s-elastic-agent-upgrade-specification]

You can upgrade the Elastic Agent version or change settings by editing the YAML specification. ECK applies the changes by performing a rolling restart of the Agent’s Pods. Depending on the settings that you used, ECK will set the [outputs](#k8s-elastic-agent-set-output) part of the configuration, or restart Elastic Agent on certificate rollover.


## Customize the Elastic Agent configuration [k8s-elastic-agent-custom-configuration]

The Elastic Agent configuration is defined in the `config` element:

```yaml subs=true
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
```

1. The root user is required to persist state in a `hostPath` volume. See [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for options to not run the Agent container as root.


Alternatively, it can be provided through a Secret specified in the `configRef` element. The Secret must have an `agent.yml` entry with this configuration:

```yaml subs=true
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
          runAsUser: 0
  configRef:
    secretName: system-cpu-config
---
apiVersion: v1
kind: Secret
metadata:
  name: system-cpu-config
stringData:
  agent.yml: |-
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
```

You can use the Fleet application in {{kib}} to generate the configuration for Elastic Agent, even when running in standalone mode. Check the [Elastic Agent standalone](/reference/fleet/install-standalone-elastic-agent.md) documentation. Adding the corresponding integration package to {{kib}} also adds the related dashboards and visualizations.


## Use multiple Elastic Agent outputs [k8s-elastic-agent-multi-output]

Elastic Agent supports the use of multiple outputs. Therefore, the `elasticsearchRefs` element accepts multiple references to {{es}} clusters. ECK populates the outputs section of the Elastic Agent configuration based on those references. If you configure more than one output, you also have to specify a unique `outputName` attribute.

To send Elastic Agent’s internal monitoring and log data to a different {{es}} cluster called `agent-monitoring` in the `elastic-monitoring` namespace, and the harvested metrics to our `quickstart` cluster, you have to define two `elasticsearchRefs` as shown in the following example:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  daemonSet:
    podTemplate:
      spec:
        securityContext:
          runAsUser: 0
  elasticsearchRefs:
  - name: quickstart
    outputName: default
  - name: agent-monitoring
    namespace: elastic-monitoring
    outputName: monitoring
  config:
    agent:
      monitoring:
        enabled: true
        use_output: monitoring
        logs: true
        metrics: true
    inputs:
      - name: system-1
        revision: 1
        type: system/metrics
        use_output: default
...
```


## Customize the connection to an {{es}} cluster [k8s-elastic-agent-connect-es]

The `elasticsearchRefs` element allows ECK to automatically configure Elastic Agent to establish a secured connection to one or more managed {{es}} clusters. By default, it targets all nodes in your cluster. If you want to direct traffic to specific nodes of your {{es}} cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.


## Set manually Elastic Agent outputs [k8s-elastic-agent-set-output]

If the `elasticsearchRefs` element is specified, ECK populates the outputs section of the Elastic Agent configuration. ECK creates a user with appropriate roles and permissions and uses its credentials. If required, it also mounts the CA certificate in all Agent Pods, and recreates Pods when this certificate changes. Moreover, `elasticsearchRef` element can refer to an ECK-managed {{es}} cluster by filling the `name`, `namespace`, `serviceName` fields accordingly, as well as to a Kubernetes secret that contains the connection information to an {{es}} cluster not managed by it. In the latter case, for authenticating against the {{es}} cluster the secret must contain the fields of `url` and either the `username` with `password` or the `api-key`. Refer to [*Connect to external Elastic resources*](connect-to-external-elastic-resources.md) for additional details.

The outputs can also be set manually. To do that, remove the `elasticsearchRefs` element from the specification and include an appropriate output configuration in the `config`, or indirectly through the `configRef` mechanism.

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  daemonSet:
    podTemplate:
      spec:
        securityContext:
          runAsUser: 0
  config:
    outputs:
      default:
        type: elasticsearch
        hosts:
          - "https://my-custom-elasticsearch-cluster.cloud.elastic.co:9243"
        password: ES_PASSWORD
        username: ES_USER
...
```


## Choose the deployment model [k8s-elastic-agent-chose-the-deployment-model]

Depending on the use case, Elastic Agent may need to be deployed as a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), or a [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulSet/). Provide a `podTemplate` element under either the `deployment` or the `daemonSet` element in the specification to choose how your Elastic Agents should be deployed. When choosing the `deployment` option you can additionally specify the [strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy) used to replace old Pods with new ones.

Similarly, you can set the [update strategy](https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/) when deploying as a DaemonSet. This allows you to control the rollout speed for new configuration by modifying the `maxUnavailable` setting:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  daemonSet:
    podTemplate:
      spec:
        securityContext:
          runAsUser: 0
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 3
...
```

Check [Set compute resources for Beats and Elastic Agent](manage-compute-resources.md#k8s-compute-resources-beats-agent) for more information on how to use the Pod template to adjust the resources given to Elastic Agent.


## Role Based Access Control for Elastic Agent [k8s-elastic-agent-role-based-access-control]

Some Elastic Agent features, such as the [Kubernetes integration](https://epr.elastic.co/package/kubernetes/0.2.8/), require that Agent Pods interact with Kubernetes APIs. This functionality requires specific permissions. The standard Kubernetes [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) rules apply. For example, to allow API interactions:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent
spec:
  version: {{version.stack}}
  elasticsearchRefs:
  - name: elasticsearch
  daemonSet:
    podTemplate:
      spec:
        automountServiceAccountToken: true
        serviceAccountName: elastic-agent
        securityContext:
          runAsUser: 0
...

apiVersion: v1
kind: ServiceAccount
metadata:
  name: elastic-agent
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: elastic-agent
subjects:
- kind: ServiceAccount
  name: elastic-agent
  namespace: default
roleRef:
  kind: ClusterRole
  name: elastic-agent
  apiGroup: rbac.authorization.k8s.io
```


## Deploying Elastic Agent in secured clusters [k8s-elastic-agent-deploying-in-secured-clusters]

To deploy Elastic Agent in clusters with the Pod Security Policy admission controller enabled, or in [OpenShift](k8s-openshift-agent.md) clusters, you might need to grant additional permissions to the Service Account used by the Elastic Agent Pods. Those Service Accounts must be bound to a Role or ClusterRole that has `use` permission for the required Pod Security Policy or Security Context Constraints. Different Elastic Agent integrations might require different settings set in their PSP/[SCC](k8s-openshift-agent.md).


## Running as a non-root user [k8s_running_as_a_non_root_user]

In order to run {{agent}} as a non-root user you must choose how you want to persist data to the Agent’s volume.

::::{tab-set}

:::{tab-item} {{agent}} 8.16 and higher

1. Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
2. Run {{agent}} with a `hostPath` volume. No additional configuration is required.

:::

:::{tab-item} {{agent}} 8.15 and before 

1. Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
2. Run {{agent}} with a `hostPath` volume in addition to a `DaemonSet` running as `root` that sets up permissions for the `agent` user.


In addition to these decisions, if you are running {{agent}} in {{fleet}} mode as a non-root user, you must configure `certificate_authorities.ssl` in each `xpack.fleet.outputs` to trust the CA of the {{es}} Cluster.

To run {{agent}} with an `emptyDir` volume.

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


To run {{agent}} with a `hostPath` volume and a `DaemonSet` to maintain permissions.

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
    xpack.fleet.agents.fleet_server.hosts: ["<FLEET_SERVER_HOST_URL>-sample-agent-http.default.svc:8220"]
    xpack.fleet.outputs:
    - id: eck-fleet-agent-output-elasticsearch
      is_default: true
      name: eck-elasticsearch
      type: elasticsearch
      hosts:
      - "<ELASTICSEARCH_HOST>-es-http.default.svc:9200" <2>
      ssl:
        certificate_authorities: ["/mnt/elastic-internal/elasticsearch-association/default/elasticsearch-sample/certs/ca.crt"] <3>
```

1. This entry must not exist when running agent in fleet mode as a non-root user.
2. Note that the correct URL for {{es}} is `<ELASTICSEARCH_HOST_URL>-es-http.<YOUR-NAMESPACE>.svc:9200`
3. Note that the correct path for {{es}} `certificate_authorities` is `/mnt/elastic-internal/elasticsearch-association/YOUR-NAMESPACE/ELASTICSEARCH-NAME/certs/ca.crt`

:::

::::

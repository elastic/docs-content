---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-fleet-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration
---

# Configuration for Fleet managed agents on {{eck}} [k8s-elastic-agent-fleet-configuration]

{{fleet}}-managed {{agents}} must connect to {{fleet-server}} to receive their configurations. You can deploy {{fleet-server}} instances using ECKs Agent CRD with the appropriate configuration, as shown in [Fleet mode and Fleet Server](#k8s-elastic-agent-fleet-configuration-fleet-mode-and-fleet-server).

To know more about {{fleet}} architecture and related components, check the {{fleet}} [documentation](/reference/fleet/fleet-server.md).

## {{fleet}} mode and {{fleet-server}} [k8s-elastic-agent-fleet-configuration-fleet-mode-and-fleet-server]

To run both {{fleet-server}} and {{agent}} in {{fleet}}-managed mode, set the `mode` configuration element to `fleet`.

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent-sample
spec:
  mode: fleet
```

To run {{fleet-server}}, set the `fleetServerEnabled` configuration element to `true`, as shown in this example:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server-sample
spec:
  mode: fleet
  fleetServerEnabled: true
```

You can leave the default value `false` for any other case.


## Configure {{kib}} [k8s-elastic-agent-fleet-configuration-required-kibana-configuration]

To have {{fleet}} running properly, the following settings must be correctly set in the {{kib}} configuration:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  config:
    xpack.fleet.agents.elasticsearch.hosts: ["<ELASTICSEARCH_HOST_URL>-es-http.default.svc:9200"]
    xpack.fleet.agents.fleet_server.hosts: ["<FLEET_SERVER_HOST_URL>-sample-agent-http.default.svc:8220"]
    xpack.fleet.packages:
      - name: system
        version: latest
      - name: elastic_agent
        version: latest
      - name: fleet_server
        version: latest
    xpack.fleet.agentPolicies:
      - name: Fleet Server on ECK policy
        id: eck-fleet-server
        namespace: default
        is_managed: true
        monitoring_enabled:
          - logs
          - metrics
        unenroll_timeout: 900
        package_policies:
        - name: fleet_server-1
          id: fleet_server-1
          package:
            name: fleet_server
      - name: Elastic Agent on ECK policy
        id: eck-agent
        namespace: default
        is_managed: true
        monitoring_enabled:
          - logs
          - metrics
        unenroll_timeout: 900
        is_default: true
        package_policies:
          - name: system-1
            id: system-1
            package:
              name: system
```

* `xpack.fleet.agents.elasticsearch.hosts` must point to the {{es}} cluster where {{agents}} should send data. For ECK-managed {{es}} clusters ECK creates a Service accessible through `<ES_RESOURCE_NAME>-es-http.<ES_RESOURCE_NAMESPACE>.svc:9200` URL, where `ES_RESOURCE_NAME` is the name of {{es}} resource and `ES_RESOURCE_NAMESPACE` is the namespace it was deployed within. Refer to [Storing local state in host path volume](configuration-examples-standalone.md#k8s_storing_local_state_in_host_path_volume) for details on adjusting this field when running agent as non-root.
* `xpack.fleet.agents.fleet_server.hosts` must point to {{fleet-server}} that {{agents}} should connect to. For ECK-managed {{fleet-server}} instances, ECK creates a Service accessible through `<FS_RESOURCE_NAME>-agent-http.FS_RESOURCE_NAMESPACE.svc:8220` URL, where `FS_RESOURCE_NAME` is the name of {{agent}} resource with {{fleet-server}} enabled and `FS_RESOURCE_NAMESPACE` is the namespace it was deployed in.
* `xpack.fleet.packages` are required packages to enable {{fleet-server}} and {{agents}} to enroll.
* `xpack.fleet.agentPolicies` policies are needed for {{fleet-server}} and {{agents}} to enroll to, check https://www.elastic.co/guide/en/fleet/current/agent-policy.html for more information.


## Set referenced resources [k8s-elastic-agent-fleet-configuration-setting-referenced-resources]

Both {{fleet-server}} and {{agent}} in {{fleet}} mode can be automatically set up with {{fleet}} by ECK. The ECK operator can set up {{fleet}} in {{kib}} (which otherwise requires manual steps) and enroll {{fleet-server}} in the default {{fleet-server}} policy. {{agent}} can be automatically enrolled in the default {{agent}} policy. To allow ECK to set this up, provide a reference to a ECK-managed {{kib}} through the `kibanaRef` configuration element.

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server-sample
spec:
  kibanaRef:
    name: kibana
```

ECK can also facilitate the connection between {{agents}} and a ECK-managed {{fleet-server}}. To allow ECK to set this up, provide a reference to {{fleet-server}} through the `fleetServerRef` configuration element.

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent-sample
spec:
  fleetServerRef:
    name: fleet-server-sample
```

Set the `elasticsearchRefs` element in your {{fleet-server}} to point to the {{es}} cluster that will manage {{fleet}}. Leave `elasticsearchRefs` empty or unset it for any {{agent}} running in {{fleet}} mode as the {{es}} cluster to target will come from {{kib}}'s `xpack.fleet.agents.elasticsearch.hosts` configuration element.

::::{note}
Currently, {{agent}} in {{fleet}} mode supports only a single output, so only a single {{es}} cluster can be referenced.
::::


```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server-sample
spec:
  elasticsearchRefs:
  - name: elasticsearch-sample
```

By default, every reference targets all instances in your {{es}}, {{kib}} and {{fleet-server}} deployments, respectively. If you want to direct traffic to specific instances, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.


## Customize {{agent}} configuration [k8s-elastic-agent-fleet-configuration-custom-configuration]

In contrast to {{agents}} in standalone mode, the configuration is managed through {{fleet}}, and it cannot be defined through `config` or `configRef` elements with a few exceptions.

One of those exceptions is the configuration of providers as described in [advanced Agent configuration managed by Fleet](/reference/fleet/advanced-kubernetes-managed-by-fleet.md). When {{agent}} is managed by {{fleet}} and is orchestrated by ECK, the configuration of providers can simply be done through the `.spec.config` element in the Agent resource as of {applies_to}`stack: ga 8.13`:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent
spec:
  config:
    fleet:
      enabled: true
    providers.kubernetes:
      add_resource_metadata:
        deployment: true
```

## Upgrade the {{agent}} specification [k8s-elastic-agent-fleet-configuration-upgrade-specification]

You can upgrade the {{agent}} version or change settings by editing the YAML specification file. ECK applies the changes by performing a rolling restart of the Agent’s Pods. Depending on the settings that you used, ECK will set up {{fleet}} in {{kib}}, enrolls the agent in {{fleet}}, or restarts {{agent}} on certificate rollover.


## Choose the deployment model [k8s-elastic-agent-fleet-configuration-chose-the-deployment-model]

Depending on the use case, {{agent}} may need to be deployed as a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/), or a [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulSet/). To choose how to deploy your {{agents}}, provide a `podTemplate` element under the `deployment` or the `daemonSet` element in the specification. If you choose the `deployment` option, you can additionally specify the [strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy) used to replace old Pods with new ones.

Similarly, you can set the [update strategy](https://kubernetes.io/docs/tasks/manage-daemon/update-daemon-set/) when deploying as a DaemonSet. This allows you to control the rollout speed for new configuration by modifying the `maxUnavailable` setting:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent-sample
spec:
  version: {{version.stack}}
  daemonSet:
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 3
...
```

Refer to [Set compute resources for Beats and Elastic Agent](manage-compute-resources.md#k8s-compute-resources-beats-agent) for more information on how to use the Pod template to adjust the resources given to {{agent}}.


## Role Based Access Control for {{agent}} [k8s-elastic-agent-fleet-configuration-role-based-access-control]

Some {{agent}} features, such as the [{{k8s}} integration](https://epr.elastic.co/package/kubernetes/0.2.8/), require that Agent Pods interact with {{k8s}} APIs. This functionality requires specific permissions. Standard {{k8s}} [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) rules apply. For example, to allow API interactions:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent-sample
spec:
  version: {{version.stack}}
  elasticsearchRefs:
  - name: elasticsearch-sample
  daemonSet:
    podTemplate:
      spec:
        automountServiceAccountToken: true
        serviceAccountName: elastic-agent
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


## Deploy {{agent}} in secured clusters [k8s-elastic-agent-fleet-configuration-deploying-in-secured-clusters]

To deploy {{agent}} in clusters with the Pod Security Policy admission controller enabled, or in [OpenShift](k8s-openshift-agent.md) clusters, you might need to grant additional permissions to the Service Account used by the {{agent}} Pods. Those Service Accounts must be bound to a Role or ClusterRole that has `use` permission for the required Pod Security Policy or Security Context Constraints. Different {{agent}} {{integrations}} might require different settings set in their PSP/[SCC](k8s-openshift-agent.md).


## Customize {{fleet-server}} Service [k8s-elastic-agent-fleet-configuration-customize-fleet-server-service]

By default, ECK creates a Service for {{fleet-server}} that {{agents}} can connect through. You can customize it using the `http` configuration element. Check more information on how to [make changes](accessing-services.md) to the Service and [customize](/deploy-manage/security/secure-cluster-communications.md) the TLS configuration.


## Control {{fleet}} policy selection [k8s-elastic-agent-control-fleet-policy-selection]

ECK uses the default policy to enroll {{agents}} in {{fleet}} and the default {{fleet-server}} policy to enroll {{fleet-server}}. A different policy can be chosen by using the `policyID` attribute in the {{agent}} resource:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server-sample
spec:
  policyID: my-custom-policy
...
```

Note that the environment variables related to policy selection mentioned in the {{agent}} [docs](/reference/fleet/agent-environment-variables.md) like `FLEET_SERVER_POLICY_ID` will be managed by the ECK operator.


## Running as a non-root user [k8s-elastic-agent-running-as-a-non-root-user]

In order to run {{agent}} as a non-root user you must choose how you want to persist data to the Agent’s volume.

::::{tab-set}

:::{tab-item} {{agent}} 8.16 and higher

1. Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
2. Run {{agent}} with a `hostPath` volume. No additional configuration is required.

:::

:::{tab-item} {{agent}} 8.15 and before 

1. Run {{agent}} with an `emptyDir` volume. This has the downside of not persisting data between restarts of the {{agent}} which can duplicate work done by the previous running Agent.
2. Run {{agent}} with a `hostPath` volume which has the advantage of persisting data between restarts of the {{agent}}.

In addition to these decisions, if you are running {{agent}} in {{fleet}} mode as a non-root user, you must configure `ssl.certificate_authorities` in each `xpack.fleet.outputs` to trust the CA of the {{es}} Cluster.

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


To run {{agent}} with a `hostPath` volume.

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

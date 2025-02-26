---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/advanced-kubernetes-managed-by-fleet.html
---

# Advanced Elastic Agent configuration managed by Fleet [advanced-kubernetes-managed-by-fleet]

For basic {{agent}} managed by {{fleet}} scenarios follow the steps in [Run {{agent}} on Kubernetes managed by {{fleet}}](/reference/ingestion-tools/fleet/running-on-kubernetes-managed-by-fleet.md).

On managed {{agent}} installations it can be useful to provide the ability to configure more advanced options, such as the configuration of providers during the startup. Refer to [Providers](/reference/ingestion-tools/fleet/providers.md) for more details.

Following steps demonstrate above scenario:


## Step 1: Download the {{agent}} manifest [_step_1_download_the_agent_manifest_2]

It is advisable to follow the steps of [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md) with Kubernetes Integration installed in your policy and download the {{agent}} manifest from Kibana UI

:::{image} images/k8skibanaUI.png
:alt: {{agent}} with K8s Package manifest
:::

Notes
:   Sample manifests can also be found [here](https://github.com/elastic/elastic-agent/blob/main/deploy/kubernetes/elastic-agent-managed-kubernetes.yaml)


## Step 2: Create a new configmap [_step_2_create_a_new_configmap]

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-node-datastreams
  namespace: kube-system
  labels:
    k8s-app: elastic-agent
data:
  agent.yml: |-
    providers.kubernetes_leaderelection.enabled: false
    fleet.enabled: true
    fleet.access_token: "<FLEET_ENROLLMENT_TOKEN>"
---
```

Notes
:   1. In the above example the disablement of `kubernetes_leaderelection` provider is demonstrated. Same procedure can be followed for alternative scenarios.


```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: agent-node-datastreams
  namespace: kube-system
  labels:
    k8s-app: elastic-agent
data:
  agent.yml: |-
    providers.kubernetes:
      add_resource_metadata:
        deployment: true
        cronjob: true
    fleet.enabled: true
    fleet.access_token: "<FLEET_ENROLLMENT_TOKEN>"
---
```

1. Find more information about [Enrollment Tokens](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md).


## Step 3: Configure Daemonset [_step_3_configure_daemonset]

Inside the downloaded manifest, update the Daemonset resource:

```yaml
containers:
  - name: elastic-agent
    image: docker.elastic.co/elastic-agent/elastic-agent: <ImageVersion>
    args: ["-c", "/etc/elastic-agent/agent.yml", "-e"]
```

Notes
:   The <ImageVersion> is just a placeholder for the elastic-agent image version that you will download in your manifest: eg. `image: docker.elastic.co/elastic-agent/elastic-agent: 8.11.0` Important thing is to update your manifest with args details

```yaml
volumeMounts:
  - name: datastreams
    mountPath: /etc/elastic-agent/agent.yml
    readOnly: true
    subPath: agent.yml
```

```yaml
volumes:
  - name: datastreams
    configMap:
      defaultMode: 0640
      name: agent-node-datastreams
```


## Important Notes [_important_notes]

1. By default the manifests for {{agent}} managed by {{fleet}} have `hostNetwork:true`. In order to support multiple installations of {{agent}}s in the same node you should set `hostNetwork:false`. See this relevant [example](https://github.com/elastic/elastic-agent/tree/main/docs/manifests/hostnetwork) as described in [{{agent}} Manifests in order to support Kube-State-Metrics Sharding](https://github.com/elastic/elastic-agent/blob/main/docs/elastic-agent-ksm-sharding.md).
2. The volume `/usr/share/elastic-agent/state` must remain mounted in [elastic-agent-managed-kubernetes.yaml](https://github.com/elastic/elastic-agent/blob/main/deploy/kubernetes/elastic-agent-managed-kubernetes.yaml), otherwise custom config map provided above will be overwritten.


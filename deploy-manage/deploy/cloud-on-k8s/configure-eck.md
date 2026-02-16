---
navigation_title: Apply configuration settings
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-operator-config.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Apply ECK configuration settings [k8s-operator-config]

This page explains the various methods for configuring and applying ECK settings.

::::{tip}
For a detailed list and description of all available settings in ECK, refer to [ECK configuration flags](cloud-on-k8s://reference/eck-configuration-flags.md).
::::

By default, the ECK installation includes a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) with an `eck.yaml` key where you can add, remove, or update configuration settings. This ConfigMap is mounted into the operator’s container as a file, and provided to the application through the `--config` flag.

::::{note}
If you use [Operator Lifecycle Manager](https://github.com/operator-framework/operator-lifecycle-manager), refer to [Configure ECK under Operator Lifecycle Manager](#k8s-operator-config-olm)
::::

To configure ECK settings, follow the instructions in the next sections depending on whether you installed ECK through the Helm chart or the YAML manifests.

## Using the operator Helm chart

If you installed ECK through the Helm chart commands listed in [](./install-using-helm-chart.md), add your configuration parameters under the `config` key in your values file, or set them inline using the equivalent `--set config.<setting-name>=<value>` flags when updating or installing the release.

Note that the Helm chart uses its own configuration parameters rather than the actual ECK parameters that are described in [{{eck}} configuration flags](cloud-on-k8s://reference/eck-configuration-flags.md). To view all configurable values in the Helm chart for the ECK operator, run the following command:

```sh
helm show values elastic/eck-operator
```

For example, the parameter `caValidity` in the Helm chart corresponds to the `ca-cert-validity` ECK parameter. To add the `caValidity` setting with a value of `43800h`, you can use either of the following methods:

### Option 1: Use a values file and reference it in the helm upgrade command:

Create a values file with the following content:

```yaml
config:
  caValidity: 43800h
```

Then, update the installed release pointing to the values file:

```sh
helm upgrade elastic-operator elastic/eck-operator -f my-values-file.yaml -n elastic-system
```

### Option 2: Use `--set` in the helm upgrade command

```sh
helm upgrade elastic-operator elastic/eck-operator --set config.caValidity=43800h -n elastic-system
```

## Using the operator YAML manifests

If you installed ECK using the manifests and the commands listed in [Deploy ECK](./install-using-yaml-manifest-quickstart.md), you can configure it by editing the `eck.yaml` key of the `elastic-operator` ConfigMap. Add, remove or update any configuration setting there and the operator will restart automatically to apply the new changes unless the `--disable-config-watch` flag is set.

You can update the ConfigMap directly using the command `kubectl edit configmap elastic-operator -n elastic-operator` or modify the installation manifests and reapply them with `kubectl apply -f <your-manifest-file.yaml>`.

The following shows the default `elastic-operator` ConfigMap, for reference purposes. Refer to [ECK configuration flags](cloud-on-k8s://reference/eck-configuration-flags.md) for a complete list of available settings.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elastic-operator
  namespace: elastic-system
data:
  eck.yaml: |-
    log-verbosity: 0
    metrics-port: 0
    container-registry: docker.elastic.co
    max-concurrent-reconciles: 3
    ca-cert-validity: 8760h
    ca-cert-rotate-before: 24h
    cert-validity: 8760h
    cert-rotate-before: 24h
    disable-config-watch: false
    exposed-node-labels: [topology.kubernetes.io/.*,failure-domain.beta.kubernetes.io/.*]
    set-default-security-context: auto-detect
    kube-client-timeout: 60s
    elasticsearch-client-timeout: 180s
    disable-telemetry: false
    distribution-channel: all-in-one
    validate-storage-class: true
    enable-webhook: true
    webhook-name: elastic-webhook.k8s.elastic.co
    webhook-port: 9443
    operator-namespace: elastic-system
    enable-leader-election: true
    elasticsearch-observation-interval: 10s
    ubi-only: false
    password-length: 24
```

Alternatively, you can edit the `elastic-operator` StatefulSet and add flags to the `args` section of the operator container — which will trigger an automatic restart of the operator pod by the StatefulSet controller.

## Configure ECK under Operator Lifecycle Manager [k8s-operator-config-olm]

If you use [Operator Lifecycle Manager (OLM)](https://github.com/operator-framework/operator-lifecycle-manager) to install and run ECK, follow these steps to configure the operator:

* Create a new ConfigMap in the same namespace as the operator. It should contain a key named `eck.yaml` pointing to the desired configuration values.

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: elastic-operator
      namespace: openshift-operators
    data:
      eck.yaml: |-
        log-verbosity: 0
        metrics-port: 6060
        container-registry: docker.elastic.co
        max-concurrent-reconciles: 3
        ca-cert-validity: 8760h
        ca-cert-rotate-before: 24h
        cert-validity: 8760h
        cert-rotate-before: 24h
    ```

* Update your [Subscription](https://github.com/operator-framework/operator-lifecycle-manager/blob/master/doc/design/subscription-config.md) to mount the ConfigMap under `/conf`.

    ```yaml subs=true
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: elastic-cloud-eck
      namespace: openshift-operators
    spec:
      channel: stable
      installPlanApproval: Automatic
      name: elastic-cloud-eck
      source: elastic-operators
      sourceNamespace: openshift-marketplace
      startingCSV: elastic-cloud-eck.v{{version.eck}}
      config:
        volumes:
          - name: config
            configMap:
              name: elastic-operator
        volumeMounts:
          - name: config
            mountPath: /conf
            readOnly: true
    ```

## Advanced configuration methods

ECK can be configured using either command-line flags, environment variables or a file containing the operator configuration, pointed by `--config` flag.

::::{important}
For most use cases, Elastic recommends configuring ECK through the `elastic-operator` ConfigMap, which is included by default in all installation methods.

This section provides a low-level overview of alternative configuration methods, primarily intended for developers or advanced users who might need to start the operator binary manually or adjust its configuration without modifying the ConfigMap. The implementation of these methods through Kubernetes manifests is out of the scope of this document.
::::

To pass configuration options as environment variables, convert the flag name to upper case and replace any dashes (`-`) with underscores (`_`). For example, the `log-verbosity` flag can be set by an environment variable named `LOG_VERBOSITY`.

If you use a combination of all or some of the these methods, the descending order of precedence in case of a conflict is as follows:

* Flag
* Environment variable
* File

If you have a large number of configuration options to specify, use the `--config` flag to point to a file containing those options. For example, assume you have a file named `eck-config.yaml` with the following content:

```yaml
log-verbosity: 2
metrics-port: 6060
namespaces: [ns1, ns2, ns3]
```

The operator can be started using any of the following methods to achieve the same end result:

```sh
./elastic-operator manager --config=eck-config.yaml
```

```sh
./elastic-operator manager --log-verbosity=2 --metrics-port=6060 --namespaces=ns1,ns2,ns3
```

```sh
LOG_VERBOSITY=2 METRICS_PORT=6060 NAMESPACES="ns1,ns2,ns3" ./elastic-operator manager
```

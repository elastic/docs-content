---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html
---

# Custom configuration files and plugins [k8s-bundles-plugins]

To run {{es}} with specific plugins or configuration files installed on ECK, you have multiple options. Each option has its own pros and cons.

1. Create a custom container image with the required plugins and configuration files.

    * **Pros**

        * Deployment is reproducible and reusable.
        * Does not require internet access at runtime.
        * Saves bandwidth and is quicker to start.

    * **Cons**

        * Requires a container registry and build infrastructure to build and host the custom image.
        * Version upgrades require building a new container image.

2. Use init containers to install plugins and configuration files.

    * **Pros**

        * Easier to get started and upgrade versions.

    * **Cons**

        * Requires pods to have internet access. **Check [the note about using Istio](#istio-note)**.
        * Adding new {{es}} nodes could randomly fail due to network issues or bad configuration.
        * Each {{es}} node needs to repeat the download, wasting bandwidth and slowing startup.
        * Deployment manifests are more complicated.

3. Use ConfigMaps or Secrets together with volumes and volume mounts for configuration files.

    * **Pros**

        * Best choice for injecting configuration files into your {{es}} nodes.
        * Follows standard Kubernetes methodology to mount files into Pods.

    * **Cons**

        * Not valid for plugins installation.
        * Requires to maintain the ConfigMaps or Secrets with the content of the files.

The following sections provide examples for each of the mentioned options.

## Create a custom image

Refer to [Creating custom images](create-custom-images.md) for instructions on how to build custom Docker images based on the official Elastic images.

## Use init containers for plugins installation

The following example describes option 2, using a repository plugin. To install the plugin before the {{es}} nodes start, use an init container to run the [plugin installation tool](elasticsearch://reference/elasticsearch-plugins/installation.md).

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        initContainers:
        - name: install-plugins
          command:
          - sh
          - -c
          - |
            bin/elasticsearch-plugin remove --purge repository-azure
            bin/elasticsearch-plugin install --batch repository-azure
```

### Note when using Istio [istio-note]

When using Istio, init containers do **not** have network access, as the Envoy sidecar that provides network connectivity is not started yet. In this scenario, custom containers are the best option. If custom containers are simply not a viable option, then it is possible to adjust the startup command for the {{es}} container itself to run the plugin installation before starting {{es}}, as the following example describes. Note that this approach will require updating the startup command if it changes in the {{es}} image, which could potentially cause failures during upgrades.

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          command:
          - /usr/bin/env
          - bash
          - -c
          - |
            #!/usr/bin/env bash
            set -e
            bin/elasticsearch-plugin remove --purge repository-s3 || true
            bin/elasticsearch-plugin install --batch repository-s3
            /bin/tini -- /usr/local/bin/docker-entrypoint.sh
```

## Use a volume and volume mount together with a ConfigMap or Secret

To install custom configuration files you can:

1. Add the configuration data into a ConfigMap or Secret.
2. Use volumes and volume mounts in your manifest to mount the contents of the ConfigMap or Secret as files in your {{es}} nodes.

The next example shows how to add a synonyms file for the [synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md) in {{es}}. But you can **use the same approach for any kind of file you want to mount into the configuration directory of Elasticsearch**, like adding CA certificates of external systems.

1. Create the ConfigMap or Secret with the data:

There are multiple ways to create and mount [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) on Kubernetes. Refer to the official documentation for more details.

This example shows how to create a ConfigMap named `synonyms` with the content of a local file named `my-synonyms.txt` added into the `synonyms-elasticsearch.txt` key of the ConfigMap.

```sh
kubectl create configmap synonyms -n <namespace> --from-file=my-synonyms.txt=synonyms-elasticsearch.txt
```

::::{tip}
Create the ConfigMap or Secret in the same namespace where your {{es}} cluster runs.
::::

2. Declare the ConfigMap as a volume and mount it in the {{es}} containers.

In this example, modify your {{es}} manifest to mount the contents of the `synonyms` ConfigMap into `/usr/share/elasticsearch/config/dictionaries` on the {{es}} nodes.

```yaml
spec:
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      spec:
        containers:
        - name: elasticsearch <1>
          volumeMounts:
          - name: synonyms
            mountPath: /usr/share/elasticsearch/config/dictionaries <2>
        volumes:
        - name: synonyms
          configMap: <3>
            name: synonyms <4>
```

1. {{es}} runs by convention in a container called `elasticsearch`. Do not change that value.
2. Use always a path under `/usr/share/elasticsearch/config`.
3. Use `secret` instead of `configMap` if you used a secret to store the data.
4. The ConfigMap name must be the same as the ConfigMap created in the previous step.

After the changes are applied, {{es}} nodes should be able to access `dictionaries/synonyms-elasticsearch.txt` and use it in any [configuration setting](./node-configuration.md).

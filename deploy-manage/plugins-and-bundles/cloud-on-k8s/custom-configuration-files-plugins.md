---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html
description: Mount configuration files into Elasticsearch pods on ECK with ConfigMaps or Secrets.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: ConfigMaps and Secrets
---

# Add configuration files with ConfigMaps or Secrets [k8s-bundles-plugins]

To install custom configuration files you can:

1. Add the configuration data into a ConfigMap or Secret.
2. Use volumes and volume mounts in your manifest to mount the contents of the ConfigMap or Secret as files in your {{es}} nodes.

The next example shows how to add a synonyms file for the [synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md) in {{es}}. But you can **use the same approach for any kind of file you want to mount into the configuration directory of Elasticsearch**, like adding CA certificates of external systems.

## Create the ConfigMap or Secret [use-a-volume-and-volume-mount-together-with-a-configmap-or-secret]

There are multiple ways to create and mount [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) on Kubernetes. Refer to the official documentation for more details.

This example shows how to create a ConfigMap named `synonyms` with the content of a local file named `my-synonyms.txt` added into the `synonyms-elasticsearch.txt` key of the ConfigMap.

```sh
kubectl create configmap synonyms -n <namespace> --from-file=my-synonyms.txt=synonyms-elasticsearch.txt
```

::::{tip}
Create the ConfigMap or Secret in the same namespace where your {{es}} cluster runs.
::::

## Declare the volume and volume mount

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

After the changes are applied, {{es}} nodes should be able to access `dictionaries/synonyms-elasticsearch.txt` and use it in any [configuration setting](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md).

::::{note}
ConfigMaps and Secrets are for configuration files only. Mounting plugin files does not install them. To install plugins, use a [custom image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md) or [init containers](init-containers-for-plugin-downloads.md).
::::

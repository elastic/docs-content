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

On {{eck}}, configuration files such as synonym dictionaries, scripts, SAML metadata, or CA certificates are not delivered as ZIP *bundles*. Instead, you store the content in a ConfigMap or Secret, then mount it into your {{es}} pods with volumes and volume mounts.

This page walks through a synonyms file for the [synonym token filter](elasticsearch://reference/text-analysis/analysis-synonym-tokenfilter.md). You can use the same pattern for any other file you want to mount into the configuration directory of {{es}}, like adding CA certificates of external systems for example.

::::{note}
ConfigMaps and Secrets are for configuration files only. They do not install plugins. To install plugins, use a [custom image](/deploy-manage/deploy/cloud-on-k8s/create-custom-images.md) or [init containers](init-containers-for-plugin-downloads.md).
::::

## Create the ConfigMap or Secret [use-a-volume-and-volume-mount-together-with-a-configmap-or-secret]

There are multiple ways to create and mount [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) on Kubernetes. Refer to the Kubernetes documentation for details.

This example creates a ConfigMap named `synonyms` from a local file `my-synonyms.txt`, stored under the key `synonyms-elasticsearch.txt`:

```sh
kubectl create configmap synonyms -n <namespace> --from-file=my-synonyms.txt=synonyms-elasticsearch.txt
```

::::{tip}
Create the ConfigMap or Secret in the same namespace where your {{es}} cluster runs.
::::

## Mount the ConfigMap in the {{es}} pods

Update your {{es}} manifest to mount the `synonyms` ConfigMap at `/usr/share/elasticsearch/config/dictionaries`:

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
2. Always use a path under `/usr/share/elasticsearch/config`.
3. Use `secret` instead of `configMap` if you stored the data in a Secret.
4. The ConfigMap name must match the ConfigMap created in the previous step.

After you apply the changes, the nodes can read `dictionaries/synonyms-elasticsearch.txt` and reference it from any [configuration setting](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md).

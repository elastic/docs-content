---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-bundles-plugins.html
---

# Custom configuration files and plugins [k8s-bundles-plugins]

To run Elasticsearch with specific plugins or configuration files installed on ECK, you have two options. Each option has its own pros and cons.

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
        * Adding new Elasticsearch nodes could randomly fail due to network issues or bad configuration.
        * Each Elasticsearch node needs to repeat the download, wasting bandwidth and slowing startup.
        * Deployment manifests are more complicated.


Refer to [Creating custom images](create-custom-images.md) for instructions on how to build custom Docker images based on the official Elastic images.

The following example describes option 2, using a repository plugin. To install the plugin before the Elasticsearch nodes start, use an init container to run the [plugin installation tool](https://www.elastic.co/guide/en/elasticsearch/plugins/current/installation.html).

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

To install custom configuration files you can use volumes and volume mounts.

The next example shows how to add a synonyms file for the [synonym token filter](https://www.elastic.co/guide/en/elasticsearch/reference/current/analysis-synonym-tokenfilter.html) in Elasticsearch. But you can use the same approach for any kind of file you want to mount into the configuration directory of Elasticsearch.

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
            mountPath: /usr/share/elasticsearch/config/dictionaries
        volumes:
        - name: synonyms
          configMap:
            name: synonyms <2>
```

1. Elasticsearch runs by convention in a container called *elasticsearch*.
2. Assuming you have created a config map in the same namespace as Elasticsearch with the name *synonyms* containing the synonyms file(s).


$$$istio-note$$$
**Note when using Istio**

When using Istio, init containers do **not** have network access, as the Envoy sidecar that provides network connectivity is not started yet. In this scenario, custom containers are the best option. If custom containers are simply not a viable option, then it is possible to adjust the startup command for the elasticsearch container itself to run the plugin installation before starting Elasticsearch, as the following example describes. Note that this approach will require updating the startup command if it changes in the Elasticsearch image, which could potentially cause failures during upgrades.

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

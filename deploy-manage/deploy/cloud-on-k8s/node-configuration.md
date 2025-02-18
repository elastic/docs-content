---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-node-configuration.html
---

# Node configuration [k8s-node-configuration]

Any setting defined in the `elasticsearch.yml` configuration file can also be defined for a set of Elasticsearch nodes in the `spec.nodeSets[?].config` section.

Some settings are managed by ECK, it is not recommended to change them, refer to [Settings managed by ECK](settings-managed-by-eck.md) for more details.

```yaml
spec:
  nodeSets:
  - name: masters
    count: 3
    config:
      # On Elasticsearch versions before 7.9.0, replace the node.roles configuration with the following:
      # node.master: true
      node.roles: ["master"]
      xpack.ml.enabled: true
  - name: data
    count: 10
    config:
      # On Elasticsearch versions before 7.9.0, replace the node.roles configuration with the following:
      # node.master: false
      # node.data: true
      # node.ingest: true
      # node.ml: true
      # node.transform: true
      node.roles: ["data", "ingest", "ml", "transform"]
```

For more information on Elasticsearch settings, check [Configuring Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html).


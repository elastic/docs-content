{{es}} settings that are typically defined in the `elasticsearch.yml` configuration file can be specified for a set of nodes in the `spec.nodeSets[?].config` section of the {{es}} resource manifest.

Some settings are managed by ECK. It is not recommended to change these managed settings. For a complete list, refer to [Settings managed by ECK](/deploy-manage/deploy/cloud-on-k8s/settings-managed-by-eck.md).

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

:::{warning}
ECK parses {{es}} configuration and normalizes it to YAML. Consequently, some {{es}} configuration schema are impossible to express with ECK and, therefore, must be set using [dynamic cluster settings](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#cluster-setting-types). For example:
```yaml
spec:
  nodeSets:
  - name: data
    # ...
    config:
      cluster.max_shards_per_node: 1000
      cluster.max_shards_per_node.frozen: 1000 # This won't work because cluster.max_shards_per_node is defined as a scalar value on the previous line
    # ...
```
:::
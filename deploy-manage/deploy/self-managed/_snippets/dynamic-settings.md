You can configure and update dynamic settings on a running cluster using the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings). You can also configure dynamic settings locally on an unstarted or shut down node using `elasticsearch.yml`.

Updates made using the cluster update settings API can be *persistent*, which apply across cluster restarts, or *transient*, which reset after a cluster restart. You can also reset transient or persistent settings by assigning them a `null` value using the API.

If you configure the same setting using multiple methods, {{es}} applies the settings in following order of precedence:

1. Transient setting
2. Persistent setting
3. `elasticsearch.yml`setting
4. Default setting value

For example, you can apply a transient setting to override a persistent setting or `elasticsearch.yml` setting. However, a change to an `elasticsearch.yml` setting will not override a defined transient or persistent setting.

::::{warning} 
We no longer recommend using transient cluster settings. Use persistent cluster settings instead. If a cluster becomes unstable, transient settings can clear unexpectedly, resulting in a potentially undesired cluster configuration.
::::

In a self-managed cluster, you should use the [cluster update settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) to configure dynamic cluster settings, and only use `elasticsearch.yml` for static cluster settings and node settings. The API doesn’t require a restart and ensures a setting’s value is the same on all nodes.

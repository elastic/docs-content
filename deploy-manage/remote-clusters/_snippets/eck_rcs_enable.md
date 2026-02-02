<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- eck-remote-clusters.md
- eck-remote-clusters-to-other-eck.md
- ece-enable-ccs-for-eck.md
- ec-enable-ccs-for-eck.md
-->
By default, the remote cluster server interface is not enabled on ECK-managed clusters. To use the API key–based security model for cross-cluster connections, you must first enable it on the remote {{es}} cluster by setting `spec.remoteClusterServer.enabled: true`:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: <cluster-name>
  namespace: <namespace>
spec:
  version: {{version.stack}}
  remoteClusterServer:
    enabled: true
  nodeSets:
    - name: default
      count: 3
      ...
      ...
```

::::{note}
Enabling the remote cluster server triggers a restart of the {{es}} cluster.
::::


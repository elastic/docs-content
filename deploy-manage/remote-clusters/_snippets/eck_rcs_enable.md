By default, the remote cluster server interface is not enabled on ECK clusters. To use the API key–based security model for cross-cluster connections, you must first enable it on the remote {{es}} cluster by setting `spec.remoteClusterServer.enabled: true`:

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


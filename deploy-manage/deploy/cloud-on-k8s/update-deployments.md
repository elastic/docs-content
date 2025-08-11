---
navigation_title: Applying updates
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-update-deployment.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Update your deployments [k8s-update-deployment]

You can add and modify most elements of the original Kubernetes cluster specification provided that they translate to valid transformations of the underlying Kubernetes resources (for example [existing volume claims cannot be downsized](volume-claim-templates.md)). The ECK operator will attempt to apply your changes with minimal disruption to the existing cluster. You should ensure that the Kubernetes cluster has sufficient resources to accommodate the changes (extra storage space, sufficient memory and CPU resources to temporarily spin up new pods, and so on).

For example, you can grow the cluster to three {{es}} nodes from the [deployed {{es}} cluster](elasticsearch-deployment-quickstart.md) example by updating the `count` with [`apply`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/):

```yaml subs=true
cat <<EOF | kubectl apply -f -
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
EOF
```

ECK will automatically schedule the requested update. Changes can be monitored with the [ECK operator logs](install-using-yaml-manifest-quickstart.md), [`events`](https://kubernetes.io/docs/reference/kubernetes-api/cluster-resources/event-v1/), and applicable product’s [pod `logs`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/). These will either report successful application of changes or provide context for further troubleshooting. Kindly note, Kubernetes restricts some changes, for example refer to [Updating Volume Claims](volume-claim-templates.md#k8s-volume-claim-templates-update).
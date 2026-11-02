---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-maps-es.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Deploy {{hosted-ems}} [k8s-maps-es]

Deploying [{{hosted-ems}}](elastic-maps-server.md) can be done with a simple manifest:

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
```

{{hosted-ems}} requires a valid Enterprise license or Enterprise trial license. Refer to [Manage your license in ECK](../../license/manage-your-license-in-eck.md) for more information.

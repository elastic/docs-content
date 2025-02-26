---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stateless-autoscaling.html
---

# Autoscaling stateless applications on ECK [k8s-stateless-autoscaling]

::::{note} 
This section only applies to stateless applications. Check [Elasticsearch autoscaling](deployments-autoscaling-on-eck.md) for more details about scaling automatically Elasticsearch.
::::


The [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale) can be used to automatically scale the deployments of the following resources:

* Kibana
* APM Server
* Elastic Maps Server

These resources expose the `scale` subresource which can be used by the Horizontal Pod Autoscaler controller to automatically adjust the number of replicas according to the CPU load or any other custom or external metric. This example shows how to create an `HorizontalPodAutoscaler` resource to adjust the replicas of a Kibana deployment according to the CPU load:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  nodeSets:
    - name: default
      count: 1
      config:
        node.store.allow_mmap: false

apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: kb
spec:
  scaleTargetRef:
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    name: kibana-sample
  minReplicas: 1
  maxReplicas: 4
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
```


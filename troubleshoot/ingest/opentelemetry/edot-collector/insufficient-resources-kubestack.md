---
navigation_title: Insufficient resources with Kube-Stack chart
description: Learn what to do when the Kube-Stack chart is deployed with insufficient resources.
applies_to:
  stack:
  serverless:
    observability:
  product:
    edot_collector: ga
products:
  - id: cloud-serverless
  - id: observability
  - id: edot-collector
---

# Insufficient resources issue with Kube-Stack Helm Chart

The OpenTelemetry Kube-Stack Helm Chart deploys multiple EDOT collectors with varying configurations based on the selected architecture and deployment mode. On larger clusters, the default Kubernetes resource limits might be insufficient.

## Symptoms   

These symptoms are common when the Kube-Stack chart is deployed with insufficient resources:

- Collector Pods in a `CrashLoopBackOff`/`OOMKilled` state.
- Cluster or Daemon pods are unable to export data to the Gateway collector due being `OOMKilled` (high memory usage). 
- Pods have logs similar to: `error	internal/queue_sender.go:128	Exporting failed. Dropping data.`

## Resolution

Follow these steps to resolve the issue.

:::::{stepper}

::::{step} Check for OOMKilled Pods
Run the following command to check the Pods:

```bash
kubectl get pods -n opentelemetry-operator-system
```

Look for any Pods in the `OOMKilled` state:

```
NAME                                                              READY   STATUS             RESTARTS      AGE
opentelemetry-kube-stack-cluster-stats-collector-7cd88c77drvj76   1/1     Running            0             49s
opentelemetry-kube-stack-daemon-collector-pn4qj                   1/1     Running            0             47s
opentelemetry-kube-stack-gateway-collector-85795c7965-wxqls       0/1     OOMKilled          3 (34s ago)   49s
opentelemetry-kube-stack-gateway-collector-8cfdb59df-lgpbr        0/1     OOMKilled          3 (30s ago)   49s
opentelemetry-kube-stack-gateway-collector-8cfdb59df-s7plz        0/1     CrashLoopBackOff   2 (17s ago)   34s
opentelemetry-kube-stack-opentelemetry-operator-77d46bc4dbv2h6k   2/2     Running            0             3m14s
```
::::

::::{step} Verify the Pod last status

Run the following command to verify the last status of the Pod:

```bash
kubectl describe pod -n opentelemetry-operator-system opentelemetry-kube-stack-gateway-collector-85795c7965-wxqls
 
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
```
::::

::::{step} Increase resource limits

Edit the `values.yaml` file used to deploy the corresponding Helm release. For the Gateway collector, ensure horitzontal Pod autoscaling is turned on. The Gateway collector configuration should be similar to this:

```yaml
  gateway:
    fullnameOverride: "opentelemetry-kube-stack-gateway"
    suffix: gateway
    replicas: 2
    autoscaler:
      minReplicas: 2 # Start with at least 2 replicas for better availability.
      maxReplicas: 5 # Allow more scale-out if needed.
      targetCPUUtilization: 70 # Scale when CPU usage exceeds 70%.
      targetMemoryUtilization: 75 # Scale when memory usage exceeds 75%.
```

If the autoscaler configuration is already available, or another Collector type is running out of memory, increase the resource limits in the corresponding Collector configuration section:

```yaml
  gateway:
    fullnameOverride: "opentelemetry-kube-stack-gateway"
    ...
    resources:
      limits:
        cpu: 500m
        memory: 20Mi
      requests:
        cpu: 100m
        memory: 10Mi
```

Make sure to update the resource limits within the correct Collector type section. Available types are: `gateway`, `daemon`, `cluster`, and `opentelemetry-operator`.
::::

::::{step} Update the Helm release

Run the following command to update the Helm release:

```bash
$ helm upgrade opentelemetry-kube-stack open-telemetry/opentelemetry-kube-stack --namespace opentelemetry-operator-system --values values.yaml --version '0.6.3'
```

:::{note}
The hard memory limit should be around 2GB.
:::
::::
::::: 

## Resources

* [Elastic Kube-stack Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-kube-stack)  
* [Elastic stack Kubernetes Helm charts](https://github.com/elastic/helm-charts)
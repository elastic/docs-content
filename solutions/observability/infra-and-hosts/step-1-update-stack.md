---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-self-managed-updating.html
applies_to:
  stack: ga
products:
  - id: observability
---

# Step 1: Update the stack [profiling-self-managed-updating]

To install the Universal Profiling backend, you need to be running the minimum supported version of the Elastic stack. Refer to the following instructions to update the stack on your platform:

* [ECE](#profiling-self-managed-updating-ece)
* [Self-managed Elastic stack](#profiling-self-managed-updating-self-managed)
* [Kubernetes](#profiling-self-managed-updating-k8s)


## ECE [profiling-self-managed-updating-ece]

Update ECE to version 3.7.0 or higher, following the [installations instructions](https://www.elastic.co/downloads/enterprise).


## Self-managed Elastic stack [profiling-self-managed-updating-self-managed]

::::{warning}
We don’t currently support running the backend applications through Elastic Agent.
::::


1. Deploy a minimum version 8.12.0 of the Elastic stack (Elasticsearch, Kibana).
2. Ensure the machines hosting the Universal Profiling backend run a Linux kernel version 4.x or higher.


## Kubernetes [profiling-self-managed-updating-k8s]

We don’t currently support running the *backend* applications through ECK, but, if you’re running an Elastic stack through ECK, you can still connect the Universal Profiling backend applications to it.

1. Update the ECK deployment you want to enable Universal Profiling to 8.12.0 or higher.
2. If you’re not using ECK, ensure your deployments of Elasticsearch and Kibana are configured to use the minimum supported version (8.12.0 or higher).

Continue to [Step 2: Enable Universal Profiling in Kibana](step-2-enable-universal-profiling-in-kibana.md).


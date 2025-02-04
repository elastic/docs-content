---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-setting-virtual-memory.html
---

# Ensuring virtual memory kernel settings [k8s-autopilot-setting-virtual-memory]

If you are intending to run production workloads on GKE Autopilot then `vm.max_map_count` should be set. The recommended way to set this kernel setting on the Autopilot hosts is with a `Daemonset` as described in the [Virtual memory](virtual-memory.md) section. You must be running at least version 1.25 when on the `regular` channel or using the `rapid` channel, which currently runs version 1.27.

::::{warning}
Only use the provided `Daemonset` exactly as specified or it could be rejected by the Autopilot control plane.
::::
